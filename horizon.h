#pragma once
#include "config_common.h"
/* USB Device descriptor parameter */
#define VENDOR_ID       0xFEED
#define PRODUCT_ID      0x0001
#define DEVICE_VER      0x0001
#define MANUFACTURER    YourName
#define PRODUCT         Horizon
/* key matrix size */
#define MATRIX_ROWS 4
#define MATRIX_COLS 12
/* key matrix pins */
#define MATRIX_ROW_PINS { B0, B1, B2, B3 }
#define MATRIX_COL_PINS { C0, C1, C2, C3, C4, C5, C6, C7, D0, D1, D2, D3 }
#define DIODE_DIRECTION COL2ROW