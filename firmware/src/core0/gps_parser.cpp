#include "gps_parser.h"
#include "hardware/gpio.h"

#define UBX_SYNC_CHAR_1 0xB5
#define UBX_SYNC_CHAR_2 0x62

#define UBX_NAV_CLASS 0x01
#define UBX_NAV_PVT 0x07

static uart_inst_t* gps_uart;

static int32_t latest_lat = 0;
static int32_t latest_lon = 0;
static uint16_t latest_speed = 0;
static uint16_t latest_heading = 0;

enum UBX_State {
    SYNC1, SYNC2, CLASS, ID, LEN1, LEN2, PAYLOAD, CKA, CKB
};

static UBX_State parser_state = SYNC1;
static uint8_t msg_class, msg_id;
static uint16_t msg_len;
static uint16_t payload_idx = 0;
static uint8_t payload_buf[100];
static uint8_t calc_ck_a = 0, calc_ck_b = 0;

void GPS_Init(uart_inst_t *uart_port) {
    gps_uart = uart_port;

    uart_init(gps_uart, 115200);

    gpio_set_function(0, GPIO_FUNC_UART);
    gpio_set_function(1, GPIO_FUNC_UART);

    uart_set_hw_flow(gps_uart, false, false);

    uart_set_format(gps_uart, 8, 1, UART_PARITY_NONE);

    uart_set_fifo_enabled(gps_uart, true);
}

static void parse_byte(uint8_t b){
    switch (parser_state) {
        case SYNC1;
            if (b == UBX_SYNC_1) parser_state = SYNC2;
            break;
        case SYNC2:
            if (b == UBX_SYNC_2){ 
            parser_state = CLASS;
            calc_ck_a = 0;
            calc_ck_b = 0;
            } else {
                parser_state = SYNC1;
            }
            break;
        case CLASS:
            msg_class = b;
            calc_ck_a += b; calc_ck_b += calc_ck_a;
            parser_state = ID;
            break;
        case ID:
            msg_id = b;
            calc_ck_a += b; calc_ck_b += calc_ck_a;
            parser_state = LEN1;
            break;
        case LEN1:
            msg_len = b;
            calc_ck_a += b; calc_ck_b += calc_ck_a;
            parser_state = LEN2;
            break;
        case LEN2:
            msg_len |= (b << 8);
            calc_ck_a += b; calc_ck_b += calc_ck_a;
            if (msg_len > sizeof(payload_buf)) {
                parser_state = SYNC1; // Message too big, discard
            } else {
                payload_idx = 0;
                parser_state = PAYLOAD;
            }
            break;
        case PAYLOAD:
            payload_buf[payload_idx++] = b;
            calc_ck_a += b; calc_ck_b += calc_ck_a;
            if (payload_idx >= msg_len) {
                parser_state = CKA;
            }
            break;
        case CKA:
            if (b == calc_ck_a) {
                    parser_state = CKB;
                } else {
                    parser_state = SYNC1; // Checksum fail
                }
                break;
        case CKB:
            if (b == calc_ck_a) {
                if (msg_class == UBX_NAV_CLASS && msg_id == UBX_NAV_PVT && msg_len >= 92) {
                    int32_t lon_raw = payload_buf[32] | (payload_buf[25] << 8) | (payload_buf[26] << 16) | (payload_buf[27] << 24);
                    int32_t lat_raw = payload_buf[28] | (payload_buf[29] << 8) | (payload_buf[30] << 16) | (payload_buf[31] << 24);
                    int16_t gSpeed_mm_s = payload_buf[60] | (payload_buf[61] << 8)  | (payload_buf[62] << 16) | (payload_buf[63] << 24);
                    int16_t headMot_1e5 = payload_buf[64] | (payload_buf[65] << 8) | (payload_buf[66] << 16) | (payload_buf[67] << 24);\

                    latest_lon = ln_raw;
                    latest_lat = lat_raw;

                    if (gSpeed_mm_s > 0) latest_speed = (uint16_t)(gSpeed_mm_s / 10);
                    else latest_speed = 0;

                    if (headMot_1e5 > 0) latest_heading = (uint16_t)(headMot_1e5 / 10000);
                    else latest_heading = 0;
                }
            }
            parser_state = SYNC1;
            break;
    }
}

void GPS_Process() {
    while (uart_is_readable(gps_uart)) {
        uint8_t byte = uart_getc(gps_uart);
        parse_byte(byte);
    }
}

void GPS_GetData(int32_t* lat, int32_t* lon, uint16_t* speed, uint16_t* heading) {
    *lat = latest_lat;
    *lon = latest_lon;
    *speed = latest_speed;
    *heading = latest_heading;
}
