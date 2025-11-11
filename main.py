from core.intent_layer.machine_modules import SolarPanelFDIRModule
from core.input_layer.input_layer import capture_diagnostic_request
from data.machines.machine_profiles import machine_profile, fault_mapping, telemetry

intent_classification = {
    "Asset_ID": "PV_PANEL_09SP823",
    "Machine_Type": "Solar_Panel",
    "Classified_Intent": "Connection_Monitoring",
    "Identified_Metric": "Voltage_V",
    "Time_Window_Hrs": 12,
}


# print(capture_diagnostic_request())
fdir_module = SolarPanelFDIRModule()
print(fdir_module.anomaly_detection(
    intent_classification, telemetry, machine_profile, fault_mapping))
