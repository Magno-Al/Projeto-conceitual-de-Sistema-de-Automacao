# Matriz Causa-e-Efeito

**Projeto:** Automação de Planta de 2 Tanques  
**Norma de referência:** ISA 84 / IEC 61511

---

## Legenda

| Símbolo | Significado |
|---------|-------------|
| **A** | Abre / Liga / Ativa |
| **F** | Fecha / Desliga / Desativa |
| **Z** | Zera / Reseta |
| **—** | Sem efeito |
| **↑** | Inibe ação (travamento) |

---

## Matriz Causa → Efeito

| # | CAUSA (Evento / Condição) | FCV-101 (entrada T1) | FCV-102 (saída T1) | FCV-201 (entrada T2) | FCV-202 (saída T2) | XL-101 (LED start T1) | XL-201 (LED start T2) | Alarme SCADA |
|---|---------------------------|----------------------|---------------------|----------------------|---------------------|------------------------|------------------------|--------------|
| 1 | **HS-101** bt_start_t1 pressionado (NA → 1) | **A** (abre entrada T1) | F | — | — | **Liga** | — | — |
| 2 | **HS-102** bt_stop_t1 pressionado (NF → 0) | **F** (fecha entrada T1) | F | — | — | **Desliga** | — | — |
| 3 | **ZSL-101** bt_emerg_t1 pressionado (NF → 0) | **F** | **A** (abre saída T1, esvazia) | — | — | **Desliga** | — | **EMERG T1** |
| 4 | **HS-201** bt_start_t2 pressionado (NA → 1) | — | — | **A** | F | — | **Liga** | — |
| 5 | **HS-202** bt_stop_t2 pressionado (NF → 0) | — | — | **F** | F | — | **Desliga** | — |
| 6 | **ZSL-201** bt_emerg_t2 pressionado (NF → 0) | — | — | **F** | **A** | — | **Desliga** | **EMERG T2** |
| 7 | **cmd_fill_t1** = 1 (SCADA → coil 16) | **A** | F | — | — | — | — | — |
| 8 | **cmd_drain_t1** = 1 (SCADA → coil 17) | F | **A** | — | — | — | — | — |
| 9 | **cmd_fill_t2** = 1 (SCADA → coil 18) | — | — | **A** | F | — | — | — |
| 10 | **cmd_drain_t2** = 1 (SCADA → coil 19) | — | — | F | **A** | — | — | — |
| 11 | **LT-101** nível T1 ≥ alvo (ProcessEngine) | **F** (para enchimento) | — | — | — | — | — | — |
| 12 | **LT-201** nível T2 ≥ alvo (ProcessEngine) | — | — | **F** | — | — | — | — |
| 13 | **Parada segura** (stop() engine / desconexão) | **F** | **F** | **F** | **F** | — | — | **Desconectado** |
| 14 | **Falha Modbus** (timeout > 1 s) | — (mantém estado) | — | — | — | — | — | **FALHA COMM** |

---

## Sequência do Processo Automático (ProcessEngine)

| Estado | Ação SCADA (comandos) | Condição de saída | Próximo estado |
|--------|----------------------|-------------------|----------------|
| **IDLE** | Todos os comandos = 0 | Operador aciona Start | FILL_T1 |
| **FILL_T1** | cmd_fill_t1 = 1 | nivel_t1 ≥ alvo_t1 | HOLD_T1 |
| **HOLD_T1** | cmd_fill_t1 = 0 (pausa) | tempo_t1 expirado | DRAIN_T1_FILL_T2 |
| **DRAIN_T1_FILL_T2** | cmd_drain_t1 = 1, cmd_fill_t2 = 1 | nivel_t2 ≥ alvo_t2 | HOLD_T2 |
| **HOLD_T2** | cmd_drain_t1 = 0, cmd_fill_t2 = 0 | tempo_t2 expirado | DRAIN_T2 |
| **DRAIN_T2** | cmd_drain_t2 = 1 | nivel_t2 ≤ 0 | DONE |
| **DONE** | Todos os comandos = 0 | — | IDLE |
| **PARADO** | Todos os comandos = 0 | Operador aciona Stop | IDLE |

---

## Intertravamentos (Interlocks)

| # | Condição de Intertravamento | Efeito |
|---|----------------------------|--------|
| IL-01 | bt_emerg_t1 = 0 (pressionado) | FCV-101 fecha, FCV-102 abre (esvazia T1 por segurança) |
| IL-02 | bt_emerg_t2 = 0 (pressionado) | FCV-201 fecha, FCV-202 abre (esvazia T2 por segurança) |
| IL-03 | bt_stop_t1 = 0 (pressionado) | FCV-101 fecha (memória de selo desligada) |
| IL-04 | bt_stop_t2 = 0 (pressionado) | FCV-201 fecha (memória de selo desligada) |
| IL-05 | Perda de conexão Modbus (SCADA) | ProcessEngine emite stop() — todos os comandos zerados |
| IL-06 | cmd_fill e cmd_drain simultâneos | Ladder: OR de comandos — ambos recebidos, abre apenas o comandado (OR com prioridade de emergência) |
