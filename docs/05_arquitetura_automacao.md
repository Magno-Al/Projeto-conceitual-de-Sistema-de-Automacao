# Arquitetura de Automação — Planta de 2 Tanques

**Projeto:** Automação de Planta de 2 Tanques  
**Disciplina:** Automação Industrial  
**Modelo de referência:** ISA-95 / Pirâmide de Automação

---

## 1. Visão Geral do Sistema

O sistema implementa automação em 3 camadas integradas por comunicação Modbus TCP/IP:

```
┌─────────────────────────────────────────────────────────────────┐
│  NÍVEL 3 — SUPERVISÓRIO (MES/SCADA)                             │
│  SCADA Python/PySide6 — Monitoramento, Controle e Supervisão    │
│  Endereço: 127.0.0.1:5020 (cliente Modbus TCP)                  │
└────────────────────────┬────────────────────────────────────────┘
                         │ Modbus TCP/IP
                         │ (porta 5020)
┌────────────────────────┴────────────────────────────────────────┐
│  NÍVEL 2 — CONTROLE (CLP)                                       │
│  OpenPLC Runtime v4 — Lógica Ladder, Malhas de Controle         │
│  Servidor Modbus: :5020 (para SCADA)                            │
│  Cliente Modbus: :502  (para Factory I/O)                       │
└────────────────────────┬────────────────────────────────────────┘
                         │ Modbus TCP/IP
                         │ (porta 502)
┌────────────────────────┴────────────────────────────────────────┐
│  NÍVEL 1 — CAMPO / SIMULAÇÃO                                    │
│  Factory I/O — Simulador 3D da Planta (Servidor Modbus :502)    │
│  Sensores: LT-101, LT-201, FT-101                               │
│  Atuadores: FCV-101, FCV-102, FCV-201, FCV-202                  │
│  Botoeiras: HS-101/102, ZSL-101, HS-201/202, ZSL-201            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Fluxo de Dados Detalhado

### 2.1 Fluxo de Leitura (Sensores → SCADA)

```
Factory I/O           OpenPLC v4                    SCADA
(Servidor :502)       (Mestre :502 / Servidor :5020) (Cliente :5020)
─────────────         ──────────────────────────────  ───────────────

LT-101 (raw)   ──FC4→  %IW0 (nivel_t1)    ──FC4→   ModbusWorker
LT-201 (raw)   ──FC4→  %IW4 (nivel_t2)    ──FC4→   polling 200 ms
FT-101 (raw)   ──FC4→  %IW1 (vazao_t1)    ──FC4→   → values_updated
                                                      signal (Qt)
FCV-101 pos    ──FC3→  %QW0 (valv_ent_t1) ──FC3→       │
FCV-102 pos    ──FC3→  %QW1 (valv_sai_t1) ──FC3→       │
FCV-201 pos    ──FC3→  %QW4 (valv_ent_t2) ──FC3→       ▼
FCV-202 pos    ──FC3→  %QW5 (valv_sai_t2) ──FC3→   SynopticWidget
                                                    ManualPanel
HS-101 (NA)    ──FC2→  %IX0.0             ──FC2→   TagTable
HS-102 (NF)    ──FC2→  %IX0.1             ──FC2→   TrendWidget
ZSL-101 (NF)   ──FC2→  %IX0.2             ──FC2→   ProcessEngine
HS-201 (NA)    ──FC2→  %IX0.4             ──FC2→
HS-202 (NF)    ──FC2→  %IX0.5             ──FC2→
ZSL-201 (NF)   ──FC2→  %IX0.6             ──FC2→

XL-101 led     ──FC1→  %QX0.0             ──FC1→   SynopticWidget
XL-201 led     ──FC1→  %QX0.2             ──FC1→   (LEDs animados)
```

### 2.2 Fluxo de Escrita (SCADA → CLP → Atuadores)

```
SCADA (ProcessEngine / ManualPanel)
        │
        │  coil_command(address, bool)
        ▼
ModbusWorker.write_coil()
        │
        │  FC5 → Coils 16–19 no OpenPLC
        ▼
OpenPLC %QX2.0 = cmd_fill_t1   ──► Ladder: OR(led_start, cmd_fill) → SEL → %QW0 (FCV-101)
OpenPLC %QX2.1 = cmd_drain_t1  ──► Ladder: OR(NC_emerg, cmd_drain) → SEL → %QW1 (FCV-102)
OpenPLC %QX2.2 = cmd_fill_t2   ──► Ladder: OR(led_start, cmd_fill) → SEL → %QW4 (FCV-201)
OpenPLC %QX2.3 = cmd_drain_t2  ──► Ladder: OR(NC_emerg, cmd_drain) → SEL → %QW5 (FCV-202)
        │
        │  FC16 → Holding Registers do Factory I/O
        ▼
