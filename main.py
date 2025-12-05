import json
import time
import sys
from core.intent_layer.machine_modules import SolarPanelFDIRModule
from core.input_layer.input_layer import capture_diagnostic_request
from data.machines.machine_profiles import (
    machine_profile,
    fault_mapping,
    telemetry,
    solar_panel_fault_log,
    weather_api
)


# ------------------------- Helper Functions ------------------------- #

def thinking(text="Processing", steps=3, delay=0.5):
    """Simple CLI animation to simulate processing/thinking"""
    for i in range(steps):
        sys.stdout.write(f"\r{text}{'.' * (i+1)}")
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")


def print_stage(title, data):
    """Pretty-print the stage JSON with a header and thinking animation"""
    print(f"\n=== {title} ===")
    thinking("Thinking")
    print(json.dumps(data, indent=4))


# ------------------------- Main Program ------------------------- #

def main():
    # Capture user intent / diagnostic directive
    user_intent = capture_diagnostic_request()

    # Initialize FDIR module
    fdir_module = SolarPanelFDIRModule()

    # ---- Stage 1: Anomaly Detection ----
    stage_1 = fdir_module.anomaly_detection(
        user_intent, telemetry, machine_profile, fault_mapping
    )
    print_stage("Stage 1: Anomaly Detection", stage_1)

    # ---- Stage 2: Diagnosis & Classification ----
    stage_2 = fdir_module.diagnosis_and_classification(
        stage_1, solar_panel_fault_log, weather_api
    )
    print_stage("Stage 2: Diagnosis & Classification", stage_2)

    # ---- Stage 3: Root Cause Isolation ----
    stage_3 = fdir_module.root_cause_isolation(
        user_intent, stage_1, stage_2
    )
    print_stage("Stage 3: Root Cause Isolation", stage_3)


# ------------------------- Entry Point ------------------------- #

if __name__ == "__main__":
    main()


def tool_recommendation():
    return {
        "Recommended_Tool": {
            "Tool_Name": "TOOL_IV_CURVE_MODEL",
            "Tool_Type": "Diagnostic",
            "Execution_Priority": "High",
            "Justification": "Tool can isolate string-level voltage anomalies using I-V curve analysis"
        }
    }
