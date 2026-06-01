PROGRAM main
  VAR
    mem_start_t1 : BOOL;
    mem_start_t2 : BOOL;
    flag_val_t1 : BOOL;
    flag_val_t2 : BOOL;
    flag_drain_t1 : BOOL;
    flag_drain_t2 : BOOL;
  END_VAR
  VAR
    bt_start_t1 AT %IX0.0 : BOOL;
    bt_stop_t1 AT %IX0.1 : BOOL;
    bt_emerg_t1 AT %IX0.2 : BOOL;
    led_start_t1 AT %QX0.0 : BOOL;
    led_stop_t1 AT %QX0.1 : BOOL;
    nivel_t1 AT %IW0 : INT;
    vazao_t1 AT %IW1 : INT;
    valv_entrada_t1 AT %QW0 : INT;
    valv_saida_t1 AT %QW1 : INT;
    display_t1 AT %QW2 : INT;
    bt_start_t2 AT %IX0.4 : BOOL;
    bt_stop_t2 AT %IX0.5 : BOOL;
    bt_emerg_t2 AT %IX0.6 : BOOL;
    led_start_t2 AT %QX0.2 : BOOL;
    nivel_t2 AT %IW4 : INT;
    valv_entrada_t2 AT %QW4 : INT;
    valv_saida_t2 AT %QW5 : INT;
    display_t2 AT %QW6 : INT;
    cmd_fill_t1 AT %QX2.0 : BOOL;
    cmd_drain_t1 AT %QX2.1 : BOOL := 0;
    cmd_fill_t2 AT %QX2.2 : BOOL;
    cmd_drain_t2 AT %QX2.3 : BOOL := 0;
    cmd_remote AT %QX2.4 : BOOL;
  END_VAR
  VAR
    _TMP_OR1203558_ENO : BOOL;
    _TMP_OR1203558_OUT : BOOL;
    _TMP_SEL1999002_ENO : BOOL;
    _TMP_SEL1999002_OUT : INT;
    _TMP_OR3000485_ENO : BOOL;
    _TMP_OR3000485_OUT : BOOL;
    _TMP_SEL1874541_ENO : BOOL;
    _TMP_SEL1874541_OUT : INT;
    _TMP_OR8903313_OUT : BOOL;
    _TMP_SEL3154547_ENO : BOOL;
    _TMP_SEL3154547_OUT : INT;
    _TMP_OR3121229_OUT : BOOL;
    _TMP_SEL6836839_ENO : BOOL;
    _TMP_SEL6836839_OUT : INT;
    _TMP_MOVE9226523_ENO : BOOL;
    _TMP_MOVE9226523_OUT : INT;
    _TMP_MOVE8696851_ENO : BOOL;
    _TMP_MOVE8696851_OUT : INT;
  END_VAR

  led_start_t1 := bt_emerg_t1 AND bt_stop_t1 AND (bt_start_t1 OR mem_start_t1);
  mem_start_t1 := bt_emerg_t1 AND bt_stop_t1 AND (bt_start_t1 OR mem_start_t1);
  led_start_t2 := bt_emerg_t2 AND bt_stop_t2 AND (bt_start_t2 OR mem_start_t2);
  mem_start_t2 := bt_emerg_t2 AND bt_stop_t2 AND (bt_start_t2 OR mem_start_t2);
  _TMP_OR1203558_OUT := OR(EN := TRUE, IN1 := led_start_t1, IN2 := cmd_fill_t1, ENO => _TMP_OR1203558_ENO);
  _TMP_SEL1999002_OUT := SEL(EN := _TMP_OR1203558_ENO, G := flag_val_t1, IN0 := 0, IN1 := 1000, ENO => _TMP_SEL1999002_ENO);
  IF _TMP_OR1203558_ENO THEN
      flag_val_t1 := _TMP_OR1203558_OUT;
  END_IF;
  IF _TMP_SEL1999002_ENO THEN
      valv_entrada_t1 := _TMP_SEL1999002_OUT;
  END_IF;
  _TMP_OR3000485_OUT := OR(EN := TRUE, IN1 := led_start_t2, IN2 := cmd_fill_t2, ENO => _TMP_OR3000485_ENO);
  _TMP_SEL1874541_OUT := SEL(EN := _TMP_OR3000485_ENO, G := flag_val_t2, IN0 := 0, IN1 := 1000, ENO => _TMP_SEL1874541_ENO);
  IF _TMP_OR3000485_ENO THEN
      flag_val_t2 := _TMP_OR3000485_OUT;
  END_IF;
  IF _TMP_SEL1874541_ENO THEN
      valv_entrada_t2 := _TMP_SEL1874541_OUT;
  END_IF;
  _TMP_OR8903313_OUT := OR(NOT(bt_emerg_t1), cmd_drain_t1);
  flag_drain_t1 := _TMP_OR8903313_OUT;
  _TMP_SEL3154547_OUT := SEL(EN := TRUE, G := flag_drain_t1, IN0 := 0, IN1 := 1000, ENO => _TMP_SEL3154547_ENO);
  IF _TMP_SEL3154547_ENO THEN
      valv_saida_t1 := _TMP_SEL3154547_OUT;
  END_IF;
  _TMP_OR3121229_OUT := OR(NOT(bt_emerg_t2), cmd_drain_t2);
  flag_drain_t2 := _TMP_OR3121229_OUT;
  _TMP_SEL6836839_OUT := SEL(EN := TRUE, G := flag_drain_t2, IN0 := 0, IN1 := 1000, ENO => _TMP_SEL6836839_ENO);
  IF _TMP_SEL6836839_ENO THEN
      valv_saida_t2 := _TMP_SEL6836839_OUT;
  END_IF;
  _TMP_MOVE9226523_OUT := MOVE(EN := TRUE, IN := nivel_t1, ENO => _TMP_MOVE9226523_ENO);
  IF _TMP_MOVE9226523_ENO THEN
      display_t1 := _TMP_MOVE9226523_OUT;
  END_IF;
  _TMP_MOVE8696851_OUT := MOVE(EN := TRUE, IN := nivel_t2, ENO => _TMP_MOVE8696851_ENO);
  IF _TMP_MOVE8696851_ENO THEN
      display_t2 := _TMP_MOVE8696851_OUT;
  END_IF;
