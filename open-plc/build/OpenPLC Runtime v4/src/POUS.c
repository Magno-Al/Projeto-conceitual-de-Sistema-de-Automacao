static inline INT __MAIN_SEL__INT__BOOL__INT__INT1(BOOL EN,
  BOOL G,
  INT IN0,
  INT IN1,
  MAIN *data__)
{
  INT __res;
  BOOL __TMP_ENO = __GET_VAR(data__->_TMP_SEL8663146_ENO,);
  __res = SEL__INT__BOOL__INT__INT(EN,
    &__TMP_ENO,
    G,
    IN0,
    IN1);
  __SET_VAR(,data__->_TMP_SEL8663146_ENO,,__TMP_ENO);
  return __res;
}

static inline INT __MAIN_SEL__INT__BOOL__INT__INT2(BOOL EN,
  BOOL G,
  INT IN0,
  INT IN1,
  MAIN *data__)
{
  INT __res;
  BOOL __TMP_ENO = __GET_VAR(data__->_TMP_SEL10764892_ENO,);
  __res = SEL__INT__BOOL__INT__INT(EN,
    &__TMP_ENO,
    G,
    IN0,
    IN1);
  __SET_VAR(,data__->_TMP_SEL10764892_ENO,,__TMP_ENO);
  return __res;
}

static inline INT __MAIN_SEL__INT__BOOL__INT__INT3(BOOL EN,
  BOOL G,
  INT IN0,
  INT IN1,
  MAIN *data__)
{
  INT __res;
  BOOL __TMP_ENO = __GET_VAR(data__->_TMP_SEL1152166_ENO,);
  __res = SEL__INT__BOOL__INT__INT(EN,
    &__TMP_ENO,
    G,
    IN0,
    IN1);
  __SET_VAR(,data__->_TMP_SEL1152166_ENO,,__TMP_ENO);
  return __res;
}

static inline INT __MAIN_SEL__INT__BOOL__INT__INT4(BOOL EN,
  BOOL G,
  INT IN0,
  INT IN1,
  MAIN *data__)
{
  INT __res;
  BOOL __TMP_ENO = __GET_VAR(data__->_TMP_SEL1305031_ENO,);
  __res = SEL__INT__BOOL__INT__INT(EN,
    &__TMP_ENO,
    G,
    IN0,
    IN1);
  __SET_VAR(,data__->_TMP_SEL1305031_ENO,,__TMP_ENO);
  return __res;
}

static inline INT __MAIN_MOVE__INT__INT5(BOOL EN,
  INT IN,
  MAIN *data__)
{
  INT __res;
  BOOL __TMP_ENO = __GET_VAR(data__->_TMP_MOVE9226523_ENO,);
  __res = MOVE__INT__INT(EN,
    &__TMP_ENO,
    IN);
  __SET_VAR(,data__->_TMP_MOVE9226523_ENO,,__TMP_ENO);
  return __res;
}

static inline INT __MAIN_MOVE__INT__INT6(BOOL EN,
  INT IN,
  MAIN *data__)
{
  INT __res;
  BOOL __TMP_ENO = __GET_VAR(data__->_TMP_MOVE8696851_ENO,);
  __res = MOVE__INT__INT(EN,
    &__TMP_ENO,
    IN);
  __SET_VAR(,data__->_TMP_MOVE8696851_ENO,,__TMP_ENO);
  return __res;
}

