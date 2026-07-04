import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from core.data_model import TelemetryFrame

class GpsMapWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.map_widget = pg.PlotWidget(title="GPS Track Trace")
        self.map_widget.setBackground('#121212')

        self.map_widget.showGrid(x=False, y=False)
        self.map_widget.hideAxis('bottom')
        self.map_widget.hideAxis('left')

        self.map_widget.setAspectLocked(True)

        self.track_curve = self.map_widget.plot(pen=pg.mkPen(color='#00FF00', width=3))

        self.start_point = self.map_widget.plot(pen=None, symbol='0', symbolPen='w', symbolBrush='g', symbolSize=12)

        self.layout.addWidget(self.map_widget) 

    def update_map(self, frames: list[TelemetryFrame]):
        if not frames:
            return

        lons = []
        lats = []

        for f in frames:
            lons.append(f.longitude / 10000000.0)
            lats.append(f.latitude / 10000000.0)
        
        self.track_curve.setData(lons, lats)

        self.start_point.setData([lons[0]], [lats[0]]) 