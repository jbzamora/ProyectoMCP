Descarga UV
https://docs.astral.sh/uv/getting-started/installation/#standalone-installer

En Consola Ejecuta: 
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

En la carpeta del proyecto python x consola ejecuta:
uv venv
uv pip install "mcp[cli]"
uv pip install fastmcp
uv pip install psycopg2-binary
