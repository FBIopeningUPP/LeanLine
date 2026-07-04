#ifndef GPS_PARSER_H
#define GPS_PARSER_H

#include <stdint.h>
#include "hardware/uart.h"

void GPS_Init(uart_inst_t *uart_port);
void GPS_Process();
void GPS_GetData(int32_t* lat, int32_t* lon, uint16_t* speed, uint16_t* heading);

#endif