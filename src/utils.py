import re
import logging

logger = logging.getLogger(__name__)

def clean_price(price_str: str) -> float:
    """
    Convierte strings como '£23.00' o '$ 23.00' a float 23.0.
    Retorna 0.0 si falla.
    """
    if not price_str:
        return 0.0
    # Extraer solo números y punto decimal
    clean_str = re.sub(r'[^\d.]', '', price_str)
    try:
        return float(clean_str)
    except ValueError:
        logger.warning(f"No se pudo convertir precio: {price_str}")
        return 0.0

def clean_stock(stock_str: str) -> int:
    if not stock_str: return 0
    numbers = re.findall(r'\d+', stock_str) # Buscará [22]
    if numbers:
        return int(numbers[0])
    return 0