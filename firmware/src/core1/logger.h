#ifndef LOGGER_H
#define LOGGER_H

#include <stdint.h>
#include <stddef.h>
#include "telemetry_frame.h"

bool logger_Init();

void Logger_WriteBlock(TelemetryFrame* buffer, size_t count);

#endif // LOGGER_H

