solar_panel = {
    "Asset_ID": "PV_PANEL_ARRAY_09SP823",
    "Machine_Type": "Solar_Panel",
    "Function": "DC Power Generation",
    "Configuration": "20S_5P",
    "Capacity_W": 15000,
    "Voltage_V": 600,

    "Monitoring_Parameters": {
        "P_DC_Out_W": {
            "Unit": "W",
            "Role": "Measure"
        },
        "V_OpenCircuit_V": {
            "Unit": "V",
            "Role": "Measure"
        },
        "Irradiance_W_m2": {
            "Unit": "W/m²",
            "Role": "Input"
        }
    },

    "Operational_Context": {
        "Status": "Active",
        "Mode": "Daytime Operation",
        "Health_Index": 0.96,
        "Uptime_Hours": 7230
    },

    "Ghost_Logs": {
        "PersistentFault": None,
        "PreviousFault": "Low Irradiance",
        "CurrentFault": None,
        "FaultSeverity": "Low",
        "Last_Fault_Timestamp": "2025-09-25T09:00:00Z",
        "Resolved": True
    },

    "Anomaly_Stats": {
        "Mean_Deviation_Output": 0.05,
        "Trend_Severity": "Stable",
        "Recent_Anomalies": 1
    },

    "Adaptive_Context": {
        "Priority_Score": 0.82,
        "Context_Confidence": 0.91,
        "Last_Update": "2025-10-23T09:30:00Z"
    },

    "Sensor_Map": {
        "P_DC_Out_W": "Sensor_PV_001",
        "V_OpenCircuit_V": "Sensor_PV_002",
        "Irradiance_W_m2": "Sensor_PV_003"
    }
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

solar_panel_fault_log = [
    {
        "machine_id": "PV_PANEL_09SP823",
        "fault_type": "Low String Voltage",
        "status": "RESOLVED_TEMPORARY",
        "severity": "WARNING",
        "timestamp": "2025-10-14T12:00:00Z"
    },
    {
        "machine_id": "PV_PANEL_09SP823",
        "fault_type": "Low String Voltage",
        "status": "RESOLVED_TEMPORARY",
        "severity": "WARNING",
        "timestamp": "2025-10-21T11:30:00Z"
    },
    {
        "machine_id": "PV_PANEL_09SP823",
        "fault_type": "Low String Voltage",
        "status": "RESOLVED_TEMPORARY",
        "severity": "WARNING",
        "timestamp": "2025-10-28T10:00:00Z"
    },
    {
        "machine_id": "PV_PANEL_09SP823",
        "fault_type": "Low String Voltage",
        "status": "ACTIVE_PENDING_ACTION",
        "severity": "WARNING",
        "timestamp": "2025-11-03T09:00:00Z"
    },
    {
        "machine_id": "PV_PANEL_09SP823",
        "fault_type": "High String Voltage",
        "status": "RESOLVED_AUTO",
        "severity": "HIGH",
        "timestamp": "2025-11-04T13:15:00Z"
    },
    {
        "machine_id": "PV_PANEL_09SP823",
        "fault_type": "High String Voltage",
        "status": "RESOLVED_AUTO",
        "severity": "HIGH",
        "timestamp": "2025-11-05T14:30:00Z"
    },
    {
        "machine_id": "PV_PANEL_09SP823",
        "fault_type": "High String Voltage",
        "status": "RESOLVED_TEMPORARY",
        "severity": "HIGH",
        "timestamp": "2025-11-07T10:45:00Z"
    },
    {
        "machine_id": "PV_PANEL_09SP823",
        "fault_type": "High String Voltage",
        "status": "ACTIVE_PENDING_ACTION",
        "severity": "HIGH",
        "timestamp": "2025-11-09T09:20:00Z"
    },
    {
        "machine_id": "PV_PANEL_09SP823",
        "fault_type": "High Cell Temperature",
        "status": "RESOLVED_AUTO",
        "severity": "HIGH",
        "timestamp": "2025-11-08T18:45:00Z"
    },
    {
        "machine_id": "PV_PANEL_09SP823",
        "fault_type": "High Cell Temperature",
        "status": "RESOLVED_AUTO",
        "severity": "HIGH",
        "timestamp": "2025-11-08T18:55:00Z"
    },
    {
        "machine_id": "PV_PANEL_09SP823",
        "fault_type": "Inverter Communication Loss",
        "status": "RESOLVED_AUTO",
        "severity": "CRITICAL",
        "timestamp": "2025-11-09T14:20:00Z"
    },
    {
        "machine_id": "PV_PANEL_09SP823",
        "fault_type": "Ground Fault Detected",
        "status": "ACTIVE_PENDING_ACTION",
        "severity": "CRITICAL",
        "timestamp": "2025-11-10T08:15:00Z"
    },
    {
        "machine_id": "PV_PANEL_09SP823",
        "fault_type": "Low Power Output",
        "status": "RESOLVED_TEMPORARY",
        "severity": "WARNING",
        "timestamp": "2025-11-10T10:30:00Z"
    },
    {
        "machine_id": "PV_PANEL_09SP823",
        "fault_type": "Panel Shading Detected",
        "status": "ACTIVE",
        "severity": "LOW",
        "timestamp": "2025-11-10T11:00:00Z"
    }
]

weather_api = {
    "temperature": 31,           # °C
    # Could be: "Rain", "Heavy Cloud", "Clear Sky", etc.
    "condition": "Clear Sky",
    "solar_radiation": 780       # W/m² (irradiance level)
}
