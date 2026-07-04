#include <stdio.h>
#include "pico/stdlib.h"
#include "pci/multicore.h"
#include "hardware/timer.h"

#include "telemetry_frame.h"
#include "core0/imu_driver.h"
#include "core0/gps_parser.h"
#include "core0/sensor_fusion.h"
#include "core1/ping_pong_buf.h"
#include "core1/logger.h"


#define FRAMES_PER_BLOCK 16

PingPongBuffer<TelemetryFrame, FRAMES_PER_BLOCK> telemetry_buffer;

#define SPI_PORT spi0
#define IMU_CS_PIN 5
#define UART_PORT uart0

void core1_entry(){
    stdio_init_all();
    sleep_ms(2000);
    printf("A.T.L.A.S. (Lean Line) Firmware Initializing... \n");

    telemetry_buffer.init();

    multicore_launch_core1(core1_entry);

    IMU_Init(SPI_PORT, IMU_CS_PIN);
    GPS_Init(UART_PORT);

    const uint32_t loop_interval_us = 10000;
    uint32_t next_loop_time = time_us_32() + loop_interval_us;
    
    printf("Core 0: Entering Sensor Acquisition Loop (100Hz)...\n");

    while (true) {
        GPS_Process();

        int16_t ax, ay, az, gx, gy, gz;
        IMU_Read(&ax, &ay, &az, &gx, &gy, &gz);

        int32_t lat, lon;
        uint16_t speed, heading;
        GPS_GetData(&lat, &lon, &speed, &heading);

        int16_t lean_angle = SensorFusion_CalculateLeanAngle(ax, ay, az, gx, gy, gz, speed);

        TelemetryFrame frame = {0};
        frame.timestamp_ms = time_us_32() / 1000;
        frame.accel_x = ax;
        frame.accel_y = ay;
        frame.accel_z = az;
        frame.gyro_x = gx;
        frame.gyro_y = gy;
        frame.gyro_z = gz;
        frame.latitude = lat;
        frame.longitude = lon;
        frame.ground_speed = speed;
        frame.heading = heading;
        frame.lean_angle = lean_angle;
        frame.padding = 0;

        telemetry_buffer.push(frame);
        
        busy_wait_until(next_loop_time);
        next_loop_time += loop_interval_us;
    }

    return 0;

}

void core1_entry() {
    printf("Core 1: Initializing SD Card Logger...\n");

    if (!Logger_Init()) {
        printf("Core 1 ERROR: SD Card Mount Failed!\n");
        while (true) tight_loop_contents();
    }

    printf("Core 1: Logger Ready. Waiting for data...\n");

    while (true) {
        TelemetryFrame* ready_block = telemetry_buffer.wait_for_full_block();
        Logger_WriteBlock(ready_block, FRAMES_PER_BLOCK);
        telemetry_buffer.free_block();
    }
}
