#ifndef SENSOR_FUSION_H
#define SENSOR_FUSION_H

#include <stdint.h>

int16_t SensorFusion_CalculateLean(int16_t ax, int16_t ay, int16_t az,
                                   int16_t gx, int16_t gy, int16_t gz,
                                uint16_t speed_cms);

#endif

