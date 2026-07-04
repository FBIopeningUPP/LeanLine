import math
from core.data_model import TelemetryFrame

class LapTimer:
        @staticmethod
        def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
            R = 6371000.0
            phi1 = math.radians(lat1)
            phi2 = math.radians(lat2)
            delta_phi = math.radians(lat2 - lat1)
            delta_lambda = math.radians(lon2 - lon1)
            a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            return R * c
        @staticmethod
        def calculate_lap_times(frames: list[TelemetryFrame], finish_lat: float, finish_lon: float, threshold_meters: float = 15.0) -> list[float]:
            lap_times = []
            in_zone = False
            last_time = None
            for f in frames:
                lat = f.latitude / 10000000.0
                lon = f.longitude / 10000000.0
                dist = LapTimer.haversine_distance(lat, lon, finish_lat, finish_lon)
                if dist <= threshold_meters:
                    if not in_zone:
                        in_zone = True
                        curr_time = f.timestamp_ms / 1000.0
                        if last_time is not None:
                            lap_time = curr_time - last_time
                            # Debounce: Ensure lap is > 30s so we don't double trigger at the start line
                            if lap_time > 30.0:
                                lap_times.append(lap_time)
                                last_time = curr_time
                        else:
                            last_time = curr_time
                else:
                    in_zone = False
            return lap_times