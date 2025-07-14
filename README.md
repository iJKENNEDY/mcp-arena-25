
# MCP101 Project

Este proyecto es un ejemplo de arquitectura MCP (Model Context Protocol) para operaciones financieras y utilidades.

## Estructura del Proyecto

```
mcp101/
│
├── server/                # Servidores MCP (exponen herramientas)
│   └── main_server.py
│
├── client/                # Clientes MCP
│   └── finance_client.py
│
├── finance/               # Lógica financiera (modelos y cálculos)
│   └── peru.py
│
├── utils/                 # Utilidades generales
│   └── helpers.py
│
├── tests/                 # Pruebas automáticas
│   └── test_finance.py
│
└── requirements.txt       # Dependencias del proyecto
```

## Requisitos

- Python 3.8+
- Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Uso

1. Ejecuta el servidor MCP en una terminal:
    ```bash
    python -m mcp101.server.main_server
    ```
2. Ejecuta el cliente en otra terminal:
    ```bash
    python -m mcp101.client.finance_client
    ```

## Pruebas

Ejecuta las pruebas automáticas con:

```bash
python -m unittest discover tests
```

## Descripción de Carpetas

- **server/**: Servidores MCP que exponen las herramientas y recursos.
- **client/**: Clientes que consumen las herramientas MCP.
- **finance/**: Lógica de negocio y modelos financieros.
- **utils/**: Funciones auxiliares y utilidades.
- **tests/**: Pruebas unitarias y de integración.

## Contribución

1. Haz un fork del repositorio.
2. Crea una rama para tu feature o fix.
3. Realiza tus cambios y agrega pruebas.
4. Haz un pull request.

---

Proyecto de ejemplo MCP para operaciones financieras