# MCP101 Project

Este proyecto es un ejemplo de servidor y cliente usando MCP (Model Context Protocol) para operaciones financieras y utilidades.

## Estructura
- `finance_client.py`: Cliente que se conecta al servidor MCP y ejecuta herramientas financieras.
- `finance_server.py`: Servidor MCP con herramientas financieras (debes agregarlo si no existe).
- `server.py`: Servidor MCP de ejemplo con herramientas simples.
- `mcp/`: Código fuente de la librería MCP (si es propio o personalizado).
- `tests/`: Pruebas automáticas.

## Requisitos
- Python 3.8+
- Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Uso
Ejecuta el servidor y el cliente en terminales separadas:

```bash
python finance_server.py
python finance_client.py
```

## Pruebas
Coloca tus pruebas en la carpeta `tests/` y ejecútalas con:

```bash
python -m unittest discover tests
```

# mcp-arena-25
Proyecto de ejemplo MCP para operaciones financieras y utilidades.