void MAIN_init__(MAIN *data__, BOOL retain) {
  __INIT_VAR(data__->MEM_START_T1,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->MEM_START_T2,__BOOL_LITERAL(FALSE),retain)
  __INIT_LOCATED(BOOL,__IX0_0,data__->BT_START_T1,retain)
  __INIT_LOCATED_VALUE(data__->BT_START_T1,__BOOL_LITERAL(FALSE))
  __INIT_LOCATED(BOOL,__IX0_1,data__->BT_STOP_T1,retain)
  __INIT_LOCATED_VALUE(data__->BT_STOP_T1,__BOOL_LITERAL(FALSE))
  __INIT_LOCATED(BOOL,__IX0_2,data__->BT_EMERG_T1,retain)
  __INIT_LOCATED_VALUE(data__->BT_EMERG_T1,__BOOL_LITERAL(FALSE))
  __INIT_LOCATED(BOOL,__IX0_3,data__->BT_EMERG_T3,retain)
  __INIT_LOCATED_VALUE(data__->BT_EMERG_T3,__BOOL_LITERAL(FALSE))
  __INIT_LOCATED(BOOL,__QX0_0,data__->LED_START_T1,retain)
  __INIT_LOCATED_VALUE(data__->LED_START_T1,__BOOL_LITERAL(FALSE))
  __INIT_LOCATED(BOOL,__QX0_1,data__->LED_STOP_T1,retain)
  __INIT_LOCATED_VALUE(data__->LED_STOP_T1,__BOOL_LITERAL(FALSE))
  __INIT_LOCATED(INT,__IW0,data__->NIVEL_T1,retain)
  __INIT_LOCATED_VALUE(data__->NIVEL_T1,0)
  __INIT_LOCATED(INT,__IW1,data__->VAZAO_T1,retain)
  __INIT_LOCATED_VALUE(data__->VAZAO_T1,0)
  __INIT_LOCATED(INT,__QW0,data__->VALV_ENTRADA_T1,retain)
  __INIT_LOCATED_VALUE(data__->VALV_ENTRADA_T1,0)
  __INIT_LOCATED(INT,__QW1,data__->VALV_SAIDA_T1,retain)
  __INIT_LOCATED_VALUE(data__->VALV_SAIDA_T1,0)
  __INIT_LOCATED(INT,__QW2,data__->DISPLAY_T1,retain)
  __INIT_LOCATED_VALUE(data__->DISPLAY_T1,0)
  __INIT_LOCATED(BOOL,__IX0_4,data__->BT_START_T2,retain)
  __INIT_LOCATED_VALUE(data__->BT_START_T2,__BOOL_LITERAL(FALSE))
  __INIT_LOCATED(BOOL,__IX0_5,data__->BT_STOP_T2,retain)
  __INIT_LOCATED_VALUE(data__->BT_STOP_T2,__BOOL_LITERAL(FALSE))
  __INIT_LOCATED(BOOL,__IX0_6,data__->BT_EMERG_T2,retain)
  __INIT_LOCATED_VALUE(data__->BT_EMERG_T2,__BOOL_LITERAL(FALSE))
  __INIT_LOCATED(BOOL,__QX0_2,data__->LED_START_T2,retain)
  __INIT_LOCATED_VALUE(data__->LED_START_T2,__BOOL_LITERAL(FALSE))
  __INIT_LOCATED(INT,__IW4,data__->NIVEL_T2,retain)
  __INIT_LOCATED_VALUE(data__->NIVEL_T2,0)
  __INIT_LOCATED(INT,__QW4,data__->VALV_ENTRADA_T2,retain)
  __INIT_LOCATED_VALUE(data__->VALV_ENTRADA_T2,0)
  __INIT_LOCATED(INT,__QW5,data__->VALV_SAIDA_T2,retain)
  __INIT_LOCATED_VALUE(data__->VALV_SAIDA_T2,0)
  __INIT_LOCATED(INT,__QW6,data__->DISPLAY_T2,retain)
  __INIT_LOCATED_VALUE(data__->DISPLAY_T2,0)
  __INIT_VAR(data__->_TMP_SEL8663146_ENO,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->_TMP_SEL8663146_OUT,0,retain)
  __INIT_VAR(data__->_TMP_SEL10764892_ENO,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->_TMP_SEL10764892_OUT,0,retain)
  __INIT_VAR(data__->_TMP_SEL1152166_ENO,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->_TMP_SEL1152166_OUT,0,retain)
  __INIT_VAR(data__->_TMP_SEL1305031_ENO,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->_TMP_SEL1305031_OUT,0,retain)
  __INIT_VAR(data__->_TMP_MOVE9226523_ENO,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->_TMP_MOVE9226523_OUT,0,retain)
  __INIT_VAR(data__->_TMP_MOVE8696851_ENO,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->_TMP_MOVE8696851_OUT,0,retain)
}

