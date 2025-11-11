import json
from datetime import datetime


def capture_diagnostic_request():
    """Captures and structures a predictive diagnostic command."""
    directive = input(
        "🧭 Enter diagnostic directive (e.g., 'run vibration analysis'): ")
    asset_node = input("🏗️ Enter Asset Node ID (Machine ID): ")
    sensor_node = input(f"🔌 Enter Sensor Node linked to Asset {asset_node}: ")

    # Timestamp current diagnostic window
    window_timestamp = datetime.now().strftime("%H:%M:%S")

    # Build standardized GridCard request packet
    diagnostic_packet = {
        "directive": directive,
        "asset_node": asset_node,
        "sensor_node": f"S_{sensor_node}",
        "window_timestamp": window_timestamp,
    }

    return diagnostic_packet
