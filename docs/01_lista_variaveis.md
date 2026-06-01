# Lista de Variáveis de Processo e Variáveis Manipuláveis

**Projeto:** Automação de Planta de 2 Tanques  
**Disciplina:** Automação Industrial  
**Simulador:** Factory I/O | Controlador: OpenPLC v4 | Supervisório: SCADA Python/PySide6

---

## 1. Variáveis de Processo (Medidas)

São as grandezas físicas monitoradas continuamente pelos instrumentos de campo e lidas pelo sistema de controle via Modbus TCP.

| # | Tag ISA | Nome Lógico | Descrição | Tipo IEC | Endereço Modbus | Unidade | Range |
|---|---------|-------------|-----------|----------|-----------------|---------|-------|
| 1 | **LT-101** | `nivel_t1` | Nível do Tanque 1 | `%IW0` | IR 0 (FC4) | cru (0–1000) | 0 – 1000 |
| 2 | **LT-201** | `nivel_t2` | Nível do Tanque 2 | `%IW4` | IR 4 (FC4) | cru (0–1000) | 0 – 1000 |
| 3 | **FT-101** | `vazao_t1` | Vazão de entrada Tanque 1 | `%IW1` | IR 1 (FC4) | cru | 0 – 1000 |
| 4 | **ZT-101** | `valv_entrada_t1` | Posição válvula entrada T1 | `%QW0` | HR 0 (FC3) | 0–1000 | 0 – 1000 |
| 5 | **ZT-102** | `valv_saida_t1` | Posição válvula saída T1 | `%QW1` | HR 1 (FC3) | 0–1000 | 0 – 1000 |
| 6 | **ZT-201** | `valv_entrada_t2` | Posição válvula entrada T2 | `%QW4` | HR 4 (FC3) | 0–1000 | 0 – 1000 |
| 7 | **ZT-202** | `valv_saida_t2` | Posição válvula saída T2 | `%QW5` | HR 5 (FC3) | 0–1000 | 0 – 1000 |

---

## 2. Variáveis Manipuláveis (Saídas de Controle)

São as grandezas sobre as quais o sistema de controle (SCADA/PLC) atua para modificar o comportamento do processo.

| # | Tag ISA | Nome Lógico | Descrição | Tipo IEC | Endereço Modbus | Valores |
|---|---------|-------------|-----------|----------|-----------------|---------|
| 8 | **FCV-101** | `cmd_fill_t1` | Comando abertura válvula entrada T1 | `%QX2.0` | Coil 16 (FC5) | 0 = fechado / 1 = aberto |
| 9 | **FCV-102** | `cmd_drain_t1` | Comando abertura válvula saída T1 | `%QX2.1` | Coil 17 (FC5) | 0 = fechado / 1 = aberto |
| 10 | **FCV-201** | `cmd_fill_t2` | Comando abertura válvula entrada T2 | `%QX2.2` | Coil 18 (FC5) | 0 = fechado / 1 = aberto |
| 11 | **FCV-202** | `cmd_drain_t2` | Comando abertura válvula saída T2 | `%QX2.3` | Coil 19 (FC5) | 0 = fechado / 1 = aberto |

---

## 3. Variáveis de Status e Intertravamento

| # | Tag ISA | Nome Lógico | Descrição | Tipo IEC | Endereço Modbus | Tipo |
|---|---------|-------------|-----------|----------|-----------------|------|
| 12 | **HS-101** | `bt_start_t1` | Botão START Tanque 1 (NA) | `%IX0.0` | DI 0 (FC2) | Digital |
| 13 | **HS-102** | `bt_stop_t1` | Botão STOP Tanque 1 (NF) | `%IX0.1` | DI 1 (FC2) | Digital |
| 14 | **ZSL-101** | `bt_emerg_t1` | Botão EMERGÊNCIA T1 (NF) | `%IX0.2` | DI 2 (FC2) | Digital |
| 15 | **HS-201** | `bt_start_t2` | Botão START Tanque 2 (NA) | `%IX0.4` | DI 4 (FC2) | Digital |
| 16 | **HS-202** | `bt_stop_t2` | Botão STOP Tanque 2 (NF) | `%IX0.5` | DI 5 (FC2) | Digital |
| 17 | **ZSL-201** | `bt_emerg_t2` | Botão EMERGÊNCIA T2 (NF) | `%IX0.6` | DI 6 (FC2) | Digital |
| 18 | **XL-101** | `led_start_t1` | Indicador luminoso START T1 | `%QX0.0` | Coil 0 (FC1) | Digital |
| 19 | **XL-201** | `led_start_t2` | Indicador luminoso START T2 | `%QX0.2` | Coil 2 (FC1) | Digital |

---

## 4. Observações Técnicas

- **Protocolo:** Modbus TCP/IP (cliente SCADA → servidor OpenPLC porta 5020)
- **Endereçamento:** padrão OpenPLC — `%IW` → Input Registers FC4; `%QW` → Holding Registers FC3; `%IX` → Discrete Inputs FC2; `%QX` → Coils FC1/FC5
- **Escala de nível:** 0 (tanque vazio) a 1000 (tanque cheio); conversão para % feita no SCADA via `config.raw_to_percent()`
- **Abertura de válvula:** 0 (completamente fechada) a 1000 (completamente aberta); valor analógico enviado ao Factory I/O
- **Botões NF (Normalmente Fechados):** valor lógico 1 = circuito fechado = botão não pressionado
