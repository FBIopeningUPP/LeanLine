import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog
from core.frame_parser import FrameParser
from ui.telemetry_plot import TelemetryPlotWidget
from ui.gps_map_widget import GpsMapWidget

class AtlasDashboard(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("A.T.L.A.S. - Lean Line")
            self.resize(1024, 768)

            self.central_widget = QWidget()
            self.setCentralWidget(self.central_widget)
            self.layout = QVBoxLayout(self.central_widget)

            self.load_btn = QPushButton("Load Telemetry Binary (.dat)")
            self.load_btn.clicked.connect(self.load_file)
            self.layout.addWidget(self.load_btn)

            self.plot_widget = TelemetryPlotWidget()
            self.layout.addWidget(self.plot_widget)

            self.map_widget = GpsMapWidget()
            self.layout.addWidget(self.map_widget)

        def load_file(self):
            filepath, _ = QFileDialog.getOpenFileName(self, "Select Binary", "", "Data Files (*.dat)")

            if filepath:
                self.setWindowTitle(f"A.T.L.A.S. - {os.path.basename(filepath)}")
                self.load_btn.setText(f"Loaded: {os.path.basename(filepath)}")

                frames = FrameParser.parse_file(filepath)

                self.plot_widget.update_plot(frames)
                self.map_widget.update_map(frames)

if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = AtlasDashboard()
        window.show()
        sys.exit(app.exec_())