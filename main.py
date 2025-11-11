from core.input_layer.input_layer import capture_diagnostic_request
from data.machines.machine_profiles import machine_profile, fault_mapping

intent_classification = {
    "Asset_ID": "PV_PANEL_09SP823",
    "Machine_Type": "Solar_Panel",
    "Classified_Intent": "Connection_Monitoring",
    "Identified_Metric": "Voltage_V",
    "Time_Window_Hrs": 12,
}

print(machine_profile, fault_mapping)


# print(capture_diagnostic_request())
# fdir_module = SolarPanelFDIRModule()
# anomaly_report = fdir_module.anomaly_detection(
#     intent_classification, telemetry, machine_profile, fault_mapping)

# print(anomaly_report(intent_classification,
#       telemetry, machine_profile, fault_mapping))
