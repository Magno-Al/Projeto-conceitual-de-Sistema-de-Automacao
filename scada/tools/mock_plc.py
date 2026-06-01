"""Servidor Modbus de simulação (mock do OpenPLC + Factory I/O).

Permite desenvolver e validar o SCADA inteiramente no Linux, sem Factory I/O
(que é Windows-only). Emula:
  - as coils de comando que o SCADA escreve (16..20);
  - a lógica das válvulas (entrada/saída seguem os comandos);
  - a física dos tanques (nível sobe ao encher, desce ao esvaziar).

Uso:
    cd scada && python tools/mock_plc.py [porta]
"""

import os
import sys
import threading
import time

# permite importar config/tags da raiz do projeto scada/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config  # noqa: E402

from pymodbus.datastore import (  # noqa: E402
    ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext,
)
from pymodbus.server import StartTcpServer  # noqa: E402

# Função-código -> store (pymodbus): 1=coils, 2=discrete inputs, 3=holding, 4=input
FC_COIL, FC_DI, FC_HR, FC_IR = 1, 2, 3, 4

FILL_RATE = max(1, config.LEVEL_RAW_MAX // 50)   # ~5 s para encher
DRAIN_RATE = max(1, config.LEVEL_RAW_MAX // 33)  # ~3 s para esvaziar
TICK = 0.1


def build_context():
    block = lambda: ModbusSequentialDataBlock(0, [0] * 64)
    store = ModbusSlaveContext(
        di=block(), co=block(), hr=block(), ir=block(), zero_mode=True,
    )
    ctx = ModbusServerContext(slaves={config.MODBUS_UNIT_ID: store}, single=False)
    # emergências são NF (1 = não pressionado / OK)
    store.setValues(FC_DI, 2, [1])  # bt_emerg_t1
    store.setValues(FC_DI, 6, [1])  # bt_emerg_t2
    return ctx, store


def simulate(store):
    while True:
        coils = store.getValues(FC_COIL, 0, 24)
        cmd_fill_t1, cmd_drain_t1 = coils[16], coils[17]
        cmd_fill_t2, cmd_drain_t2 = coils[18], coils[19]

        irs = store.getValues(FC_IR, 0, 6)
        n1, n2 = irs[0], irs[4]

        if cmd_fill_t1:
            n1 += FILL_RATE
        if cmd_drain_t1:
            n1 -= DRAIN_RATE
        if cmd_fill_t2:
            n2 += FILL_RATE
        if cmd_drain_t2:
            n2 -= DRAIN_RATE
        n1 = max(0, min(config.LEVEL_RAW_MAX, n1))
        n2 = max(0, min(config.LEVEL_RAW_MAX, n2))

        # input registers: níveis (%IW0, %IW4)
        store.setValues(FC_IR, 0, [n1])
        store.setValues(FC_IR, 4, [n2])

        # holding registers: válvulas + display (%QW0..2, %QW4..6)
        vo = config.VALVE_OPEN
        store.setValues(FC_HR, 0, [vo if cmd_fill_t1 else 0,
                                   vo if cmd_drain_t1 else 0, n1])
        store.setValues(FC_HR, 4, [vo if cmd_fill_t2 else 0,
                                   vo if cmd_drain_t2 else 0, n2])

        # leds de start (%QX0.0, %QX0.2) refletem enchimento
        store.setValues(FC_COIL, 0, [1 if cmd_fill_t1 else 0, 0,
                                     1 if cmd_fill_t2 else 0])
        time.sleep(TICK)


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else config.MODBUS_PORT
    ctx, store = build_context()
    t = threading.Thread(target=simulate, args=(store,), daemon=True)
    t.start()
    print(f"Mock PLC/Modbus em 0.0.0.0:{port} (unit {config.MODBUS_UNIT_ID})")
    print("Ctrl+C para sair.")
    StartTcpServer(context=ctx, address=("0.0.0.0", port))


if __name__ == "__main__":
    main()
