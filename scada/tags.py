from dataclasses import dataclass

DISCRETE_INPUT = "di"    
COIL = "coil"             
INPUT_REGISTER = "ir"     
HOLDING_REGISTER = "hr"  


@dataclass(frozen=True)
class Tag:
    name: str        
    iec: str      
    kind: str         
    address: int        
    writable: bool    
    unit: str = ""      
    description: str = ""


NIVEL_T1 = Tag("nivel_t1", "%IW0", INPUT_REGISTER, 0, False, "cru", "Nível do tanque 1")
VAZAO_T1 = Tag("vazao_t1", "%IW1", INPUT_REGISTER, 1, False, "cru", "Vazão T1")
NIVEL_T2 = Tag("nivel_t2", "%IW4", INPUT_REGISTER, 4, False, "cru", "Nível do tanque 2")

VALV_ENTRADA_T1 = Tag("valv_entrada_t1", "%QW0", HOLDING_REGISTER, 0, False, "0-1000", "Válvula de entrada T1")
VALV_SAIDA_T1 = Tag("valv_saida_t1", "%QW1", HOLDING_REGISTER, 1, False, "0-1000", "Válvula de saída T1")
DISPLAY_T1 = Tag("display_t1", "%QW2", HOLDING_REGISTER, 2, False, "cru", "Display nível T1")
VALV_ENTRADA_T2 = Tag("valv_entrada_t2", "%QW4", HOLDING_REGISTER, 4, False, "0-1000", "Válvula de entrada T2")
VALV_SAIDA_T2 = Tag("valv_saida_t2", "%QW5", HOLDING_REGISTER, 5, False, "0-1000", "Válvula de saída T2")
DISPLAY_T2 = Tag("display_t2", "%QW6", HOLDING_REGISTER, 6, False, "cru", "Display nível T2")

LED_START_T1 = Tag("led_start_t1", "%QX0.0", COIL, 0, False, "", "LED start T1 (selo ligado)")
LED_STOP_T1 = Tag("led_stop_t1", "%QX0.1", COIL, 1, False, "", "LED stop T1")
LED_START_T2 = Tag("led_start_t2", "%QX0.2", COIL, 2, False, "", "LED start T2 (selo ligado)")

BT_START_T1 = Tag("bt_start_t1", "%IX0.0", DISCRETE_INPUT, 0, False, "", "Botão start T1")
BT_STOP_T1 = Tag("bt_stop_t1", "%IX0.1", DISCRETE_INPUT, 1, False, "", "Botão stop T1 (NF)")
BT_EMERG_T1 = Tag("bt_emerg_t1", "%IX0.2", DISCRETE_INPUT, 2, False, "", "Botão emergência T1 (NF)")
BT_START_T2 = Tag("bt_start_t2", "%IX0.4", DISCRETE_INPUT, 4, False, "", "Botão start T2")
BT_STOP_T2 = Tag("bt_stop_t2", "%IX0.5", DISCRETE_INPUT, 5, False, "", "Botão stop T2 (NF)")
BT_EMERG_T2 = Tag("bt_emerg_t2", "%IX0.6", DISCRETE_INPUT, 6, False, "", "Botão emergência T2 (NF)")

CMD_FILL_T1 = Tag("cmd_fill_t1", "%QX2.0", COIL, 16, True, "", "Comando: abrir entrada T1")
CMD_DRAIN_T1 = Tag("cmd_drain_t1", "%QX2.1", COIL, 17, True, "", "Comando: abrir saída T1")
CMD_FILL_T2 = Tag("cmd_fill_t2", "%QX2.2", COIL, 18, True, "", "Comando: abrir entrada T2")
CMD_DRAIN_T2 = Tag("cmd_drain_t2", "%QX2.3", COIL, 19, True, "", "Comando: abrir saída T2")
CMD_REMOTE = Tag("cmd_remote", "%QX2.4", COIL, 20, True, "", "Comando: habilita modo remoto/auto")

ALL_TAGS = [
    NIVEL_T1, VAZAO_T1, NIVEL_T2,
    VALV_ENTRADA_T1, VALV_SAIDA_T1, DISPLAY_T1,
    VALV_ENTRADA_T2, VALV_SAIDA_T2, DISPLAY_T2,
    LED_START_T1, LED_STOP_T1, LED_START_T2,
    BT_START_T1, BT_STOP_T1, BT_EMERG_T1,
    BT_START_T2, BT_STOP_T2, BT_EMERG_T2,
    CMD_FILL_T1, CMD_DRAIN_T1, CMD_FILL_T2, CMD_DRAIN_T2, CMD_REMOTE,
]

BY_NAME = {t.name: t for t in ALL_TAGS}

# Coils
COMMAND_COILS = [CMD_FILL_T1, CMD_DRAIN_T1, CMD_FILL_T2, CMD_DRAIN_T2]
