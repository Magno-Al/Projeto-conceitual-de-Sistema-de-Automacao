# Folha de Dados de Instrumento

**Norma de referência:** ISA 20.00.01 / IEC 61511

---

## Identificação do Instrumento

| Campo | Valor |
|-------|-------|
| **Tag** | LT-101 |
| **Revisão** | 1.0 |
| **Data** | 2026-06-01 |

---

## 1. Função / Descrição

| # | Especificação | Valor |
|---|---------------|-------|
| 1 | **Identificação (Tag)** | LT-101 |
| 2 | **Descrição** | Transmissor de Nível do Tanque 1 (Tank 0 – Factory I/O) |
| 3 | **Função** | Medir e transmitir continuamente o nível de líquido no Tanque 1 para o CLP via protocolo Modbus TCP |
| 4 | **Localização** | Campo — Tanque T1 (planta simulada no Factory I/O) |
| 5 | **Loop de controle** | Malha de nível LIC-101 (Tanque 1) |

---

## 2. Variável de Processo

| # | Especificação | Valor |
|---|---------------|-------|
| 6 | **Variável medida** | Nível de líquido (água) |
| 7 | **Princípio de medição** | Sensor analógico de posição linear (simulado por Factory I/O — equivalente a transmissor ultrassônico ou de pressão diferencial) |
| 8 | **Fluido de processo** | Água (H₂O) |
| 9 | **Temperatura do processo** | Ambiente (~25 °C) |
| 10 | **Pressão de operação** | Atmosférica (1 atm) |

---

## 3. Especificações de Medição

| # | Especificação | Valor |
|---|---------------|-------|
| 11 | **Range de medição** | 0 a 100 % do volume do tanque |
| 12 | **Sinal de saída (raw Modbus)** | 0 a 1000 (inteiro sem sinal de 16 bits) |
| 13 | **Resolução** | 1 unidade (0,1% do span) |
| 14 | **Unidade de engenharia** | % (porcentagem do volume) |
| 15 | **Escala de conversão** | `% = (raw / 1000) × 100` — implementada em `config.raw_to_percent()` |
| 16 | **Precisão / Exatidão** | ±0,1 % do span (resolução do simulador Factory I/O) |
| 17 | **Tempo de resposta** | < 100 ms (ciclo do Factory I/O) |

---

## 4. Interface e Comunicação

| # | Especificação | Valor |
|---|---------------|-------|
| 18 | **Protocolo de comunicação** | Modbus TCP/IP |
| 19 | **Endereço Modbus** | Input Register 0 (IR 0), Function Code 4 (FC4) |
| 20 | **Endereço IEC 61131-3 (OpenPLC)** | `%IW0` |
| 21 | **Servidor Modbus** | OpenPLC Runtime v4 (porta TCP 5020) |
| 22 | **Ciclo de atualização** | 100 ms (ciclo do CLP OpenPLC) |
| 23 | **Ciclo de polling SCADA** | 200 ms (configurável em `config.POLL_INTERVAL_MS`) |

---

## 5. Instalação e Operação

| # | Especificação | Valor |
|---|---------------|-------|
| 24 | **Alimentação** | Simulado (Factory I/O — sem alimentação física) |
| 25 | **Temperatura ambiente de operação** | 0 °C a 50 °C (Factory I/O: execução em PC Windows) |
| 26 | **Grau de proteção** | N/A (ambiente simulado) |
| 27 | **Montagem** | Lateral do tanque (posição fixa no modelo 3D Factory I/O) |

---

## 6. Alarmes e Limites

| Condição | Limite | Ação |
|----------|--------|------|
| Nível Baixo (LL) | < 5 % (raw < 50) | Indicação no SCADA — inibe comando de esvaziamento |
| Nível Alto (HH) | > 95 % (raw > 950) | Indicação no SCADA — inibe comando de enchimento |
| Falha de comunicação | Timeout > 1 s | SCADA exibe "Desconectado" — comandos bloqueados |

---

## 7. Diagrama de Blocos do Instrumento

```
  TANQUE T1                   FACTORY I/O                  OPENPLC v4              SCADA
  ─────────                   ──────────                   ──────────              ─────
  Sensor de        Raw 0–1000  Modbus Server    %IW0       Ladder        Modbus    Indicação
  nível (float) ──────────────► (porta :502) ──────────── ►  logic  ──── TCP ────► nível %
  (0.0 a 1.0)                                              (CLP)        :5020      e alarmes
```

---

## 8. Referências e Normas

| Norma | Título |
|-------|--------|
| ISA 5.1 | Instrumentation Symbols and Identification |
| IEC 61131-3 | Linguagens de Programação para CLP |
| IEC 61511 | Functional Safety for Process Industry |
| Modbus.org | Modbus Application Protocol Specification V1.1b3 |
