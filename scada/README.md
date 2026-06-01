# SCADA — Planta de 2 Tanques (PySide6 + Modbus TCP)

Aplicação SCADA para a planta de 2 tanques simulada no **Factory I/O** e
controlada pelo **OpenPLC v4** (ladder). O SCADA é um **cliente Modbus TCP** do
servidor do OpenPLC: lê todas as variáveis da planta, permite **controle manual
ponto a ponto** e executa um **processo automático** parametrizado.

## Arquitetura

```
Factory I/O  <--Modbus TCP-->  OpenPLC v4 (ladder + servidor Modbus)  <--Modbus TCP-->  SCADA (este app)
 (servidor 502)                (mestre do Factory I/O; servidor p/ SCADA)               (cliente)
```

O OpenPLC é mestre do Factory I/O (porta 502). O **servidor Modbus do próprio
OpenPLC** — onde este SCADA conecta — normalmente fica em **outra porta**
(confira em OpenPLC → Settings → *Modbus Server* e ajuste em `config.py`).

### Camada de comando (por que o SCADA não escreve direto nas saídas)
Num PLC, o ladder recalcula as saídas (`%QX`/`%QW`) a cada scan, então um cliente
Modbus não consegue sobrescrevê-las. Por isso o SCADA escreve em **coils de
comando livres** (`%QX2.0`+ / coils 16+) que o ladder lê e combina (OR) com os
botões físicos. Veja `../open-plc/COMMAND_LAYER.md` para as alterações no ladder.

## Instalação

```bash
cd scada
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> `pymodbus` está fixado em `>=3.5,<3.8` (a API do datastore/servidor mudou na
> série 3.8+; o mock usa a API clássica).

## Executar

**1. Contra o setup real (Windows/lab):** Factory I/O + OpenPLC rodando (com a
ladder recompilada incluindo a camada de comando). Ajuste host/porta em
`config.py` (ou na barra de conexão) e rode:

```bash
python app.py
```

**2. Desenvolvimento no Linux (sem Factory I/O):** suba o mock, que emula
PLC + física dos tanques, e aponte o SCADA para a porta dele:

```bash
python tools/mock_plc.py 15020      # terminal 1
# em config.py: MODBUS_PORT = 15020  (ou digite na barra de conexão)
python app.py                        # terminal 2
```

## Telas

- **Sinótico animado:** 2 tanques com nível em tempo real, válvulas
  (verde = aberta), LEDs de start e alarme de emergência.
- **Controle:** botões Encher / Pausar / Esvaziar por tanque + painel do
  processo automático (4 parâmetros: 2 níveis-alvo + 2 tempos).
- **Tags:** tabela com todas as variáveis (ler tudo; alternar coils de comando).
- **Tendência:** gráfico dos níveis (%) ao longo do tempo.

## Processo automático (sequência)

1. Enche T1 até o nível-alvo 1
2. Pausa, aguarda o tempo 1
3. Esvazia T1 enquanto enche T2 até o nível-alvo 2
4. Aguarda o tempo 2
5. Esvazia T2 e finaliza

A lógica de sequência roda no SCADA (supervisão); a atuação vai pelas coils de
comando para o PLC. "Parar" faz parada segura (zera todos os comandos).

## Calibração

Os níveis chegam como INT cru do Factory I/O. Após observar o range real,
ajuste `LEVEL_RAW_MIN`/`LEVEL_RAW_MAX` em `config.py` para a conversão cru → %.

## Estrutura

```
scada/
  app.py                 entrypoint
  config.py              conexão, escala, polling
  tags.py                registro central de tags (mapa Modbus)
  plc/modbus_worker.py   QThread: polling + escrita (pymodbus)
  core/process_engine.py máquina de estados do processo automático
  ui/                    sinótico, manual, auto, tabela de tags, tendência
  tools/mock_plc.py      servidor Modbus de simulação (dev no Linux)
```