END_PROGRAM


CONFIGURATION Config0

  RESOURCE Res0 ON PLC
    TASK task0(INTERVAL := T#20ms,PRIORITY := 1);
    PROGRAM instance0 WITH task0 : main;
  END_RESOURCE
END_CONFIGURATION

(*DBG:char md5[] = "b09cb24a6608440258c9b614b884dbac";*)
(*DBG:/**)
(*DBG: * This file is part of OpenPLC Runtime*)
(*DBG: **)
(*DBG: * Copyright (C) 2023 Autonomy, GP Orcullo*)
(*DBG: * Based on the work by GP Orcullo on Beremiz for uC*)
(*DBG: **)
(*DBG: * This program is free software; you can redistribute it and/or*)
(*DBG: * modify it under the terms of the GNU General Public License*)
(*DBG: * as published by the Free Software Foundation; either version 2*)
(*DBG: * of the License, or (at your option) any later version.*)
(*DBG: **)
(*DBG: * This program is distributed in the hope that it will be useful,*)
(*DBG: * but WITHOUT ANY WARRANTY; without even the implied warranty of*)
(*DBG: * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the*)
(*DBG: * GNU General Public License for more details.*)
(*DBG: **)
(*DBG: * You should have received a copy of the GNU General Public License*)
(*DBG: * along with this program; If not, see <http://www.gnu.org/licenses/>.*)
(*DBG: **)
(*DBG: */*)
(*DBG:*)
(*DBG:#include <stdbool.h>*)
(*DBG:*)
(*DBG:// Include defines.h first for Arduino builds to set USE_*_BLOCKS macros*)
(*DBG:// before iec_std_FB.h processes its conditional includes*)
(*DBG:#ifdef ARDUINO*)
(*DBG:#include "../examples/Baremetal/defines.h"*)
(*DBG:#endif*)
(*DBG:*)
(*DBG:#include "iec_types_all.h"*)
(*DBG:#include "POUS.h"*)
(*DBG:*)
(*DBG:#define SAME_ENDIANNESS      0*)
(*DBG:#define REVERSE_ENDIANNESS   1*)
(*DBG:*)
(*DBG:char plc_program_md5[] = "b09cb24a6608440258c9b614b884dbac";*)
(*DBG:*)
(*DBG:uint8_t endianness;*)
(*DBG:*)
(*DBG:*)
(*DBG:extern MAIN RES0__INSTANCE0;*)
(*DBG:*)
(*DBG:static const struct {*)
(*DBG:    void *ptr;*)
(*DBG:    __IEC_types_enum type;*)
(*DBG:} debug_vars[] = {*)
(*DBG:    {&(RES0__INSTANCE0.MEM_START_T1), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.MEM_START_T2), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.FLAG_VAL_T1), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.FLAG_VAL_T2), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.FLAG_DRAIN_T1), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.FLAG_DRAIN_T2), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.BT_START_T1), BOOL_P_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.BT_STOP_T1), BOOL_P_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.BT_EMERG_T1), BOOL_P_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.LED_START_T1), BOOL_O_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.LED_STOP_T1), BOOL_O_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.NIVEL_T1), INT_P_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.VAZAO_T1), INT_P_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.VALV_ENTRADA_T1), INT_O_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.VALV_SAIDA_T1), INT_O_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.DISPLAY_T1), INT_O_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.BT_START_T2), BOOL_P_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.BT_STOP_T2), BOOL_P_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.BT_EMERG_T2), BOOL_P_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.LED_START_T2), BOOL_O_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.NIVEL_T2), INT_P_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.VALV_ENTRADA_T2), INT_O_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.VALV_SAIDA_T2), INT_O_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.DISPLAY_T2), INT_O_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.CMD_FILL_T1), BOOL_O_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.CMD_DRAIN_T1), BOOL_O_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.CMD_FILL_T2), BOOL_O_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.CMD_DRAIN_T2), BOOL_O_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0.CMD_REMOTE), BOOL_O_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0._TMP_OR1203558_ENO), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0._TMP_OR1203558_OUT), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0._TMP_SEL1999002_ENO), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0._TMP_SEL1999002_OUT), INT_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0._TMP_OR3000485_ENO), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0._TMP_OR3000485_OUT), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0._TMP_SEL1874541_ENO), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0._TMP_SEL1874541_OUT), INT_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0._TMP_OR8903313_OUT), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0._TMP_SEL3154547_ENO), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0._TMP_SEL3154547_OUT), INT_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0._TMP_OR3121229_OUT), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0._TMP_SEL6836839_ENO), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0._TMP_SEL6836839_OUT), INT_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0._TMP_MOVE9226523_ENO), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0._TMP_MOVE9226523_OUT), INT_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0._TMP_MOVE8696851_ENO), BOOL_ENUM},*)
(*DBG:    {&(RES0__INSTANCE0._TMP_MOVE8696851_OUT), INT_ENUM},*)
(*DBG:};*)
(*DBG:*)
(*DBG:#define VAR_COUNT               47*)
(*DBG:*)
(*DBG:uint16_t get_var_count(void)*)
(*DBG:{*)
(*DBG:    return VAR_COUNT;*)
(*DBG:}*)
(*DBG:*)
(*DBG:size_t get_var_size(size_t idx)*)
(*DBG:{*)
(*DBG:    if (idx >= VAR_COUNT)*)
(*DBG:    {*)
(*DBG:        return 0;*)
(*DBG:    }*)
(*DBG:    switch (debug_vars[idx].type) {*)
(*DBG:    case BOOL_ENUM:*)
(*DBG:    case BOOL_O_ENUM:*)
(*DBG:    case BOOL_P_ENUM:*)
(*DBG:        return sizeof(BOOL);*)
(*DBG:    case INT_ENUM:*)
(*DBG:    case INT_O_ENUM:*)
(*DBG:    case INT_P_ENUM:*)
(*DBG:        return sizeof(INT);*)
(*DBG:    default:*)
(*DBG:        return 0;*)
(*DBG:    }*)
(*DBG:}*)
(*DBG:*)
(*DBG:void *get_var_addr(size_t idx)*)
(*DBG:{*)
(*DBG:    void *ptr = debug_vars[idx].ptr;*)
(*DBG:*)
(*DBG:    switch (debug_vars[idx].type) {*)
(*DBG:    case BOOL_ENUM:*)
(*DBG:        return (void *)&((__IEC_BOOL_t *) ptr)->value;*)
(*DBG:    case BOOL_O_ENUM:*)
(*DBG:    case BOOL_P_ENUM:*)
(*DBG:        return (void *)((((__IEC_BOOL_p *) ptr)->flags & __IEC_FORCE_FLAG)*)
(*DBG:                        ? &(((__IEC_BOOL_p *) ptr)->fvalue)*)
(*DBG:                        : ((__IEC_BOOL_p *) ptr)->value);*)
(*DBG:    case INT_ENUM:*)
(*DBG:        return (void *)&((__IEC_INT_t *) ptr)->value;*)
(*DBG:    case INT_O_ENUM:*)
(*DBG:    case INT_P_ENUM:*)
(*DBG:        return (void *)((((__IEC_INT_p *) ptr)->flags & __IEC_FORCE_FLAG)*)
(*DBG:                        ? &(((__IEC_INT_p *) ptr)->fvalue)*)
(*DBG:                        : ((__IEC_INT_p *) ptr)->value);*)
(*DBG:    default:*)
(*DBG:        return 0;*)
(*DBG:    }*)
(*DBG:}*)
(*DBG:*)
(*DBG:void force_var(size_t idx, bool forced, void *val)*)
(*DBG:{*)
(*DBG:    void *ptr = debug_vars[idx].ptr;*)
(*DBG:*)
(*DBG:    if (forced) {*)
(*DBG:        size_t var_size = get_var_size(idx);*)
(*DBG:        switch (debug_vars[idx].type) {*)
(*DBG:        case BOOL_ENUM: {*)
(*DBG:            memcpy(&((__IEC_BOOL_t *) ptr)->value, val, var_size);*)
(*DBG:            ((__IEC_BOOL_t *) ptr)->flags |= __IEC_FORCE_FLAG;*)
(*DBG:            break;*)
(*DBG:        }*)
(*DBG:    *)
(*DBG:        case BOOL_O_ENUM: {*)
(*DBG:            memcpy((((__IEC_BOOL_p *) ptr)->value), val, var_size);*)
(*DBG:            memcpy(&((__IEC_BOOL_p *) ptr)->fvalue, val, var_size);*)
(*DBG:            ((__IEC_BOOL_p *) ptr)->flags |= __IEC_FORCE_FLAG;*)
(*DBG:            break;*)
(*DBG:        }*)
(*DBG:        case BOOL_P_ENUM: {*)
(*DBG:            memcpy(&((__IEC_BOOL_p *) ptr)->fvalue, val, var_size);*)
(*DBG:            ((__IEC_BOOL_p *) ptr)->flags |= __IEC_FORCE_FLAG;*)
(*DBG:            break;*)
(*DBG:        }*)
(*DBG:        case INT_ENUM: {*)
(*DBG:            memcpy(&((__IEC_INT_t *) ptr)->value, val, var_size);*)
(*DBG:            ((__IEC_INT_t *) ptr)->flags |= __IEC_FORCE_FLAG;*)
(*DBG:            break;*)
(*DBG:        }*)
(*DBG:    *)
(*DBG:        case INT_O_ENUM: {*)
(*DBG:            memcpy((((__IEC_INT_p *) ptr)->value), val, var_size);*)
(*DBG:            memcpy(&((__IEC_INT_p *) ptr)->fvalue, val, var_size);*)
(*DBG:            ((__IEC_INT_p *) ptr)->flags |= __IEC_FORCE_FLAG;*)
(*DBG:            break;*)
(*DBG:        }*)
(*DBG:        case INT_P_ENUM: {*)
(*DBG:            memcpy(&((__IEC_INT_p *) ptr)->fvalue, val, var_size);*)
(*DBG:            ((__IEC_INT_p *) ptr)->flags |= __IEC_FORCE_FLAG;*)
(*DBG:            break;*)
(*DBG:        }*)
(*DBG:        default:*)
(*DBG:            break;*)
(*DBG:        }*)
(*DBG:    } else {*)
(*DBG:        switch (debug_vars[idx].type) {*)
(*DBG:        case BOOL_ENUM:*)
(*DBG:            ((__IEC_BOOL_t *) ptr)->flags &= ~__IEC_FORCE_FLAG;*)
(*DBG:            break;*)
(*DBG:        case BOOL_O_ENUM:*)
(*DBG:        case BOOL_P_ENUM:*)
(*DBG:            ((__IEC_BOOL_p *) ptr)->flags &= ~__IEC_FORCE_FLAG;*)
(*DBG:            break;*)
(*DBG:        case INT_ENUM:*)
(*DBG:            ((__IEC_INT_t *) ptr)->flags &= ~__IEC_FORCE_FLAG;*)
(*DBG:            break;*)
(*DBG:        case INT_O_ENUM:*)
(*DBG:        case INT_P_ENUM:*)
(*DBG:            ((__IEC_INT_p *) ptr)->flags &= ~__IEC_FORCE_FLAG;*)
(*DBG:            break;*)
(*DBG:        default:*)
(*DBG:            break;*)
(*DBG:        }*)
(*DBG:    }*)
(*DBG:}*)
(*DBG:*)
(*DBG:void swap_bytes(void *ptr, size_t size)*)
(*DBG:{*)
(*DBG:    uint8_t *bytePtr = (uint8_t *)ptr;*)
(*DBG:    size_t i;*)
(*DBG:    for (i = 0; i < size / 2; ++i)*)
(*DBG:    {*)
(*DBG:        uint8_t temp = bytePtr[i];*)
(*DBG:        bytePtr[i] = bytePtr[size - 1 - i];*)
(*DBG:        bytePtr[size - 1 - i] = temp;*)
(*DBG:    }*)
(*DBG:}*)
(*DBG:*)
(*DBG:void trace_reset(void)*)
(*DBG:{*)
(*DBG:    for (size_t i=0; i < VAR_COUNT; i++)*)
(*DBG:    {*)
(*DBG:        force_var(i, false, 0);*)
(*DBG:    }*)
(*DBG:}*)
(*DBG:*)
(*DBG:void set_trace(size_t idx, bool forced, void *val)*)
(*DBG:{*)
(*DBG:    if (idx >= 0 && idx < VAR_COUNT)*)
(*DBG:    {*)
(*DBG:        if (endianness == REVERSE_ENDIANNESS)*)
(*DBG:        {*)
(*DBG:            // Prevent swapping for STRING type*)
(*DBG:            if (debug_vars[idx].type == STRING_ENUM)*)
(*DBG:            {*)
(*DBG:                // Do nothing*)
(*DBG:                ;*)
(*DBG:            }*)
(*DBG:            else*)
(*DBG:            {*)
(*DBG:                swap_bytes(val, get_var_size(idx));*)
(*DBG:            }*)
(*DBG:        }*)
(*DBG:*)
(*DBG:        force_var(idx, forced, val);*)
(*DBG:    }*)
(*DBG:}*)
(*DBG:*)
(*DBG:void set_endianness(uint8_t value)*)
(*DBG:{*)
(*DBG:    if (value == SAME_ENDIANNESS || value == REVERSE_ENDIANNESS)*)
(*DBG:    {*)
(*DBG:        endianness = value;*)
(*DBG:    }*)
(*DBG:}*)
(*DBG:*)