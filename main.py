from core.intent_layer.machine_modules import SolarPanelFDIRModule
from core.input_layer.input_layer import capture_diagnostic_request
from data.machines.machine_profiles import machine_profile, fault_mapping, telemetry


# Enter ID:s PV_PANEL_09SP823

user_intent = capture_diagnostic_request()
fdir_module = SolarPanelFDIRModule()
stage_1 = fdir_module.anomaly_detection(
    user_intent, telemetry, machine_profile, fault_mapping)
print(stage_1)
