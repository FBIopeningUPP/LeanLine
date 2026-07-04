cmake_minimum_required(VERSION 3.13)

    # Include the Pico SDK import file
    include(pico_sdk_import.cmake)

    project(LeanLine_ATLAS C CXX ASM)
    set(CMAKE_C_STANDARD 11)
    set(CMAKE_CXX_STANDARD 17)

    # Initialize the Pico SDK
    pico_sdk_init()

    # Add our executable and ALL source files
    add_executable(atlas_firmware
        src/main.cpp
        src/core0/imu_driver.cpp
        src/core0/gps_parser.cpp
        src/core0/sensor_fusion.cpp
        src/core1/logger.cpp
    )

    # Pull in the hardware libraries we need
    target_link_libraries(atlas_firmware
        pico_stdlib
        pico_multicore
        hardware_spi
        hardware_uart
        hardware_dma
    )

    # Enable USB serial output, disable UART output
    pico_enable_stdio_usb(atlas_firmware 1)
    pico_enable_stdio_uart(atlas_firmware 0)

    # Generate the .uf2 file for drag-and-drop flashing
    pico_add_extra_outputs(atlas_firmware)