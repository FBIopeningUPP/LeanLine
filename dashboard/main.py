import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog, QLabel

# Import all our custom modules
from core.frame_parser import FrameParser
from ui.telemetry_plot import TelemetryPlotWidget
from ui.gps_map_widget import GpsMapWidget
from core.lap_timer import LapTimer

class AtlasDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("A.T.L.A.S. - Lean Line")
        self.resize(1024, 768)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

            # 1. Load Button
        self.load_btn = QPushButton("Load Telemetry Binary (.dat)")
        self.load_btn.setStyleSheet("""
                QPushButton {
                    font-size: 16px; font-weight: bold; padding: 12px;
                    background-color: #2196F3; color: white; border-radius: 4px;
                }
                QPushButton:hover { background-color: #1976D2; }
            """)
        self.load_btn.clicked.connect(self.load_file)
        self.layout.addWidget(self.load_btn)

            # 2. Lap Time Label (Bright green LCD text)
        self.lap_label = QLabel("Lap Times: Waiting for data...")
        self.lap_label.setStyleSheet("""
                QLabel {
                    font-size: 20px; font-weight: bold; color: #00FF00;
                    background-color: #121212; padding: 10px; border-radius: 4px;
                }
            """)
        self.layout.addWidget(self.lap_label)

            # 3. Telemetry Graph Widget
        self.plot_widget = TelemetryPlotWidget()
        self.layout.addWidget(self.plot_widget)

            # 4. GPS Map Widget
        self.map_widget = GpsMapWidget()
        self.layout.addWidget(self.map_widget)

    def load_file(self):
        start_dir = os.path.join(os.path.dirname(__file__), '..', 'simulator')
        if not os.path.exists(start_dir):
            start_dir = os.getcwd()

        filepath, _ = QFileDialog.getOpenFileName(self, "Select A.T.L.A.S Binary", start_dir, "Data Files (*.dat)")

        if filepath:
            self.setWindowTitle(f"A.T.L.A.S. - {os.path.basename(filepath)}")

                # Parse the binary data
            frames = FrameParser.parse_file(filepath)

                # Update the Visual Widgets
            self.plot_widget.update_plot(frames)
            self.map_widget.update_map(frames)

                # Calculate Lap Times
            if frames:
                    # Use the very first GPS coordinate in the file as the "Start/Finish Line"
                start_lat = frames[0].latitude / 10000000.0
                start_lon = frames[0].longitude / 10000000.0

                laps = LapTimer.calculate_lap_times(frames, start_lat, start_lon)

                if laps:
                        lap_text = " | ".join([f"Lap {i+1}: {lap:.2f}s" for i, lap in enumerate(laps)])
                else:
                    lap_text = "No full laps completed."

                self.lap_label.setText(f"Lap Times: {lap_text}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = AtlasDashboard()
    window.show()
    sys.exit(app.exec_())