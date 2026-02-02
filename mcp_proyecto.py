from fastmcp import FastMCP
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Any

# MCP Server
mcp = FastMCP("Alquiler de Películas")

# CONFIGURACIÓN POSTGRES
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "ProyectoLP",
    "user": "postgres",
    "password": "Admin123**"
}

def conectar_bd():
    return psycopg2.connect(**DB_CONFIG)


@mcp.tool()
def listar_tablas(schema: str = "public") -> List[str]:
    """
    Lista las tablas de un schema (por defecto public)
    """
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = %s
          AND table_type = 'BASE TABLE'
        ORDER BY table_name
    """, (schema,))

    tablas = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tablas

@mcp.tool()
def describir_tabla(nombre_tabla: str, schema: str = "public") -> Dict[str, Any]:
    """
    Describe una tabla de PostgreSQL
    """
    conn = conectar_bd()
    cursor = conn.cursor()

    # Columnas
    cursor.execute("""
        SELECT
            column_name,
            data_type,
            is_nullable,
            column_default
        FROM information_schema.columns
        WHERE table_schema = %s
          AND table_name = %s
        ORDER BY ordinal_position
    """, (schema, nombre_tabla))

    columnas = cursor.fetchall()

    # Claves primarias
    cursor.execute("""
        SELECT kcu.column_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
          ON tc.constraint_name = kcu.constraint_name
        WHERE tc.constraint_type = 'PRIMARY KEY'
          AND tc.table_schema = %s
          AND tc.table_name = %s
    """, (schema, nombre_tabla))

    pk_cols = {row[0] for row in cursor.fetchall()}

    # Conteo de registros
    cursor.execute(f'SELECT COUNT(*) FROM "{schema}"."{nombre_tabla}"')
    total_registros = cursor.fetchone()[0]

    conn.close()

    return {
        "schema": schema,
        "tabla": nombre_tabla,
        "total_registros": total_registros,
        "columnas": [
            {
                "nombre": col[0],
                "tipo": col[1],
                "no_nulo": col[2] == "NO",
                "valor_por_defecto": col[3],
                "es_clave_primaria": col[0] in pk_cols
            }
            for col in columnas
        ]
    }

@mcp.tool()
def ejecutar_consulta(sql: str) -> List[Dict[str, Any]]:
    """
    Ejecuta consultas SELECT de solo lectura en PostgreSQL
    """
    sql_upper = sql.strip().upper()

    if not sql_upper.startswith("SELECT"):
        return [{
            "error": "Solo se permiten consultas SELECT",
            "tipo": "SecurityError"
        }]

    palabras_prohibidas = [
        "INSERT", "UPDATE", "DELETE", "DROP",
        "ALTER", "CREATE", "TRUNCATE"
    ]

    if any(p in sql_upper for p in palabras_prohibidas):
        return [{
            "error": "Consulta contiene palabras no permitidas",
            "tipo": "SecurityError"
        }]

    try:
        conn = conectar_bd()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(sql)
        resultados = cursor.fetchall()
        conn.close()
        return resultados

    except psycopg2.Error as e:
        return [{
            "error": str(e),
            "tipo": "PostgreSQLError"
        }]


if __name__ == "__main__":
    mcp.run()
