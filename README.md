**Fancy BLE Scanner – README**

This project is a Bluetooth Low Energy (BLE) Scanner GUI built with Python, PyQt5, and Bleak.
It scans nearby BLE devices in real-time, displays their name, MAC address, and RSSI signal strength in a color-coded bar.

**Features**

Real-time BLE scanning using Bleak
 (cross-platform Bluetooth library).

**Fancy GUI built with PyQt5**
.

Color-coded RSSI bars:

🟢 Green → Strong signal (> -60 dBm)

🟠 Orange → Medium signal (-80 to -60 dBm)

🔴 Red → Weak signal (< -80 dBm)

Automatic refresh every second.

Works on Windows, Linux, and macOS.

Clone the repo (or copy ble_scan_GUI.py).

**Install required dependencies:**
pip install bleak pyqt5

import sys, asyncio, threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QProgressBar
from PyQt5.QtCore import Qt, QTimer
from bleak import BleakScanner
PyQt5 → GUI framework

Bleak → Bluetooth scanning library

Threading + asyncio → Run BLE scanning in background while GUI stays responsive


**Notes**

On Windows, you must run inside a Python venv (Bleak requirement).
On Linux/macOS, run with sudo if devices don’t appear.
RSSI fluctuates, so colors will update dynamically.
