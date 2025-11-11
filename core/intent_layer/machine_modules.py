from dataclasses import dataclass
from logging import error


@dataclass
class SolarPanelModule:
    pass


# --- 2. Mock Data Inputs (Simulating API/DB Calls) ---
# Mock Intent Package from Stage 0 (User Query: "Voltage is low")
intent_classification = {
    "Asset_ID": "PV_PANEL_09SP823",
    "Machine_Type": "Solar_Panel",
    "Classified_Intent": "Connection_Monitoring",
    "Identified_Metric": "Voltage_V",
    "Time_Window_Hrs": 12,
}

# Mock Telemetry Data (Actual, Measured Value)
# Simulating a 350V reading (Expected: 400V)
telemetry = {
    "Solar_Panel": {
        "Voltage_V": 350.2,
        "Current_A": 8.9,
        "Panel_Temp_C": 34,
    }
}

# Fault Type Mapping based on Deviation Percentage
fault_mapping = {
    "Voltage_V": [
        {"condition": "deviation_per < -20",
            "fault_type": "Critical Low Voltage", "severity": "CRITICAL"},
        {"condition": "deviation_per < -10",
            "fault_type": "Low String Voltage", "severity": "WARNING"},
        {"condition": "deviation_per > 20",
            "fault_type": "Critical High Voltage", "severity": "CRITICAL"},
        {"condition": "deviation_per > 10",
            "fault_type": "High String Voltage", "severity": "HIGH"},
    ],

    "Current_A": [
        {"condition": "deviation_per > 30",
            "fault_type": "Critical Overcurrent", "severity": "CRITICAL"},
        {"condition": "deviation_per > 15",
            "fault_type": "Overcurrent Detected", "severity": "HIGH"},
        {"condition": "deviation_per < -15",
            "fault_type": "Low String Current", "severity": "WARNING"},
    ],

    "Temperature_C": [
        {"condition": "deviation_per > 25 or measured_value > 85", "fault_type": "Critical High Temperature",
         "severity": "CRITICAL"},
        {"condition": "deviation_per > 15 or measured_value > 75", "fault_type": "High Cell Temperature",
         "severity": "HIGH"},
        {"condition": "deviation_per < -20 or measured_value < 0", "fault_type": "Low Operating Temperature",
         "severity": "LOW"},
    ],

    "Power_W": [
        {"condition": "deviation_per < -30",
            "fault_type": "Critical Low Power", "severity": "CRITICAL"},
        {"condition": "deviation_per < -15",
            "fault_type": "Low Power Output", "severity": "WARNING"},
        {"condition": "deviation_per > 20",
            "fault_type": "Power Surge Detected", "severity": "HIGH"},
    ],

    "Efficiency_%": [
        {"condition": "deviation_per < -25",
            "fault_type": "Critical Efficiency Loss", "severity": "CRITICAL"},
        {"condition": "deviation_per < -10",
            "fault_type": "Panel Efficiency Degradation", "severity": "WARNING"},
    ],

    "Irradiance_W/m2": [
        {"condition": "deviation_per < -40",
            "fault_type": "Severe Shading", "severity": "HIGH"},
        {"condition": "deviation_per < -20",
            "fault_type": "Panel Shading Detected", "severity": "LOW"},
        {"condition": "deviation_per < -15",
            "fault_type": "Soiling Detected", "severity": "LOW"},
    ]
}

# Mock CT Model / Machine Profile (Expected Value)
machine_profile = {
    "Voltage_V": 400.0,  # The expected/nominal reading (Dynamic Baseline)
    "Current_A": 9.2,
}

# --- 3. Stage 1 Processing Logic ---

# 1. Fetch relevant values
event_id = generate_event_id()
identified_metric = intent_classification["Identified_Metric"]
machine_type = intent_classification["Machine_Type"]

# NOTE: Using machine_type to look up data source, assumed successful lookup
measured_value = telemetry.get(machine_type, {}).get(identified_metric, None)
expected_value = machine_profile.get(identified_metric, None)


# Handle cases where data is missing
if measured_value is None or expected_value is None or expected_value == 0:
    print("ERROR: Missing or invalid data for deviation check.")
    exit()

# 2. Calculate Deviation Percent
deviation_per = ((measured_value - expected_value) / expected_value) * 100

# 3. FIX: Define a realistic Threshold and Check against Absolute Value
# In electrical engineering, 10% is often the trigger point for a Warning/Anomaly Flag.
THRESHOLD_PERCENT = 10.0

if abs(deviation_per) >= THRESHOLD_PERCENT:
    anomaly_status = True
    if deviation_per > 0:
        status_flag = "Anomaly_High_Threshold_Violated"
    else:
        status_flag = "Anomaly_Low_Threshold_Violated"
else:
    anomaly_status = False
    status_flag = "Within_Tolerance_Nominal"

# ---  Applying Mapping to Your Anomaly Report ---
metric = identified_metric

# Get fault mapping for this metric
metric_faults = fault_mapping.get(metric, [])

fault_type = "Unknown Fault"

for fault_rule in metric_faults:
    condition = fault_rule["condition"]
    fault_type = fault_rule["fault_type"]


# --- 4. Final Output Generation (Stage 1 JSON) ---

anomaly_report = {
    "event_id": event_id,
    "fdir_stage": "1_RealTime_Signal_Processor",
    "asset_id": intent_classification["Asset_ID"],
    "timestamp": "2025-11-06T14:45:33.210Z",  # Mock timestamp for structure
    "anomaly_status": anomaly_status,  # True/False
    "anomaly_verification": {
        "fault_type": fault_type,
        "metric_analysed": identified_metric,
        "measured_value": measured_value,
        "expected_value": expected_value,
        # Rounded for JSON readability
        "deviation_percent": round(deviation_per, 2),
        "status_flag": status_flag,
        "tolerance_threshold": f"+/-{THRESHOLD_PERCENT}%"
    }
}

# # --- Output Results ---
# print("--- STAGE 1 EXECUTION RESULTS ---")
# print(f"Measured Value: {measured_value} V")
# print(f"Expected Value: {expected_value} V")
# print(f"Deviation: {round(deviation_per, 2)}%")
# print(f"Threshold Used: +/-{THRESHOLD_PERCENT}%")
# print(f"ANOMALY STATUS: {status_flag}\n")
#
# print("--- FINAL STAGE 1 JSON OUTPUT ---")
# import json
# print(json.dumps(anomaly_report, indent=4))
