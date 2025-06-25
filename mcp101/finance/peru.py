# Funciones específicas para finanzas en Perú

class BVLParameters:
    """Parámetros básicos para la Bolsa de Valores de Lima (BVL)."""
    def __init__(self, ticker: str, nombre: str, sector: str, moneda: str = "PEN"):
        self.ticker = ticker  # Símbolo de la acción
        self.nombre = nombre  # Nombre de la empresa
        self.sector = sector  # Sector económico
        self.moneda = moneda  # Moneda de cotización (por defecto PEN)

    def __repr__(self):
        return f"<BVLParameters {self.ticker} - {self.nombre} ({self.sector}) [{self.moneda}]>"

# Ejemplo de función para interactuar con bolsas locales

def obtener_info_bvl(ticker: str) -> BVLParameters:
    """Devuelve parámetros básicos de una acción de la BVL (simulado)."""
    # Aquí se podría conectar a una API real o base de datos
    ejemplos = {
        "CVERDEC1": BVLParameters("CVERDEC1", "Cementos Pacasmayo", "Construcción"),
        "ALICORC1": BVLParameters("ALICORC1", "Alicorp S.A.A.", "Consumo Masivo"),
        "CREDITC1": BVLParameters("CREDITC1", "Credicorp Ltd.", "Financiero"),
    }
    return ejemplos.get(ticker, BVLParameters(ticker, "Desconocido", "Desconocido"))

# Puedes agregar más funciones para interactuar con otras bolsas locales aquí.
def calcular_rentabilidad(ticker: str, precio_inicial: float, precio_final: float) -> float:
    """Calcula la rentabilidad de una acción dada su cotización inicial y final."""
    if precio_inicial <= 0:
        raise ValueError("El precio inicial debe ser mayor que cero.")
    rentabilidad = (precio_final - precio_inicial) / precio_inicial * 100
    return round(rentabilidad, 2)

def obtener_precio_accion(ticker: str) -> float:
    """Simula la obtención del precio actual de una acción (simulado)."""
    # Aquí se podría conectar a una API real o base de datos
    precios_simulados = {
        "CVERDEC1": 5.50,
        "ALICORC1": 10.20,
        "CREDITC1": 200.00,
    }
    return precios_simulados.get(ticker, 0.0)  # Retorna 0.0 si no se encuentra el ticker
def obtener_sector(ticker: str) -> str:
    """Devuelve el sector económico de una acción (simulado)."""
    # Aquí se podría conectar a una API real o base de datos
    sectores_simulados = {
        "CVERDEC1": "Construcción",
        "ALICORC1": "Consumo Masivo",
        "CREDITC1": "Financiero",
    }
    return sectores_simulados.get(ticker, "Desconocido")  # Retorna "Desconocido" si no se encuentra el ticker
def obtener_moneda(ticker: str) -> str:
    """Devuelve la moneda de cotización de una acción (simulado)."""
    # Aquí se podría conectar a una API real o base de datos
    monedas_simuladas = {
        "CVERDEC1": "PEN",
        "ALICORC1": "PEN",
        "CREDITC1": "USD",
    }
    return monedas_simuladas.get(ticker, "PEN")  # Retorna "PEN" si no se encuentra el ticker

def ejemplo_uso():
    print("--- Ejemplo de uso de finanzas BVL Perú ---")
    ticker = "CVERDEC1"
    info = obtener_info_bvl(ticker)
    print(f"Información básica: {info}")
    precio = obtener_precio_accion(ticker)
    print(f"Precio actual de {ticker}: S/ {precio}")
    sector = obtener_sector(ticker)
    print(f"Sector: {sector}")
    moneda = obtener_moneda(ticker)
    print(f"Moneda: {moneda}")
    # Simular rentabilidad
    precio_inicial = 4.80
    precio_final = precio
    rentabilidad = calcular_rentabilidad(ticker, precio_inicial, precio_final)
    print(f"Rentabilidad desde S/ {precio_inicial} hasta S/ {precio_final}: {rentabilidad}%")

if __name__ == "__main__":
    ejemplo_uso()