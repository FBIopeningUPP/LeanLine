#include "sensor_fusion.h"
#include <math.h>

#define PI 3.1415926535f
#define GRAVITY 9.81f

#define DT 0.01f // Time step in seconds (100 Hz)

#define ALPHA 0.98f // Complementary filter coefficient

static float current_lean_angle = 0.0f; // Current lean angle in degrees

int16_t SensorFusion_CalculateLean(int16_t ax, int16_t ay, int16_t az, 
                                   int16_t gx, int16_t gy, int16_t gz,
                                   uint16_t speed_cms) 
{
    float roll_rate_dps = (float)gx / 16.4f; // Convert gyro reading to degrees per second
    float yaw_rate_dps = (float)gy / 16.4f; // Convert gyro reading to degrees per second

    float gyro_angle = current_lean_angle + (roll_rate_dps * DT); // Integrate gyro rate to get angle

    float v_mps = (float)speed_cms / 100.0f; // Convert speed from cm/s to m/s
    float yaw_rate_rads = yaw_rate_dps * (PI / 180.0f); // Convert yaw rate to radians per second

    float centripetal_acc = v_mps * yaw_rate_rads;

    float physics_angle_rads = atan2f(centripetal_acc, GRAVITY); // Calculate lean angle based on centripetal acceleration
    float physics_angle_degs = physics_angle_rads * (180.0f / PI); // Convert to degrees

    if (speed_cms > 300) {
        current_lean_angle = (ALPHA * gyro_angle) + ((1.0f - ALPHA) * physics_angle_degs); // Complementary filter
    } else {
        float ay_g = (float)ay / 2048.0f; // Convert accelerometer reading to g's
        float az_g = (float)az / 2048.0f; // Convert accelerometer reading to g's
        float static_angle = atan2f(ay_g, az_g) * (180.0f / PI); // Calculate lean angle from accelerometer

        current_lean_angle = (ALPHA * gyro_angle) + ((1.0f - ALPHA) * static_angle); // Complementary filter
    }

    return (int16_t)(current_lean_angle * 100.0f);  // Return the current lean angle as an integer
}

