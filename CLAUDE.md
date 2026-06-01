# CLAUDE.md

Guia do projeto para o Claude Code (e para humanos). Trabalho prático da
disciplina de **Automação Industrial**: automação de uma planta de 2 tanques.

## Visão geral

Planta de 2 tanques simulada no **Factory I/O**, controlada por **OpenPLC v4**
(ladder), com uma aplicação **SCADA** em Python/PySide6 para supervisão e
controle. Comunicação por **Modbus TCP**.

```
Factory I/O  <--Modbus TCP-->  OpenPLC v4 (ladder + servidor Modbus)  <--Modbus TCP-->  SCADA
 (servidor :502)               (mestre do Factory I/O; servidor p/ SCADA)               (cliente, este app)
```

- O OpenPLC é **mestre** do Factory I/O (porta 502) — ver `open-plc/devices/remote/FactoryIO.json`.
- O **servidor Modbus do próprio OpenPLC** (onde o SCADA conecta) costuma ficar
  em **outra porta** (a 502 já é do Factory I/O). Confirmar em OpenPLC → Settings.

## Estrutura do repositório

```
.
├── Requisitos do trabalho.pdf     requisitos da disciplina + doc técnica (mapa de variáveis)
├── factory-io/
│   └── tank-process.factoryio     cena do Factory I/O (2 tanques)
├── open-plc/                       projeto do OpenPLC (editor web v4)
│   ├── plc.xml                     POU em formato PLCopen
│   ├── pous/programs/main.ld       ladder (React-Flow JSON) — editar no OpenPLC Editor
│   ├── devices/remote/FactoryIO.json  config do OpenPLC como mestre do Factory I/O
│   ├── build/.../program.st        ST compilado (referência da lógica atual)
│   └── COMMAND_LAYER.md            ALTERAÇÕES no ladder p/ controle via SCADA (a aplicar)
└── scada/                          aplicação SCADA (Python/PySide6) — desenvolvida aqui
```

## Lógica atual do PLC (já feita e testada)

Por tanque: circuito de **selo** (start/stop/emergência) que aciona válvulas via
blocos `SEL` (0–1000). start → abre entrada (enche); stop → pausa; emergência →
abre saída (esvazia). Botões `bt_stop`/`bt_emerg` são **NF** (1 = não pressionado).

## Mapa Modbus (servidor do OpenPLC)

Endereçamento padrão OpenPLC: `%IX`→Discrete Input (FC2), `%QX`→Coil (FC1/5),
`%IW`→Input Register (FC4), `%QW`→Holding Register (FC3/16).

**Leitura:**

| Tag | IEC | Modbus | FC |
|---|---|---|---|
| nivel_t1 / vazao_t1 / nivel_t2 | %IW0 / %IW1 / %IW4 | IR 0 / 1 / 4 | 4 |
| valv_entrada/saida/display_t1 | %QW0 / %QW1 / %QW2 | HR 0 / 1 / 2 | 3 |
| valv_entrada/saida/display_t2 | %QW4 / %QW5 / %QW6 | HR 4 / 5 / 6 | 3 |
| led_start_t1 / led_stop_t1 / led_start_t2 | %QX0.0 / .1 / %QX0.2 | Coil 0 / 1 / 2 | 1 |
| bt_start/stop/emerg_t1 | %IX0.0 / .1 / .2 | DI 0 / 1 / 2 | 2 |
| bt_start/stop/emerg_t2 | %IX0.4 / .5 / .6 | DI 4 / 5 / 6 | 2 |

**Comando (coils livres que o SCADA escreve e o ladder lê — ver COMMAND_LAYER.md):**

| Tag | IEC | Coil | Função |
|---|---|---|---|
| cmd_fill_t1 / cmd_drain_t1 | %QX2.0 / .1 | 16 / 17 | entrada / saída T1 |
| cmd_fill_t2 / cmd_drain_t2 | %QX2.2 / .3 | 18 / 19 | entrada / saída T2 |
| cmd_remote (opcional) | %QX2.4 | 20 | habilita modo remoto |

