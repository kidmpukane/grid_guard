import json
from datetime import datetime


def capture_diagnostic_request():
    """Captures and structures a predictive diagnostic command."""
    directive = input(
        "🧭 Enter diagnostic directive (e.g., 'run vibration analysis'): ")
    classified_intent = directive  # Placeholder for actual intent classification
    asset_node = input("🏗️ Enter Asset Node ID (Machine ID): ")
    machine_type = input(
        "⚙️ Enter Machine Type (e.g., 'Solar_Panel', 'Wind_Turbine', etc.): ")
    sensor_node = input(f"🔌 Enter Sensor Node linked to Asset {asset_node}: ")

    # Timestamp current diagnostic window
    window_timestamp = datetime.now().strftime("%H:%M:%S")

    # Build standardized GridCard request packet
    diagnostic_packet = {
        "asset_id": asset_node,
        "machine_type": machine_type,
        "sensor_node": f"S_{sensor_node}",
        "prompt": directive,
        "classified_intent": classified_intent,
        "identified_metric": "Voltage_V",
        "time_window_hrs": window_timestamp,
    }

    return diagnostic_packet
