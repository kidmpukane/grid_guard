from logging import error
from dataclasses import dataclass
from helpers.helper_functions import generate_event_id


@dataclass
class SolarPanelFDIRModule:

    def anomaly_detection(self, intent_classification, telemetry, machine_profile, fault_mapping):

        # 1. Fetch relevant values
        event_id = generate_event_id()
        identified_metric = intent_classification["Identified_Metric"]
        machine_type = intent_classification["Machine_Type"]
        # NOTE: Using machine_type to look up data source, assumed successful lookup
        measured_value = telemetry.get(
            machine_type, {}).get(identified_metric, None)
        expected_value = machine_profile.get(identified_metric, None)

        # Handle cases where data is missing
        if measured_value is None or expected_value is None or expected_value == 0:
            print("ERROR: Missing or invalid data for deviation check.")
            exit()

        # 2. Calculate Deviation Percent
        deviation_per = ((measured_value - expected_value) /
                         expected_value) * 100

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

        return anomaly_report
