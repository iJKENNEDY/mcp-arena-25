# Ejemplos Medium MCP101

Este directorio contiene ejemplos de uso intermedio para la arquitectura MCP101, mostrando cómo integrar y orquestar herramientas MCP en flujos de trabajo más complejos.

## Estructura del Directorio

```
examples-medium/
│
├── multi_tool_orchestrator.py   # Orquestador de múltiples herramientas MCP
├── ...                          # Otros ejemplos de integración MCP
```

## Descripción de Archivos

- **multi_tool_orchestrator.py**: Ejemplo de cómo definir y ejecutar flujos de trabajo que combinan varias herramientas MCP, incluyendo lógica para reemplazo de parámetros y ejecución asíncrona.

## Requisitos

- Python 3.8+
- Instalar dependencias desde el directorio raíz del proyecto:

```bash
pip install -r ../../requirements.txt
```

## Ejecución de Ejemplos

Puedes ejecutar los scripts directamente usando Python:

```bash
python multi_tool_orchestrator.py
```

## Notas

- Estos ejemplos están diseñados para ilustrar patrones de orquestación y modularidad recomendados en MCP101.
- Modifica los flujos de trabajo y herramientas según tus necesidades para experimentar con la arquitectura MCP.

---
