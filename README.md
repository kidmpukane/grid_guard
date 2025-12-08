# **README — GridGuard: Modular Reasoning Engine for Smart Grids**

## **Overview**

GridGuard is a modular reasoning engine designed to analyze diagnostic queries within smart-grid environments.
It follows a fully decomposed, microservice-style architecture where each stage of the reasoning pipeline is an independent, swappable unit.

The system ingests a natural-language directive, interprets the intent, maps it to machine-specific diagnostic modules, and executes a fault-detection routine using structured machine profiles.

This project implements the **first working build**, containing:

* Input Layer
* Intent Classifier
* Intent Layer / Machine Diagnostics
* Machine Profile Loader
* Core Diagnostic Execution
* Complete FTIR trace-logging (every stage prints its reasoning)

---

## **Current Capabilities**

✔ Accepts free-form diagnostic instructions
✔ Maps asset ID, machine type, and sensor node to internal modules
✔ Uses a hybrid rule-based diagnostic engine
✔ Runs FTIR (Fault Tree – Isolation – Recommendation) reasoning
✔ Prints reasoning trace at every step
✔ Modular design → each layer can scale independently

---

# **How the System Runs**

Open a terminal in the project directory and run:

```bash
py main.py
```

You will be prompted with four inputs:

```
🧭 Enter diagnostic directive (e.g., 'Check voltage on Solar Panel'):
🏗️ Enter Asset Node ID (Machine ID):
⚙️ Enter Machine Type (e.g., 'Solar_Panel', 'Wind_Turbine', etc.):
🔌 Enter Sensor Node linked to Asset:
```

Example:

```
Check voltage on Solar Panel
CS-PV-01235
Solar_Panel
S-PV-35
```

The engine will then:

1. Parse and validate the directive
2. Identify machine class & diagnostic module
3. Load relevant machine profile from `/data/machines`
4. Execute rule-based diagnostics
5. Print FTIR trace logs
6. Produce a final recommendation or warning

---

# **Project Structure**

```
grid_guard/
│   main.py
│   TODO
│   AVA_(GridGuard).png   <-- architecture diagram
│   README                <-- this file
│   __init__.py
│
├── core/
│   ├── input_layer/
│   │     input_layer.py
│   │
│   ├── intent_classification/
│   │     intent_classsifier.py
│   │     intent_data/intent_mappings.py
│   │
│   ├── intent_layer/
│   │     machine_modules.py
│   │
│   ├── contextual_memory/      (reserved for future builds)
│   ├── permission_checker/     (reserved)
│   ├── response_generator/     (reserved)
│   └── tool_execution/         (reserved)
│
├── data/
│   └── machines/
│         machine_profiles.py
│
├── helpers/
│   helper_functions.py
│
├── models/                     (empty placeholder — for ML models)
└── services/                   (generic services or utilities)
```

---

# **Architecture (High-Level)**

### **1. Input Layer**

Takes raw user instructions and creates a structured request object.
Performs minor cleaning, validation, and logs the raw intent.

### **2. Intent Classification**

Classifies the instruction into diagnostic categories
(e.g., *check voltage*, *inspect temperature*, *look up device status*).

Uses simple rule-matching and mapping tables (expandable).

### **3. Intent Layer / Machine Diagnostic Module**

Loads the correct machine profile and diagnostic rules based on:

* Machine ID
* Machine type
* Sensor node
* Instruction intent

Executes FTIR logic.

### **4. Data Layer**

Holds all machine profiles.
Profiles define:

* thresholds
* normal operating ranges
* fault signatures
* recommended actions

This is the core of your domain knowledge base.

### **5. Trace & Output**

Every stage prints structured logs so developers can see how the engine reasons.
This transparency is the backbone of AVA/GridGuard’s design philosophy.

---

# **Extending the System (Roadmap)**

This build is the foundation. Next phases:

### 🔹 **Tool Selector**

Route requests to tool-specific executors (ML models, simulators, calculators).

### 🔹 **Permission Checker**

Restrict operations based on user, role, and machine capability.

### 🔹 **Response Generator**

Transform raw diagnostic outputs into natural-language explanations.

### 🔹 **Contextual Memory**

Retain recent previous queries, asset context, and anomaly history.

### 🔹 **Model Layer**

Host advanced predictive models (e.g., anomaly detection, time-series forecasts).

---

# **Contributing / Modifying**

Because every subsystem is modular, you can replace components by editing:

| Layer             | Swap file                              |
| ----------------- | -------------------------------------- |
| Input processing  | `core/input_layer/input_layer.py`      |
| Intent logic      | `core/intent_classification/`          |
| Machine reasoning | `core/intent_layer/machine_modules.py` |
| Machine profiles  | `data/machines/machine_profiles.py`    |

Each part acts like its own micro-service in a full distributed architecture.

---

# **Status**

This is the first operational build of the GridGuard reasoning engine.
It handles structured diagnostics and prints transparent FTIR reasoning trace logs.

Future versions will layer on more intelligence, more autonomy, and richer safety tooling.
