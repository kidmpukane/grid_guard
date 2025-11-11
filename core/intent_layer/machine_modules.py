from datetime import datetime
from logging import error
from dataclasses import dataclass
from helpers.helper_functions import generate_event_id


@dataclass
class SolarPanelFDIRModule:

    def anomaly_detection(self, intent_classification, telemetry, machine_profile, fault_mapping):

        # 1. Fetch relevant values
        event_id = generate_event_id()
        identified_metric = intent_classification["identified_metric"]
        machine_type = intent_classification["machine_type"]
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
            "asset_id": intent_classification["asset_id"],
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

    def diagnosis_and_classification(anomaly_report, solar_panel_fault_log, weather_api):
        asset_id = anomaly_report["asset_id"]
        event_id = anomaly_report["event_id"]
        current_fault = anomaly_report["anomaly_verification"]["fault_type"]
        deviation_per = anomaly_report["anomaly_verification"]["deviation_percent"]
        fault_count = 0
        similar_faults = []
        for fault in solar_panel_fault_log:
            historical_faults = fault["fault_type"]
            if current_fault == historical_faults:
                fault_count += 1
                similar_faults.append(fault)
            else:
                fault_count += 0
        # --- TEMPORAL THRESHOLDS (30-Day Window) ---
        ISOLATED_MAX = 2
        RECURRING_MIN = 3
        PERSISTENT_MIN = 10

        isolated = fault_count <= ISOLATED_MAX

        recurring = (fault_count >= RECURRING_MIN) and (
            fault_count < PERSISTENT_MIN)
        persisting = fault_count >= PERSISTENT_MIN

        classification = ""
        severity = ""

        # The order of checks is critical here: check highest severity first.
        if persisting == True:
            # CRITICAL: 10 or more events
            severity = "CRITICAL"
            classification = "Persistent_Critical_Failure"
        elif recurring == True:
            # HIGH: 3 to 9 events
            severity = "HIGH"
            classification = "Re_occurring_Systemic_Fault"
        else:
            # WARNING: 1 or 2 events (The Isolated case)
            severity = "WARNING"
            classification = "Isolated_Transient_Fault"

    # ------------------------------------------------------------------------:
    # ---------------------- Historical_Faults_Context------------------------:
    # ------------------------------------------------------------------------:

        historical_fault_count = 0
        for fault in solar_panel_fault_log:
            if fault:
                historical_fault_count += 1

        similar_anomalies = fault_count

        if similar_faults:
            # Sort by timestamp to ensure chronological order
            sorted_faults = sorted(
                similar_faults, key=lambda x: x['timestamp'])

            last_occurrence = sorted_faults[-1]

        if len(similar_faults) > 1:
            # Sort by timestamp to ensure chronological order
            sorted_faults = sorted(
                similar_faults, key=lambda x: x['timestamp'])

            # Calculate intervals between consecutive events
            intervals = []
            for i in range(1, len(sorted_faults)):
                prev_time = datetime.fromisoformat(
                    sorted_faults[i - 1]['timestamp'].replace('Z', '+00:00'))
                curr_time = datetime.fromisoformat(
                    sorted_faults[i]['timestamp'].replace('Z', '+00:00'))

                # Calculate difference in hours
                interval_hours = (curr_time - prev_time).total_seconds() / 3600
                intervals.append(interval_hours)

            # Calculate average
            average_interval_between_events_hrs = sum(
                intervals) / len(intervals)

    # -------------------------------------------------------------------------------:
    # ---------------------- Environmental_Validation_Context------------------------:
    # -------------------------------------------------------------------------------:

        ambient_temp = weather_api["temperature"]
        weather_context = weather_api["condition"]
        irradiance = weather_api["solar_radiation"]

        if irradiance < 200 or weather_context in ["Rain", "Heavy Cloud"]:
            environmental_interference = True
        else:
            environmental_interference = False

        # Validation_Result
        if environmental_interference:
            validation_result = "Environmental_Influence_Possible"
        else:
            validation_result = "Operational_Condition_Normal"

        impact_factor = abs(deviation_per) / 100

        # -------------------------------------------------------------------------------:
        # ------------------------ Severity_Scoring_Context------------------------------:
        # -------------------------------------------------------------------------------:

        # Recurrence_Weight
        recurrence_weight = fault_count / historical_fault_count

        # Final_Severity_Score
        final_severity_score = (impact_factor * 0.6) + \
            (recurrence_weight * 0.4)

        # Severity_Label
        if final_severity_score < 0.3:
            severity_label = "Low"
        elif final_severity_score < 0.6:
            severity_label = "Moderate"
        elif final_severity_score < 0.8:
            severity_label = "High"
        else:
            severity_label = "Critical"

        return {
            "asset_id": asset_id,

            "isolated": isolated,
            "recurring": recurring,
            "persisting": persisting,
            "severity": severity,

            "fault_context": {
                "fdir_stage": "2_Historical_Contextualiser",
                "recurrence_scan": {
                    "event_id": event_id,
                    "metric_analysed": anomaly_report["anomaly_verification"]["metric_analysed"],
                    "historical_faults_reviewed": historical_fault_count,
                    "similar_anomalies_found": similar_anomalies,
                    "temporal_classification": classification,
                    "last_occurrence_timestamp": last_occurrence['timestamp'],
                    "average_interval_between_events_hrs":
                        f"{average_interval_between_events_hrs:.2f} hours"

                },
                "environmental_validation": {
                    "irradiance_level": irradiance,
                    "ambient_temperature": ambient_temp,
                    "weather_context": weather_context,
                    "environmental_interference": environmental_interference,
                    "validation_result": validation_result
                },
                "severity_scoring": {
                    "impact_factor": impact_factor,
                    "recurrence_weight": recurrence_weight,
                    "final_severity_score": final_severity_score,
                    "severity_label": severity_label
                }
            }
        }

    def root_cause_isolation(intent, anomaly_report, diagnosis_report):
        rt_confidence_score = 0.85  # placeholder
        abs_deviation = ((
            anomaly_report["anomaly_verification"]["deviation_percent"]) * 100) * 100
        return {
            "asset_id": anomaly_report["asset_id"],
            "fdir_stage": "3_diagnostic_isolator",

            "root_cause_diagnosis": {
                "fdir_code": "PV-STRING-V-004",
                "root_cause": diagnosis_report["fault_context"]["recurrence_scan"]["temporal_classification"],
                "isolation_point": intent["sensor_node"],
                "confidence_score": rt_confidence_score,

                "fusion_analysis": {
                    "real_time_deviation": {
                        "measured_value": anomaly_report["anomaly_verification"]["measured_value"],
                        "expected_value": anomaly_report["anomaly_verification"]["expected_value"],
                        "deviation_absolute": abs_deviation,
                        "deviation_percent": anomaly_report["anomaly_verification"]["deviation_percent"]
                    },
                    "historical_pattern": {
                        "similar_anomalies_found": diagnosis_report["fault_context"]["recurrence_scan"]["similar_anomalies_found"],
                        "temporal_classification": diagnosis_report["fault_context"]["recurrence_scan"]["temporal_classification"],
                        "average_interval_between_events_hrs": diagnosis_report["fault_context"]["recurrence_scan"]["average_interval_between_events_hrs"]
                    }
                },

                "diagnostic_rules_applied": [
                    "IF Voltage_String < Dynamic_Baseline_Min AND Irradiance_Normal THEN Root_Cause = Module Degradation or Wiring Fault",
                    "IF Similar_Anomalies_Recurrent THEN Confidence_Score += 0.05"
                ]
            }
        }
