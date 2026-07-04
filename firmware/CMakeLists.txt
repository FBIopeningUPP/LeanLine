cmake_minimum_required(VERSION 3.13)

include(pico_sdk_import.cmake)

project(LeanLine_ATLAS C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

pico_sdk_init()

add_executable(atlas_firmware
src/main.cpp
)

target_link_libraries(atlas_firmware
    pico_stdlib
    pico_multicore
    hardware_spi
    hardware_uart
    hardware_dma
)

pico_enable_stdio_usb(atlas_firmware 1)
pico_enable_stdio_uart(atlas_firmware 0)

pico_add_extra_outputs(atlas_firmware)
