import asyncio
import logging
from datetime import datetime
from bleak import BleakScanner

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler("ble_scan.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# Store last seen devices and RSSI
seen_devices = {}

def detection_callback(device, advertisement_data):
    name = device.name or "Unknown"
    address = device.address
    rssi = advertisement_data.rssi  # <-- Works with bleak >=0.22
    seen_devices[address] = (name, rssi)

async def scan_and_log():
    seen_devices.clear()
    scanner = BleakScanner(detection_callback)
    logging.info("Scanning for BLE devices...")
    
    try:
        await scanner.start()
        await asyncio.sleep(2.0)
        await scanner.stop()

        if not seen_devices:
            logging.info("No BLE devices found.")
        else:
            for address, (name, rssi) in seen_devices.items():
                logging.info(f"{name} ({address}) RSSI: {rssi} dBm")

    except Exception as e:
        logging.error(f"Error during scan: {e}")

async def main_loop():
    logging.info("BLE Scanner Started (Logging every 10 seconds)... Press Ctrl+C to stop.")
    try:
        while True:
            await scan_and_log()
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logging.info("BLE Scanner stopped by user.")

if __name__ == "__main__":
    asyncio.run(main_loop())
