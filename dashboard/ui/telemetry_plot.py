import pyqtgraph as pg
from PyQt5.QtWidgets import QVBoxLayout, QWidget

from core.data_model import TelemetryFrame

class TelemetryPlotWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.plot_widget = pg.PlotWidget(title="A.T.L.A.S. Telemetry (Speed & Lean Angle)")

        self.plot_widget.setBackground("w")
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        self.plot_widget.addLegend()

        self.plot_widget.setLabel('bottom', 'Time (Seconds)', color='white')
        self.plot_widget.setLabel('left', 'Value', color='white')

        self.speed_curve = self.plot_widget.plot(pen=pg.mkPen('#00E5FF', width=2), name="Speed (km/h)")
        self.lean_angle_curve = self.plot_widget.plot(pen=pg.mkPen('#FF00E5', width=2), name="Lean Angle (Degrees)")

        self.layout.addWidget(self.plot_widget)
    
    def update_plot(self, frames):
        if not frames:
            return
        
        times_sec = []
        speeds_kmh = []
        leans_deg = []

        start_time_ms = frames[0].timestamp_ms

        for f in frames:
            t_sec = (f.timestamp_ms - start_time_ms) / 1000.0
            times_sec.append(t_sec)

            s_kmh = f.ground_speed / 100.0
            speeds_kmh.append(s_kmh)

            l_deg = f.lead_voltage / 100.0
            leans_deg.append(l_deg)
        
        self.speed_curve.setData(times_sec, speeds_kmh)
        self.lean_angle_curve.setData(times_sec, leans_deg)
        

