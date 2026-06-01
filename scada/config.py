"""Configuração central do SCADA.

Todos os parâmetros ajustáveis ficam aqui para facilitar a calibração no
laboratório (porta do servidor Modbus do OpenPLC, escala dos níveis, etc.).
"""

# ---------------------------------------------------------------------------
# Conexão Modbus TCP com o servidor do OpenPLC
# ---------------------------------------------------------------------------
# Atenção: o Factory I/O ocupa a porta 502 (ele é o servidor que o OpenPLC,
# como mestre, fica lendo). Portanto o *servidor Modbus do próprio OpenPLC*
# (onde este SCADA conecta) normalmente está em outra porta. Confira em
# OpenPLC -> Settings -> Modbus Server e ajuste abaixo.
MODBUS_HOST = "127.0.0.1"
MODBUS_PORT = 502          # ajuste p/ a porta do servidor do OpenPLC (ex.: 1502)
MODBUS_UNIT_ID = 1         # slave/unit id do OpenPLC
MODBUS_TIMEOUT = 1.0       # segundos

# Período de polling da camada Modbus (ms)
POLL_INTERVAL_MS = 200

# ---------------------------------------------------------------------------
# Escala dos sensores de nível (valor cru do Modbus -> porcentagem)
# ---------------------------------------------------------------------------
# Os níveis chegam como INT cru vindo do Factory I/O. Após observar o range
# real no laboratório, ajuste LEVEL_RAW_MIN/MAX para a conversão cru -> %.
LEVEL_RAW_MIN = 0
LEVEL_RAW_MAX = 10000      # valor cru correspondente a 100% (calibrar!)


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


# ---------------------------------------------------------------------------
# Valor de abertura total de válvula (usado pelo ladder / mock): 0..1000
# ---------------------------------------------------------------------------
VALVE_OPEN = 1000
