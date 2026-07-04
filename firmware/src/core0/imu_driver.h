#ifndef IMU_DRIVER_H
#define IMU_DRIVER_H

#include <stdint.h>
#include "hardware/spi.h"

void IMU_Init(spi_inst_t *spi_port, uint cs_pin);
void IMU_Read(int16_t *ax, int16_t *ay, int16_t *az, int16_t *gx, int16_t *gy, int16_t *gz);

#endif 