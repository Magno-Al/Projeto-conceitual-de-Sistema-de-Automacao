#include "POUS.h"
#include "Config0.h"

void MAIN_init__(MAIN *data__, BOOL retain) {
  __INIT_LOCATED(BOOL,__IX0_0,data__->BT_START_T1,retain)
  __INIT_LOCATED_VALUE(data__->BT_START_T1,__BOOL_LITERAL(FALSE))
  __INIT_LOCATED(BOOL,__IX0_1,data__->BT_STOP_T1,retain)
  __INIT_LOCATED_VALUE(data__->BT_STOP_T1,__BOOL_LITERAL(FALSE))
  __INIT_LOCATED(BOOL,__QX0_0,data__->LED_START_T1,retain)
  __INIT_LOCATED_VALUE(data__->LED_START_T1,__BOOL_LITERAL(FALSE))
}

// Code part
void MAIN_body__(MAIN *data__) {
  // Initialise TEMP variables

  __SET_LOCATED(data__->,LED_START_T1,,(!(__GET_LOCATED(data__->BT_STOP_T1,)) && (__GET_LOCATED(data__->BT_START_T1,) || __GET_LOCATED(data__->LED_START_T1,))));

  goto __end;

__end:
  return;
} // MAIN_body__() 