> **Por que a camada de comando:** um cliente Modbus só escreve em coils/holding
> registers e não pode sobrescrever saídas que o ladder recalcula a cada scan.
> As coils ≥ 16 estão fora da faixa do Factory I/O (coils 0–15), então o ladder
> as lê como comando sem conflito, combinando-as (OR) com os botões físicos.

## Aplicação SCADA (`scada/`)

PySide6 + pymodbus. Arquitetura:

- `config.py` — host/porta Modbus, escala cru→% dos níveis, período de polling.
- `tags.py` — registro central das tags (fonte única de verdade do mapa Modbus).
- `plc/modbus_worker.py` — `QThread`: faz polling (~200 ms), emite snapshot
  (`values_updated`) e serializa escritas (fila). Detecta em runtime o kwarg de
  unidade do pymodbus (`slave`/`device_id`) para compatibilidade entre versões.
- `core/process_engine.py` — máquina de estados do processo automático:
  `FILL_T1 → HOLD_T1 → DRAIN_T1_FILL_T2 → HOLD_T2 → DRAIN_T2 → DONE`. Atua só
  pelas coils de comando (supervisão; controle real fica no PLC). `stop()` =
  parada segura (zera comandos).
- `ui/` — `main_window` (barra de conexão + abas), `synoptic_widget` (mímico
  animado via QPainter), `manual_panel` (Encher/Pausar/Esvaziar por tanque),
  `auto_panel` (4 parâmetros + start/stop), `tag_table`, `trend_widget` (QtCharts).
- `tools/mock_plc.py` — servidor Modbus que emula PLC + física dos tanques, para
  desenvolver/testar no Linux sem o Factory I/O (Windows-only).

### Sinais Qt (fluxo de dados)
`ModbusWorker.values_updated(dict)` → sinótico, painéis, tabela, tendência e
`ProcessEngine.update_values`. Comandos: `*.coil_command(addr, bool)` e
`ProcessEngine.coil_command` → `ModbusWorker.write_coil`.

## Como rodar

```bash
cd scada
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt        # PySide6, pymodbus>=3.5,<3.8

# Dev no Linux (sem Factory I/O):
python tools/mock_plc.py 15020         # terminal 1  (ajustar MODBUS_PORT=15020)
python app.py                          # terminal 2

# Setup real (Windows/lab): Factory I/O + OpenPLC rodando; ajustar host/porta e:
python app.py
```

> **pymodbus** está fixado em `>=3.5,<3.8`: a API de datastore/servidor mudou
> muito na série 3.8+ (3.13 reescreveu `ModbusSlaveContext`→`ModbusDeviceContext`,
> `zero_mode`, etc.). O `mock_plc.py` usa a API clássica (3.6.x validado).

## Convenções e notas

- **Não editar à mão** `open-plc/plc.xml` nem `pous/programs/main.ld`: são
  gerados/donos do OpenPLC Editor. Alterações de ladder vão como instruções em
  `open-plc/COMMAND_LAYER.md` (aplicar no editor, compilar e fazer upload).
- **Níveis** chegam como INT cru do Factory I/O; calibrar `LEVEL_RAW_MIN/MAX` em
  `config.py` após observar o range real.
- Código e comentários em **português** (contexto acadêmico).

## Verificação

Validado headless contra o `mock_plc.py`: round-trip Modbus (encher/drenar),
sinótico/tabela atualizando e o processo automático percorrendo todos os estados
até "Concluído". Para validar mudanças: subir o mock e rodar `app.py`
(`QT_QPA_PLATFORM=offscreen` para testes sem display).

## Pendências / próximos passos

- Aplicar a camada de comando no ladder (COMMAND_LAYER.md) e validar no lab.
- Documentos acadêmicos do PDF: P&ID + lista de instrumentos, folha de dados de
  1 instrumento (≥10 especificações), matriz Causa-e-Efeito — reaproveitar a
  tabela de tags.
