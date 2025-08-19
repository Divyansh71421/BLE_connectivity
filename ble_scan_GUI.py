import sys
import asyncio
import threading
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QProgressBar
)
from PyQt5.QtCore import Qt, QTimer
from bleak import BleakScanner


class BLEScannerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fancy BLE Scanner")
        self.setGeometry(200, 200, 700, 400)

        self.devices = {}  # {address: {"name": name, "rssi": rssi}}

        # Table setup
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Name", "Address", "RSSI Signal"])
        self.table.horizontalHeader().setStretchLastSection(True)

        layout = QVBoxLayout()
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Timer to refresh UI every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_table)
        self.timer.start(1000)

        # Start BLE scanning in another thread
        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self.start_ble_loop, daemon=True).start()

    def start_ble_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.scan_ble())

    async def scan_ble(self):
        def detection_callback(device, advertisement_data):
            rssi = advertisement_data.rssi
            name = device.name or "Unknown"
            self.devices[device.address] = {"name": name, "rssi": rssi}

        scanner = BleakScanner(detection_callback)
        await scanner.start()
        while True:
            await asyncio.sleep(0.1)

    def update_table(self):
        self.table.setRowCount(len(self.devices))
        for row, (address, data) in enumerate(self.devices.items()):
            name_item = QTableWidgetItem(data["name"])
            name_item.setFlags(Qt.ItemIsEnabled)

            addr_item = QTableWidgetItem(address)
            addr_item.setFlags(Qt.ItemIsEnabled)

            # RSSI Progress Bar
            rssi_bar = QProgressBar()
            rssi_val = data["rssi"] if data["rssi"] is not None else -100
            rssi_bar.setMinimum(-100)
            rssi_bar.setMaximum(-30)
            rssi_bar.setValue(rssi_val)

            # Color coding
            if rssi_val > -60:
                rssi_bar.setStyleSheet("QProgressBar::chunk { background-color: green; }")
            elif rssi_val > -80:
                rssi_bar.setStyleSheet("QProgressBar::chunk { background-color: orange; }")
            else:
                rssi_bar.setStyleSheet("QProgressBar::chunk { background-color: red; }")

            self.table.setItem(row, 0, name_item)
            self.table.setItem(row, 1, addr_item)
            self.table.setCellWidget(row, 2, rssi_bar)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BLEScannerGUI()
    window.show()
    sys.exit(app.exec_())