// Code part
void MAIN_body__(MAIN *data__) {
  // Initialise TEMP variables

  __SET_LOCATED(data__->,LED_START_T1,,((__GET_LOCATED(data__->BT_EMERG_T1,) && __GET_LOCATED(data__->BT_STOP_T1,)) && (__GET_LOCATED(data__->BT_START_T1,) || __GET_VAR(data__->MEM_START_T1,))));
  __SET_VAR(data__->,MEM_START_T1,,((__GET_LOCATED(data__->BT_EMERG_T1,) && __GET_LOCATED(data__->BT_STOP_T1,)) && (__GET_LOCATED(data__->BT_START_T1,) || __GET_VAR(data__->MEM_START_T1,))));
  __SET_LOCATED(data__->,LED_START_T2,,((__GET_LOCATED(data__->BT_EMERG_T2,) && __GET_LOCATED(data__->BT_STOP_T2,)) && (__GET_LOCATED(data__->BT_START_T2,) || __GET_VAR(data__->MEM_START_T2,))));
  __SET_VAR(data__->,MEM_START_T2,,((__GET_LOCATED(data__->BT_EMERG_T2,) && __GET_LOCATED(data__->BT_STOP_T2,)) && (__GET_LOCATED(data__->BT_START_T2,) || __GET_VAR(data__->MEM_START_T2,))));
  __SET_VAR(data__->,_TMP_SEL8663146_OUT,,__MAIN_SEL__INT__BOOL__INT__INT1(
    (BOOL)__BOOL_LITERAL(TRUE),
    (BOOL)__GET_LOCATED(data__->LED_START_T1,),
    (INT)0,
    (INT)1000,
    data__));
  if (__GET_VAR(data__->_TMP_SEL8663146_ENO,)) {
    __SET_LOCATED(data__->,VALV_ENTRADA_T1,,__GET_VAR(data__->_TMP_SEL8663146_OUT,));
  };
  __SET_VAR(data__->,_TMP_SEL10764892_OUT,,__MAIN_SEL__INT__BOOL__INT__INT2(
    (BOOL)__BOOL_LITERAL(TRUE),
    (BOOL)__GET_LOCATED(data__->LED_START_T2,),
    (INT)0,
    (INT)1000,
    data__));
  if (__GET_VAR(data__->_TMP_SEL10764892_ENO,)) {
    __SET_LOCATED(data__->,VALV_ENTRADA_T2,,__GET_VAR(data__->_TMP_SEL10764892_OUT,));
  };
  __SET_VAR(data__->,_TMP_SEL1152166_OUT,,__MAIN_SEL__INT__BOOL__INT__INT3(
    (BOOL)__BOOL_LITERAL(TRUE),
    (BOOL)__GET_LOCATED(data__->BT_EMERG_T1,),
    (INT)1000,
    (INT)0,
    data__));
  if (__GET_VAR(data__->_TMP_SEL1152166_ENO,)) {
    __SET_LOCATED(data__->,VALV_SAIDA_T1,,__GET_VAR(data__->_TMP_SEL1152166_OUT,));
  };
  __SET_VAR(data__->,_TMP_SEL1305031_OUT,,__MAIN_SEL__INT__BOOL__INT__INT4(
    (BOOL)__BOOL_LITERAL(TRUE),
    (BOOL)__GET_LOCATED(data__->BT_EMERG_T2,),
    (INT)1000,
    (INT)0,
    data__));
  if (__GET_VAR(data__->_TMP_SEL1305031_ENO,)) {
    __SET_LOCATED(data__->,VALV_SAIDA_T2,,__GET_VAR(data__->_TMP_SEL1305031_OUT,));
  };
  __SET_VAR(data__->,_TMP_MOVE9226523_OUT,,__MAIN_MOVE__INT__INT5(
    (BOOL)__BOOL_LITERAL(TRUE),
    (INT)__GET_LOCATED(data__->NIVEL_T1,),
    data__));
  if (__GET_VAR(data__->_TMP_MOVE9226523_ENO,)) {
    __SET_LOCATED(data__->,DISPLAY_T1,,__GET_VAR(data__->_TMP_MOVE9226523_OUT,));
  };
  __SET_VAR(data__->,_TMP_MOVE8696851_OUT,,__MAIN_MOVE__INT__INT6(
    (BOOL)__BOOL_LITERAL(TRUE),
    (INT)__GET_LOCATED(data__->NIVEL_T2,),
    data__));
  if (__GET_VAR(data__->_TMP_MOVE8696851_ENO,)) {
    __SET_LOCATED(data__->,DISPLAY_T2,,__GET_VAR(data__->_TMP_MOVE8696851_OUT,));
  };

  goto __end;

__end:
  return;
} // MAIN_body__() 





