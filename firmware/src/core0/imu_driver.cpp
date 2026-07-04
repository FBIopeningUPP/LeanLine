#include "imu_driver.h"
#include "hardware/gpio.h"
#include "pico/time.h"

#define REG_DEVICE_CONFIG 0x11
#define REG_PWR_MGMT0 0x4E
#define REG_ACCEL_CONFIG 0x50
#define REG_GYRO_CONFIG 0x4F
#define REG_ACCL_DATA_X1 0x1F

static spi_inst_t* imu_spi;
static uint imu_cs;

static void cs_select(){
    asm volatile("nop \n nop \n nop");
    gpio_put(imu_cs, 0);
    asm volatile("nop \n nop \n nop");
}

static void cs_deselect(){
    asm volatile("nop \n nop \n nop");
    gpio_put(imu_cs, 1);
    asm volatile("nop \n nop \n nop");
}

static void write_register(uint8_t reg, uint8_t data){
    cs_select();
    spi_write_blocking(imu_spi, buf, 2);
    cs_deselect();
    sleep_ms(1);
}

void IMU_Init(spi_inst_t *spi_port, uint cs_pin){
    imu_spi = spi_port;
    imu_cs = cs_pin;

    spi_init(imu_spi, 800000);

    spi_set_format(imu_spi, 8, SPI_CPOL_1, SPI_CPHA_1, SPI_MSB_FIRST);

    gpio_init(imu_cs);
    gpio_set_dir(imu_cs, GPIO_OUT);
    gpio_put(imu_cs, 1);

    sleep_ms(100);

    write_register(REG_DEVICE_CONFIG, 0x01);
    sleep_ms(50);

    write_register(REG_PWR_MGMT0, 0x0F);
    sleep_ms(50);

    write_register(REG_ACCEL_CONFIG0, 0x06);

    write _register(REG_GYRO_CONFIG0, 0x06);

    sleep_ms(50);
}

void IMU_Read(int16_t *ax, int16_t* ay, int16_t* az, int16_t* gx, int16_t* gy, int16_t* gz) {
    uint8_t reg = REG_ACCL_DATA_X1 | 0x80;
    uint8_t raw_data[12];
    
    cs_select();

    spi_write_blocking(imu_spi, &reg, 1);

    spi_read_blocking(imu_spi, 0x00, raw_data, 12);

    cs_deselect();

    *ax = (int16_t)((raw_data[0] << 8) | raw_data[1]);
    *ay = (int16_t)((raw_data[2] << 8) | raw_data[3]);
    *az = (int16_t)((raw_data[4] << 8) | raw_data[5]);
    *gx = (int16_t)((raw_data[6] << 8) | raw_data[7]);
    *gy = (int16_t)((raw_data[8] << 8) | raw_data[9]);
    *gz = (int16_t)((raw_data[10] << 8) | raw_data[11]);
}

