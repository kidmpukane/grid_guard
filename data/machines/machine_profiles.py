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
