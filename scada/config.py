MODBUS_HOST = "127.0.0.1"
MODBUS_PORT = 5020    
MODBUS_UNIT_ID = 1      
MODBUS_TIMEOUT = 1.0  

POLL_INTERVAL_MS = 200

LEVEL_RAW_MIN = 0
LEVEL_RAW_MAX = 1000 


def raw_to_percent(raw: int) -> float:
    """Converte o valor cru de nível para porcentagem (0-100)."""
    span = LEVEL_RAW_MAX - LEVEL_RAW_MIN
    if span <= 0:
        return 0.0
    pct = (raw - LEVEL_RAW_MIN) / span * 100.0
    return max(0.0, min(100.0, pct))


def percent_to_raw(pct: float) -> int:
    """Converte uma porcentagem (0-100) de volta para o valor cru."""
    span = LEVEL_RAW_MAX - LEVEL_RAW_MIN
    return int(LEVEL_RAW_MIN + (pct / 100.0) * span)

VALVE_OPEN = 1000
