import sys
import os
import math
import struct
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QSlider
from PyQt5.QtCore import Qt

class TelemetryPacker:
    FRAME_FORMAT = '<I6h2i2HhH'
    FRAME_SIZE = 32
    @staticmethod
    def pack_frame(timestamp_ms, ax, ay, az, gx, gy, gz, lat, lon, speed, heading, lean):
        return struct.pack(TelemetryPacker.FRAME_FORMAT, int(timestamp_ms), int(ax), int(ay), int(az), int(gx), int(gy), int(gz), int(lat), int(lon), int(speed), int(heading), int(lean), 0)
class SimulatorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("A.T.L.A.S. - Digital Twin Simulator")
        self.resize(500,400)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.title = QLabel("Digital Twin Parameters")
        self.title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 20px;")
        self.layout.addWidget(self.title)
        self.speed_label = QLabel("Speed: 120 km/h")
        self.layout.addWidget(self.speed_label)
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(0, 300)
        self.speed_slider.setValue(120)
        self.speed_slider.valueChanged.connect(lambda v: self.speed_label.setText(f"Speed: {v} km/h"))
        self.layout.addWidget(self.speed_slider)
        self.lean_label = QLabel("Lean Angle: 45°")
        self.layout.addWidget(self.lean_label)
        self.lean_slider = QSlider(Qt.Horizontal)
        self.lean_slider.setRange(0, 60)
        self.lean_slider.setValue(45)
        self.lean_slider.valueChanged.connect(lambda v: self.lean_label.setText(f"Lean Angle: {v}°"))
        self.layout.addWidget(self.lean_slider)
        self.radius_label = QLabel("Track Radius (GPS Spread): 3000")
        self.layout.addWidget(self.radius_label)
        self.radius_slider = QSlider(Qt.Horizontal)
        self.radius_slider.setRange(100, 10000)
        self.radius_slider.setValue(3000)
        self.radius_slider.valueChanged.connect(lambda v: self.radius_label.setText(f"Track Radius (GPS Spread): {v}"))
        self.layout.addWidget(self.radius_slider)
        self.duration_label = QLabel("Lap Duration: 60 seconds")
        self.layout.addWidget(self.duration_label)
        self.duration_slider = QSlider(Qt.Horizontal)
        self.duration_slider.setRange(10, 300)
        self.duration_slider.setValue(60)
        self.duration_slider.valueChanged.connect(lambda v: self.duration_label.setText(f"Lap Duration: {v} seconds"))
        self.layout.addWidget(self.duration_slider)
        self.gen_btn = QPushButton("Generate simulated_lap.dat")
        self.gen_btn.setStyleSheet("""
                font-size: 16px;
                font-weight: bold;
                padding: 12px;
                background-color: #FF5722;
                color: white;
                border-radius: 4px;
                margin-top: 20px;
            """)
        self.gen_btn.clicked.connect(self.generate_data)
        self.layout.addWidget(self.gen_btn)
        self.status_label = QLabel("")
        self.layout.addWidget(self.status_label)

    def generate_data(self):
            speed_cms = int((self.speed_slider.value() / 3.6) * 100)
            max_lean = self.lean_slider.value() * 100
            radius = self.radius_slider.value()
            duration_sec = self.duration_slider.value()

            # ---> THIS IS THE LINE YOU WERE MISSING <---
            frames_count = duration_sec * 100

            dt_ms = 10
            script_dir = os.path.dirname(os.path.abspath(__file__))
            output_file = os.path.join(script_dir, "simulated_lap.dat")

            with open(output_file, 'wb') as f:
                for i in range(frames_count):
                    timestamp_ms = i * dt_ms
                    lean_angle = int(math.sin(i * 0.05) * max_lean)
                    heading = (i * 10) % 36000
                    lat_center = 365842200
                    lon_center = -1217535500
                    lat = lat_center + int(math.sin(i * 0.01) * radius)
                    lon = lon_center + int(math.cos(i * 0.01) * radius)
                    frame_bytes = TelemetryPacker.pack_frame(
                        timestamp_ms, 0, 0, 981, 0, 0, 0,
                        lat, lon, speed_cms, heading, lean_angle
                    )
                    f.write(frame_bytes)

            self.status_label.setText(f"Success! Wrote {frames_count} frames to simulated_lap.dat")
            self.status_label.setStyleSheet("color: #00FF00; font-weight: bold; font-size: 14px;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = SimulatorGUI()
    window.show()
    sys.exit(app.exec_())


