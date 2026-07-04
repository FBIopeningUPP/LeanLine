import struct
import os
from core.data_model import TelemetryFrame


class FrameParser:
    FRAME_FORMAT = '<I6h2i2HhH'
    FRAME_SIZE = 32

    @staticmethod
    def parse_file(filepath: str) -> list[TelemetryFrame]:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Telemetry File not found: {filepath}")
        
        frames = []
        print(f"Parsing telemetry binary: {filepath}")

        with open(filepath, 'rb') as f:
            while true:

                chunk = f.read(FrameParser.FRAME_SIZE)

                if not chunk or len(chunk) < FrameParser.FRAME_SIZE:
                    break  
                    
                unpacked = struct.unpack(FrameParser. FRAME_FORMAT, chunk)

                frame = TelemetryFrame(
                    timestamp_ms=unpacked[0],
                    accel_x=unpacked[1],
                    accel_y=unpacked[2],
                    accel_z=unpacked[3],
                    gyro_x=unpacked[4],
                    gyro_y=unpacked[5],
                    gyro_z=unpacked[6],
                    latitude=unpacked[7],
                    longitude=unpacked[8],
                    ground_speed=unpacked[9],
                    heading=unpacked[10],
                    lead_voltage=unpacked[11]
                ) # type: ignore
                frames.append(frame)
        
        print(f"Successfully parser {len(frames)} frames.")
        return frames

                