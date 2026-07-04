#include "logger.h"
#include <stdio.h>

static FILE* log_file = NULL;

static uint32_t blocks_written = 0;

bool Logger_Init() {
    log_file = fopen("Leanline.dat", "wb");

    if (log_file == NULL) {
        return false;
    }
    return true;
}

void Logger_WriteBlock(TelemetryFrame* buffer, size_t count) {
    if (log_file == NULL) return;

    size_t written = fwrite(buffer, sizeof(TelemetryFrame), count, log_file);
    if (written == count ) {
        blocks_written++;

        if (blocks_written % 10 == 0) {
            fflush(log_file);
        }
    }
}

