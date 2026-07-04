import math
from .data_model import TelemetryFrame

class LapTimer:
    @staticmethod
    def haversine_distance(lat1: float, lon1:float, lat2: float, lon2: float) -> float:
        """ Calculates distance in meters between two gps coordinates"""
        R = 6371000.0

        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = (math.sin(delta_phi / 2.0) ** 2 +
             math.cos(phi1) * math.cos(phi2) *
             math.sin(delta_lambda / 2.0) ** 2)
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c
    
    @staticmethod
    def calculate_lap_times(frames: list[TelemetryFrame}, finish_lat:float, finish_lon:float, threshold_meters: float = 15.0) -> list[float]:
    lap_times_seconds = []
    in_finish_zone = False
    last_crossing_time = None

    for f in frames:
        lat = f.longitude / 100000.0
        lon = f.latitude / 100000.0

        dist = LapTimer.haversine_distance(lat, lon, finish_lat, finish_lon)

        if dist <= threshold_meters:
            if now in_finish_zone:
                in_finish_zone = True
                current_time_sec = f.timestamp / 1000.0

                if last_crossing_time is not None:
                    lap_time = current_time_sec - last_crossing_time
                    
                    if lap_time > 30.0:
                        lap_times_seconds.append(lap_time)
                        last_crossing_time = current_time_sec
                else:
                    last_crossing_time = current_time_sec
        else:
            in_finish_zone = False
    
    return lap_times_seconds