# Camada de comando do SCADA — alterações no ladder

O SCADA (cliente Modbus) só pode **escrever** em coils e holding registers, e não
pode sobrescrever as saídas que o ladder recalcula a cada scan. Por isso criamos
**coils de comando livres** que o SCADA escreve e o ladder *lê*, combinando-as
(OR) com os botões físicos. Assim o controle real continua no PLC e o SCADA
supervisiona/sequencia.

As coils usadas (≥ `%QX2.0` / coil 16) estão **fora** da faixa que o Factory I/O
troca (`%QX0.0–%QX1.7`, coils 0–15), então não há conflito.

## 1. Novas variáveis (adicionar em `main` no OpenPLC Editor)

| Variável | Endereço | Tipo | Modbus coil | Função |
|---|---|---|---|---|
| `cmd_fill_t1`  | `%QX2.0` | BOOL | 16 | abrir válvula de entrada T1 |
| `cmd_drain_t1` | `%QX2.1` | BOOL | 17 | abrir válvula de saída T1 |
| `cmd_fill_t2`  | `%QX2.2` | BOOL | 18 | abrir válvula de entrada T2 |
| `cmd_drain_t2` | `%QX2.3` | BOOL | 19 | abrir válvula de saída T2 |
| `cmd_remote` (opcional) | `%QX2.4` | BOOL | 20 | habilita modo remoto |

## 2. Rungs de válvula (modificar os existentes)

A lógica de **selo (start/stop/emergência) permanece intacta** — os botões
físicos continuam funcionando. Só os 4 rungs que acionam as válvulas via `SEL`
passam a considerar também os comandos do SCADA.

Equivalente em ST (implemente como LD no editor — `SEL` com a condição no `G`):

```iecst
(* Entrada T1: abre se o selo de start estiver ligado OU houver comando do SCADA *)
valv_entrada_t1 := SEL(G := led_start_t1 OR cmd_fill_t1, IN0 := 0, IN1 := 1000);

(* Entrada T2 *)
valv_entrada_t2 := SEL(G := led_start_t2 OR cmd_fill_t2, IN0 := 0, IN1 := 1000);

(* Saída T1: abre na emergência (bt_emerg_t1 é NF: 0 quando pressionado)
   OU por comando do SCADA *)
valv_saida_t1 := SEL(G := (NOT bt_emerg_t1) OR cmd_drain_t1, IN0 := 0, IN1 := 1000);

(* Saída T2 *)
valv_saida_t2 := SEL(G := (NOT bt_emerg_t2) OR cmd_drain_t2, IN0 := 0, IN1 := 1000);
```

> Observação sobre polaridade: no programa original, a saída usava
> `SEL(G := bt_emerg_t1, IN0 := 1000, IN1 := 0)` — ou seja, abre (1000) quando a
> emergência é pressionada (`bt_emerg_t1 = 0`). A forma acima é equivalente
> (`drain := (NOT bt_emerg_t1) OR cmd_drain_t1`) e acrescenta o comando do SCADA.

## 3. Passos no OpenPLC

1. Abrir o projeto no **OpenPLC Editor**, adicionar as 4 (ou 5) variáveis acima.
2. Ajustar os 4 rungs de válvula conforme a lógica acima.
3. **Compilar** e fazer **upload** para o OpenPLC Runtime.
4. Confirmar a porta do *Modbus Server* do OpenPLC (Settings) e apontar o SCADA
   para ela (`scada/config.py` → `MODBUS_PORT`).

## 4. Mapa Modbus de leitura (referência do SCADA)

| Tag | IEC | Modbus | FC |
|---|---|---|---|
| nivel_t1 / nivel_t2 | %IW0 / %IW4 | Input Reg 0 / 4 | 4 |
| valv_entrada/saida_t1 | %QW0 / %QW1 | Hold Reg 0 / 1 | 3 |
| valv_entrada/saida_t2 | %QW4 / %QW5 | Hold Reg 4 / 5 | 3 |
| led_start_t1 / led_start_t2 | %QX0.0 / %QX0.2 | Coil 0 / 2 | 1 |
| bt_start/stop/emerg_t1 | %IX0.0/.1/.2 | DI 0/1/2 | 2 |
| bt_start/stop/emerg_t2 | %IX0.4/.5/.6 | DI 4/5/6 | 2 |