Factory I/O recebe posição das válvulas (0–1000) e simula a física dos tanques
```

---

## 3. Arquitetura de Software (SCADA)

```
app.py  ──────────────────────────────────────────────────────
│                                                             │
│  MainWindow (PySide6 QMainWindow)                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Barra de conexão: host / porta / btn conectar        │  │
│  │                                                        │  │
│  │  SynopticWidget ── QPainter ── animação em tempo real  │  │
│  │                                                        │  │
│  │  QTabWidget                                            │  │
│  │  ├── [Controle]                                        │  │
│  │  │   ├── ManualPanel (Encher/Pausar/Esvaziar por T)    │  │
│  │  │   └── AutoPanel  (alvo + tempo + start/stop)        │  │
│  │  ├── [Tags]    TagTable (tabela de todas as tags)       │  │
│  │  └── [Tendência] TrendWidget (QtCharts, 300 amostras)  │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ModbusWorker (QThread)                                     │
│  ├── polling 200 ms → values_updated(dict)                  │
│  ├── write_coil(addr, bool) → fila thread-safe              │
│  └── connection_changed(bool, msg)                          │
│                                                             │
│  ProcessEngine (QObject)                                    │
│  ├── Estados: IDLE→FILL_T1→HOLD_T1→DRAIN_T1_FILL_T2        │
│  │           →HOLD_T2→DRAIN_T2→DONE                        │
│  ├── update_values(dict) ← ModbusWorker                     │
│  └── coil_command(addr, bool) → ModbusWorker               │
└─────────────────────────────────────────────────────────────
```

---

## 4. Diagrama de Comunicação (Redes)

```
                    REDE LOCAL (localhost / 127.0.0.1)
                    ─────────────────────────────────

  ┌──────────────┐    Modbus TCP     ┌──────────────────────┐
  │  Factory I/O │◄──────:502────────│   OpenPLC Runtime v4 │
  │  (Servidor)  │                   │   (Mestre p/ F.IO)   │
  └──────────────┘                   │   (Servidor p/ SCADA)│
                                     └──────────┬───────────┘
                                                │
                                           Modbus TCP
                                              :5020
                                                │
                                     ┌──────────┴───────────┐
                                     │   SCADA Python        │
                                     │   (Cliente Modbus)    │
                                     │   Polling 200 ms      │
                                     └──────────────────────┘

  Protocolo: Modbus TCP/IP
  Versão: Modbus Application Protocol v1.1b3
  Library SCADA: pymodbus 3.7.x
  Unit ID: 1 (ambas as conexões)
```

---

## 5. Descrição das Camadas (Pirâmide ISA-95)

### Nível 0 — Processo Físico
Planta simulada no **Factory I/O** com dois tanques, válvulas proporcionais (0–1000), sensores de nível e botoeiras de operação local.

### Nível 1 — Instrumentação de Campo
Sensores analógicos (LT-101, LT-201, FT-101) e atuadores (FCV-101 a FCV-202) integrados ao Factory I/O. Comunicação via **Modbus TCP servidor porta 502**.

### Nível 2 — Controle (CLP)
**OpenPLC Runtime v4** executando programa ladder com:
- **Circuitos de selo** (start/stop/emergência) por tanque
- **Lógica de válvulas** com OR entre comandos locais e SCADA
- **Mestre Modbus** para leitura do Factory I/O a cada 100 ms
- **Servidor Modbus** porta 5020 para o SCADA

### Nível 3 — Supervisório (SCADA)
Aplicação **Python/PySide6** com:
- Interface gráfica animada (sinótico, gráfico de tendência)
- Controle manual e automático
- Polling Modbus a cada 200 ms
- Processo automático sequencial (máquina de estados)

### Nível 4+ — MES / ERP
Fora do escopo deste trabalho prático.

---

## 6. Tecnologias Utilizadas

| Componente | Tecnologia | Versão |
|------------|------------|--------|
| Simulador 3D | Factory I/O | v3/v4 |
| CLP (software) | OpenPLC Runtime v4 | v4.x |
| Linguagem CLP | Ladder Diagram (LD) — IEC 61131-3 | — |
| Interface SCADA | Python + PySide6 | 6.11+ |
| Protocolo | Modbus TCP/IP | RFC 1014 |
| Biblioteca Modbus | pymodbus | 3.7.x |
| SO (CLP + SCADA) | Windows 11 | 22H2+ |
| Comunicação | TCP/IP (localhost) | IPv4 |
