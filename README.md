Descarga UV:<br>
https://docs.astral.sh/uv/getting-started/installation/#standalone-installer

En Consola Ejecuta:<br>
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

En la carpeta del proyecto python x consola ejecuta:<br>
uv venv<br>
uv pip install "mcp[cli]"<br>
uv pip install fastmcp<br>
uv pip install psycopg2-binary
