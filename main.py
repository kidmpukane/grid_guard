from core.intent_layer.machine_modules import SolarPanelFDIRModule
from core.input_layer.input_layer import capture_diagnostic_request
from data.machines.machine_profiles import machine_profile, fault_mapping, telemetry, solar_panel_fault_log, weather_api


# Enter ID:s PV_PANEL_09SP823

# user_intent = capture_diagnostic_request()
# fdir_module = SolarPanelFDIRModule()
# stage_1 = fdir_module.anomaly_detection(
#     user_intent, telemetry, machine_profile, fault_mapping)
anomaly_report = {
    'event_id': 'PV-748-284-44',
    'fdir_stage': '1_RealTime_Signal_Processor',
    'asset_id': 'PV_PANEL_09SP823',
    'timestamp': '2025-11-06T14:45:33.210Z',
    'anomaly_status': True,
    'anomaly_verification':
        {'fault_type': 'High String Voltage',
         'metric_analysed': 'Voltage_V',
         'measured_value': 350.2,
         'expected_value': 400.0,
         'deviation_percent': -12.45,
         'status_flag': 'Anomaly_Low_Threshold_Violated',
         'tolerance_threshold': '+/-10.0%'
         }}

stage_2 = fdir_module.fault_diagnosis(
    anomaly_report, solar_panel_fault_log, weather_api)
print(stage_2)
