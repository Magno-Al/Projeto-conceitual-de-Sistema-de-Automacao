# P&ID — Diagrama de Processo e Instrumentação

**Projeto:** Automação de Planta de 2 Tanques  
**Norma de referência:** ISA 5.1 / ANSI/ISA-5.1-2009  
**Revisão:** 1.0

---

## Legenda de Simbologia ISA

| Símbolo | Significado |
|---------|-------------|
| `( )` | Instrumento montado em campo |
| `(□)` | Instrumento montado no painel / CLP |
| `(◎)` | Instrumento montado no painel compartilhado (SCADA) |
| **L** | Nível (Level) |
| **F** | Vazão (Flow) |
| **Z** | Posição (Position) |
| **H** | Manual / Mão (Hand) |
| **T** | Transmissor |
| **C** | Controlador |
| **V** | Válvula (Valve) |
| **I** | Indicador |
| **A** | Alarme |
| **S** | Chave / Switch |
| **NF** | Normalmente Fechado |
| **NA** | Normalmente Aberto |
| `───` | Linha de processo |
| `- - -` | Sinal elétrico / Modbus |
| `═══` | Linha de sinal digital |

---

## Diagrama P&ID (ASCII)

```
                    FONTE DE ÁGUA
                         │
                         │ (linha de processo)
                         │
                    ┌────┴────┐
                    │ FT-101  │  ←── Transmissor de Vazão Entrada T1
                    └────┬────┘
                         │
                    ┌────┴────┐
                    │ FCV-101 │  ←── Válvula de Controle Entrada T1
                    │  (FO)   │      (Fail-Open: abre sob comando SCADA)
                    └────┬────┘
                         │
   HS-101 ──START        │        bt_emerg_t1 ──ZSL-101
   HS-102 ──STOP  ───────┤
                         │
   ╔═══════════════════════╗
   ║       TANQUE T1        ║
   ║                        ║
   ║   ┌──────────────┐     ║
   ║   │    LT-101    │     ║  ←── Transmissor de Nível T1
   ║   │  (0 – 100%)  │     ║
   ║   └──────────────┘     ║
   ║                        ║
   ╚═══════════════╤═════════╝
                   │
              ┌────┴────┐
              │ FCV-102 │  ←── Válvula de Controle Saída T1
              │  (FC)   │      (Fail-Close: fecha por padrão)
              └────┬────┘
                   │
                   │ (linha de transferência T1 → T2)
                   │
              ┌────┴────┐
              │ FCV-201 │  ←── Válvula de Controle Entrada T2
              │  (FO)   │
              └────┬────┘
                   │
   HS-201 ──START  │        bt_emerg_t2 ──ZSL-201
   HS-202 ──STOP ──┤
                   │
   ╔═══════════════════════╗
   ║       TANQUE T2        ║
   ║                        ║
   ║   ┌──────────────┐     ║
   ║   │    LT-201    │     ║  ←── Transmissor de Nível T2
   ║   │  (0 – 100%)  │     ║
   ║   └──────────────┘     ║
   ║                        ║
   ╚═══════════════╤═════════╝
                   │
              ┌────┴────┐
              │ FCV-202 │  ←── Válvula de Controle Saída T2
              │  (FC)   │
              └────┬────┘
                   │
                DESCARTE
```

---

## Malhas de Controle

```
  CAMPO                    CLP (OpenPLC v4)             SCADA (Python/PySide6)
  ─────                    ────────────────             ──────────────────────

  LT-101 ─── Modbus IR0 ──► %IW0 ──► Ladder ──► %QW0 ─── Modbus HR0 ──► FCV-101
  FT-101 ─── Modbus IR1 ──► %IW1      (lógica      %QW1 ─── Modbus HR1 ──► FCV-102
  LT-201 ─── Modbus IR4 ──► %IW4    de controle)   %QW4 ─── Modbus HR4 ──► FCV-201
                                                    %QW5 ─── Modbus HR5 ──► FCV-202

  HS-101 ─── Modbus DI0 ──► %IX0.0   SCADA lê:
  HS-102 ─── Modbus DI1 ──► %IX0.1   LT-101, LT-201, FT-101
  ZSL-101 ── Modbus DI2 ──► %IX0.2   ZT-101..202 (posição válvulas)
  HS-201 ─── Modbus DI4 ──► %IX0.4   XL-101, XL-201 (LEDs)
  HS-202 ─── Modbus DI5 ──► %IX0.5
  ZSL-201 ── Modbus DI6 ──► %IX0.6   SCADA escreve (coils 16–19):
                                      cmd_fill_t1 → FCV-101 via ladder
  XL-101 ◄── Modbus C0 ──── %QX0.0   cmd_drain_t1 → FCV-102 via ladder
  XL-201 ◄── Modbus C2 ──── %QX0.2   cmd_fill_t2 → FCV-201 via ladder
                                      cmd_drain_t2 → FCV-202 via ladder
```

---

## Lista de Instrumentos (Instrument Index)

| Tag | Descrição | Sinal | Localização | Protocolo |
|-----|-----------|-------|-------------|-----------|
| LT-101 | Transmissor de Nível Tanque 1 | Analógico 0–1000 | Campo (T1) | Modbus TCP IR0 |
| LT-201 | Transmissor de Nível Tanque 2 | Analógico 0–1000 | Campo (T2) | Modbus TCP IR4 |
| FT-101 | Transmissor de Vazão Entrada T1 | Analógico 0–1000 | Campo (linha T1) | Modbus TCP IR1 |
| FCV-101 | Válvula de Controle Entrada T1 | Analógico 0–1000 | Campo (linha T1) | Modbus TCP HR0 |
| FCV-102 | Válvula de Controle Saída T1 | Analógico 0–1000 | Campo (linha T1) | Modbus TCP HR1 |
| FCV-201 | Válvula de Controle Entrada T2 | Analógico 0–1000 | Campo (linha T2) | Modbus TCP HR4 |
| FCV-202 | Válvula de Controle Saída T2 | Analógico 0–1000 | Campo (linha T2) | Modbus TCP HR5 |
| HS-101 | Botão Start T1 (NA) | Digital | Painel local T1 | Modbus TCP DI0 |
| HS-102 | Botão Stop T1 (NF) | Digital | Painel local T1 | Modbus TCP DI1 |
| ZSL-101 | Botão Emergência T1 (NF) | Digital | Painel local T1 | Modbus TCP DI2 |
| HS-201 | Botão Start T2 (NA) | Digital | Painel local T2 | Modbus TCP DI4 |
| HS-202 | Botão Stop T2 (NF) | Digital | Painel local T2 | Modbus TCP DI5 |
| ZSL-201 | Botão Emergência T2 (NF) | Digital | Painel local T2 | Modbus TCP DI6 |
| XL-101 | Indicador Luminoso START T1 | Digital | Painel local T1 | Modbus TCP C0 |
| XL-201 | Indicador Luminoso START T2 | Digital | Painel local T2 | Modbus TCP C2 |
| PLC-001 | CLP OpenPLC Runtime v4 | — | Sala de controle | Modbus TCP :5020 |
| SCADA-001 | Sistema Supervisório Python/PySide6 | — | Sala de controle | Modbus TCP :5020 |
