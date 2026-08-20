# 🤖 Machine Learning Model | AI-Powered Smart Irrigation System

This document describes the machine-learning architecture, model selection, training workflow, inference process, persistence, fallback behavior, and deployment strategy used by the AI-Powered Smart Irrigation System.

---

## 📑 Table of Contents

1. [Overview](#-overview)
2. [ML Objective](#-ml-objective)
3. [Problem Formulation](#-problem-formulation)
4. [Model Architecture](#-model-architecture)
5. [Why Random Forest](#-why-random-forest)
6. [Input and Output](#-input-and-output)
7. [Training Pipeline](#-training-pipeline)
8. [Dataset Requirements](#-dataset-requirements)
9. [Data Preprocessing](#-data-preprocessing)
10. [Train/Validation Split](#-trainvalidation-split)
11. [Model Training](#-model-training)
12. [Model Evaluation](#-model-evaluation)
13. [Model Serialization](#-model-serialization)
14. [Inference Pipeline](#-inference-pipeline)
15. [Decision Logic](#-decision-logic)
16. [Fallback Strategy](#-fallback-strategy)
17. [Model Explainability](#-model-explainability)
18. [Model Lifecycle](#-model-lifecycle)
19. [Future Improvements](#-future-improvements)
20. [Conclusion](#-conclusion)

---

# 🌱 Overview

The machine-learning subsystem is responsible for determining whether irrigation should be activated based on current environmental conditions and near-term weather forecasts.

The model combines:

- Current temperature
- Current humidity
- Current soil moisture
- Forecast rainfall
- Rain probability
- Forecast temperature
- Forecast humidity

The model produces a binary irrigation recommendation:

```text
0 → Irrigation not required
1 → Irrigation required
```

The ML subsystem is integrated into the backend rather than running directly on the ESP32.

```text
ESP32
  │
  │ Sensor telemetry
  ▼
Flask Backend
  │
  ├── Local Sensor Data
  │
  ├── Weather Forecast
  │
  └── Historical / Derived Features
           │
           ▼
      Random Forest
           │
           ▼
    Irrigation Decision
           │
           ▼
      Relay Command
```

---

# 🎯 ML Objective

The primary objective is to learn the relationship between environmental conditions and irrigation requirements.

The model approximates:

$$
Y = f(X)
$$

where:

- $X$ = environmental and weather features
- $Y$ = irrigation requirement

The desired output is:

$$
Y \in \{0,1\}
$$

with:

```text
Y = 0 → Do not irrigate
Y = 1 → Irrigate
```

The model is therefore a **binary classification problem**.

---

# 🧮 Problem Formulation

For a given time $t$, define the environmental state:

$$
S_t =
[
T_t,
H_t,
SM_t
]
$$

and forecast state:

$$
W_t =
[
R_t,
P_t,
T_f,
H_f
]
$$

The complete feature vector is:

$$
X_t = [S_t,W_t]
$$

Therefore:

$$
X_t =
[
T_t,
H_t,
SM_t,
R_t,
P_t,
T_{f,t},
H_{f,t}
]
$$

The classifier computes:

$$
\hat{Y}_t =
f_{\mathrm{RF}}(X_t)
$$

where:

$$
\hat{Y}_t \in \{0,1\}
$$

---

# 🌲 Model Architecture

The system uses:

```text
Scikit-Learn RandomForestClassifier
```

Conceptually:

```text
                         Input Features
                              │
       ┌──────────────────────┼──────────────────────┐
       │                      │                      │
       ▼                      ▼                      ▼
 Temperature             Humidity             Soil Moisture
       │                      │                      │
       └──────────────────────┼──────────────────────┘
                              │
       ┌──────────────────────┼──────────────────────┐
       │                      │                      │
       ▼                      ▼                      ▼
    Rainfall           Rain Probability       Forecast Temp
                              │
                              ▼
                     Forecast Humidity
                              │
                              ▼
                 ┌─────────────────────┐
                 │   Random Forest     │
                 │                     │
                 │  Tree 1             │
                 │  Tree 2             │
                 │  Tree 3             │
                 │  ...                │
                 │  Tree N             │
                 └──────────┬──────────┘
                            │
                       Majority Vote
                            │
                            ▼
                   Irrigation Decision
                       0 / 1
```

A Random Forest is an ensemble of decision trees.

Each tree generates a prediction, and the forest combines the predictions to determine the final class.

---

# 🤔 Why Random Forest?

Random Forest is suitable for the current prototype because the input data contains nonlinear relationships.

For example:

```text
Low soil moisture
+
High temperature
+
Low rainfall probability
=
High irrigation requirement
```

However:

```text
Low soil moisture
+
High rain probability
+
High forecast rainfall
=
Potentially lower irrigation requirement
```

These interactions are not necessarily well represented by a simple linear model.

Random Forest can naturally model such nonlinear feature interactions.

---

## Advantages

### 1. Nonlinear Relationships

Random Forest can capture complex relationships between environmental variables.

### 2. Mixed Feature Behavior

The model can work with continuous numerical features without requiring complex transformations.

### 3. Robustness

Ensembling multiple decision trees generally makes the model less sensitive to individual training examples.

### 4. Interpretability

Feature importance can provide insight into which environmental variables influence predictions.

### 5. Easy Deployment

A trained Random Forest can be serialized using `joblib` and loaded directly by the Flask backend.

---

# 📥 Input and Output

## Input

The model receives seven features:

```text
[
    temperature,
    humidity,
    soil_moisture,
    rainfall,
    rain_probability,
    forecast_temperature,
    forecast_humidity
]
```

---

## Output

The classifier produces:

```text
0 → Irrigation OFF
1 → Irrigation ON
```

The backend converts this prediction into a final relay command after applying manual override and safety logic.

---

# 🧩 Feature Matrix

For $n$ observations, the input matrix is:

$$
X \in \mathbb{R}^{n \times 7}
$$

Example:

```text
X =
[
 [28.4, 72.1, 34.7, 0.0, 20.0, 29.1, 70.0],
 [31.2, 58.0, 24.0, 0.0, 10.0, 32.0, 55.0],
 [26.8, 81.0, 48.0, 5.2, 85.0, 25.4, 84.0]
]
```

The target vector is:

$$
y \in \{0,1\}^n
$$

Example:

```text
y =
[
 0,
 1,
 0
]
```

---

# 🏋️ Training Pipeline

The complete training workflow is:

```text
                 Raw Dataset
                      │
                      ▼
              Data Validation
                      │
                      ▼
              Missing-Value Check
                      │
                      ▼
              Feature Selection
                      │
                      ▼
             Target Separation
                      │
                      ▼
           Train / Validation Split
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
      Training Set           Validation Set
          │                       │
          ▼                       │
   Random Forest Fit              │
          │                       │
          └───────────┬───────────┘
                      ▼
                Model Evaluation
                      │
                      ▼
             Model Serialization
                      │
                      ▼
          irrigation_model.pkl
```

---

# 📊 Dataset Requirements

The dataset should contain the same seven features used during inference.

Recommended columns:

```text
temperature
humidity
soil_moisture
rainfall
rain_probability
forecast_temperature
forecast_humidity
irrigation_required
```

Example:

| temperature | humidity | soil_moisture | rainfall | rain_probability | forecast_temperature | forecast_humidity | irrigation_required |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 31.2 | 58 | 24 | 0.0 | 10 | 32.0 | 55 | 1 |
| 27.4 | 74 | 46 | 4.5 | 80 | 26.8 | 78 | 0 |
| 29.1 | 68 | 38 | 0.2 | 25 | 30.0 | 65 | 0 |
| 33.5 | 49 | 18 | 0.0 | 5 | 34.2 | 46 | 1 |

---

# ⚠️ Training Data Quality

The model's quality depends heavily on the quality of its training data.

The dataset should eventually be based on:

- Real sensor measurements
- Real weather observations
- Crop-specific irrigation requirements
- Soil characteristics
- Field observations
- Actual irrigation events
- Agronomic recommendations

A synthetically generated dataset may be useful for software development and pipeline testing, but it should not be treated as equivalent to validated field data.

---

# 🧹 Data Preprocessing

Before training, the dataset should be checked for:

```text
Missing values
Duplicate records
Impossible values
Sensor outliers
Incorrect timestamps
Invalid weather values
Incorrect labels
```

Example acceptable ranges may include:

```text
Temperature       → physically plausible field range
Humidity          → 0–100 %
Soil Moisture     → 0–100 %
Rain Probability  → 0–100 %
Rainfall          → ≥ 0 mm
```

The precise physical limits should be defined according to the sensor, crop, field, and weather source.

---

# 🔢 Target Construction

The target column represents whether irrigation is required.

```text
irrigation_required
```

Example:

```text
0 → No irrigation
1 → Irrigation required
```

The target should ideally be based on an explicit irrigation policy or validated agronomic labels rather than arbitrary thresholds.

---

# ✂️ Train/Validation Split

The dataset is divided into:

```text
Training Data
Validation Data
```

For example:

```text
80% → Training
20% → Validation
```

Conceptually:

```text
Full Dataset
     │
     ├─────────────── 80% ────────────────┐
     │                                    │
     ▼                                    ▼
Training Set                         Validation Set
     │                                    │
     ▼                                    │
Random Forest                            │
     │                                    │
     └──────────────┬─────────────────────┘
                    ▼
              Model Evaluation
```

For time-series agricultural data, a chronological split is often preferable to a purely random split because it better represents deployment on future observations.

---

# 🌳 Model Training

The Random Forest is trained using the seven input features.

Conceptually:

```python
model.fit(train_X, train_y)
```

A typical implementation can use parameters such as:

```python
RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
```

The exact hyperparameters should be tuned using validation data rather than assumed to be universally optimal.

---

# ⚙️ Hyperparameters

Important Random Forest hyperparameters include:

| Parameter | Purpose |
|---|---|
| `n_estimators` | Number of decision trees |
| `max_depth` | Maximum tree depth |
| `min_samples_split` | Minimum samples required to split |
| `min_samples_leaf` | Minimum samples at a leaf |
| `max_features` | Number of features considered per split |
| `class_weight` | Handles class imbalance |
| `random_state` | Reproducibility |

---

# ⚖️ Class Imbalance

Irrigation datasets may contain more `OFF` observations than `ON` observations.

For example:

```text
OFF = 85%
ON  = 15%
```

A model could achieve high accuracy simply by predicting `OFF` most of the time.

Therefore, the following should be monitored:

```text
Precision
Recall
F1-score
Confusion Matrix
```

Class weighting or resampling can also be considered when appropriate.

---

# 📈 Model Evaluation

The trained model should be evaluated using unseen validation data.

Important metrics include:

## Accuracy

$$
Accuracy =
\frac{TP+TN}{TP+TN+FP+FN}
$$

---

## Precision

$$
Precision =
\frac{TP}{TP+FP}
$$

---

## Recall

$$
Recall =
\frac{TP}{TP+FN}
$$

---

## F1 Score

$$
F1 =
2
\frac{Precision \times Recall}
{Precision + Recall}
$$

---

# 🚿 Irrigation-Specific Error Analysis

The two major errors have different operational consequences.

## False Positive

```text
Model predicts:
Irrigation ON

Actual:
Irrigation not required
```

Potential consequence:

```text
Water wastage
Energy consumption
Unnecessary pump operation
```

---

## False Negative

```text
Model predicts:
Irrigation OFF

Actual:
Irrigation required
```

Potential consequence:

```text
Insufficient irrigation
Plant water stress
Crop damage
```

For this reason, accuracy alone should not determine whether the model is suitable.

---

# 📊 Confusion Matrix

The classification results can be represented as:

```text
                    Actual
                 OFF       ON
              ┌────────┬────────┐
Predicted OFF │   TN   │   FN   │
              ├────────┼────────┤
Predicted ON  │   FP   │   TP   │
              └────────┴────────┘
```

The preferred balance between FP and FN depends on crop, season, soil, water availability, and irrigation policy.

---

# 💾 Model Serialization

After successful training and validation, the model is saved using `joblib`.

Conceptual workflow:

```text
Random Forest
     │
     ▼
joblib.dump()
     │
     ▼
irrigation_model.pkl
```

The resulting file becomes the backend inference artifact.

---

# 📂 Model Artifact

Expected location:

```text
machine-learning/
└── irrigation_model.pkl
```

or, depending on the project structure:

```text
backend/
└── ml/
    └── irrigation_model.pkl
```

The exact location should remain consistent between training and deployment.

---

# 🚀 Inference Pipeline

During normal operation:

```text
ESP32 Telemetry
       │
       ▼
Flask API
       │
       ▼
Weather Forecast
       │
       ▼
Feature Construction
       │
       ▼
7-Feature Vector
       │
       ▼
Loaded Random Forest
       │
       ▼
Prediction
       │
       ▼
Override / Safety Layer
       │
       ▼
Relay Command
```

---

# 🔍 Inference Example

Input:

```text
temperature          = 31.2
humidity             = 58.0
soil_moisture        = 24.0
rainfall             = 0.0
rain_probability     = 10.0
forecast_temperature = 32.0
forecast_humidity    = 55.0
```

Feature vector:

```text
[
    31.2,
    58.0,
    24.0,
    0.0,
    10.0,
    32.0,
    55.0
]
```

Model output:

```text
1
```

Interpretation:

```text
Irrigation required
```

The backend then applies the control-mode and safety logic before generating the final relay command.

---

# 🎛️ Decision Layer

The ML prediction is **not necessarily the final actuator command**.

The complete decision hierarchy is:

```text
                 ML Prediction
                      │
                      ▼
              Manual Override?
                 /        \
               YES         NO
                │           │
                ▼           ▼
          Override State  ML Result
                │           │
                └─────┬─────┘
                      ▼
                Safety Checks
                      │
                      ▼
                Final Command
```

Mathematically:

$$
U_t =
\begin{cases}
U_{\text{manual}}, & \text{manual override active}\\
Y_t, & \text{ML inference successful}\\
U_{\text{safe}}, & \text{ML inference failed}
\end{cases}
$$

---

# 🛡️ ML Failure Fallback

The system should never depend exclusively on the `.pkl` file for safe operation.

If model loading fails:

```text
irrigation_model.pkl
        │
        ▼
     Load Error
        │
        ▼
Safety Controller
```

Example safety policy:

```text
IF soil_moisture < 30%
    → Pump ON
ELSE
    → Pump OFF
```

This is a fallback control rule, not a replacement for a properly trained production model.

---

# 🌦️ Weather Failure and ML

If the weather API is unavailable, the backend can continue operating using defined fallback values.

Conceptually:

```text
Weather API
    │
    ├── SUCCESS → Real forecast
    │
    └── FAILURE → Safe fallback values
                         │
                         ▼
                  Feature Vector
                         │
                         ▼
                    Random Forest
```

The system should log whenever fallback weather data is used.

---

# 🔬 Model Explainability

Random Forest provides useful diagnostic information such as feature importance.

Conceptually:

```text
Feature Importance
        │
        ├── Soil Moisture
        ├── Rain Probability
        ├── Temperature
        ├── Rainfall
        ├── Forecast Temperature
        ├── Humidity
        └── Forecast Humidity
```

The actual ranking must be calculated from the trained model and should not be assumed beforehand.

Feature importance can help answer:

> Which environmental variables are most influential in irrigation predictions?

---

# 🧠 AI Suggestion Generation

The binary model output can be converted into a human-readable message.

Example:

```text
Prediction = 1

AI Suggestion:
"Irrigation recommended based on current environmental
conditions and forecast data."
```

For more informative explanations, the backend can combine:

```text
Prediction
+
Feature values
+
Control mode
+
Weather status
```

Example:

```text
"Irrigation recommended because soil moisture is low
and forecast rainfall probability is limited."
```

These explanations should describe the actual decision logic rather than inventing causal reasoning that the model did not establish.

---

# 🔄 Model Lifecycle

The complete model lifecycle is:

```text
                 ┌───────────────┐
                 │ Dataset       │
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │ Validation    │
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │ Training      │
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │ Evaluation    │
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │ Serialization │
                 └───────┬───────┘
                         ↓
              irrigation_model.pkl
                         │
                         ▼
                 ┌───────────────┐
                 │ Deployment    │
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │ Inference     │
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │ Monitoring    │
                 └───────┬───────┘
                         │
                         └──────→ Retraining
```

---

# 🔁 Continuous Learning Architecture

Once sufficient real-world telemetry has been collected, the system can support model improvement.

```text
ESP32
  ↓
Telemetry
  ↓
SQLite
  ↓
Historical Dataset
  ↓
Data Validation
  ↓
Labeling
  ↓
Retraining
  ↓
Evaluation
  ↓
New Model
  ↓
Deployment
```

A model should only be promoted to production if its validation performance and operational behavior meet predefined criteria.

---

# 🚀 Future ML Improvements

The current Random Forest architecture can be extended with:

### Gradient Boosting

```text
XGBoost
LightGBM
CatBoost
```

### Time-Series Models

```text
LSTM
GRU
Temporal CNN
Temporal Fusion Transformer
```

### Regression

Instead of predicting only irrigation ON/OFF:

```text
Predict soil moisture after N hours
```

### Reinforcement Learning

The controller could eventually optimize:

```text
Water consumption
+
Crop water availability
+
Pump energy consumption
```

---

# 🌾 Crop-Specific Models

Different crops have different water requirements.

A future system could support:

```text
Crop Type
     ↓
Crop-Specific Parameters
     ↓
Feature Engineering
     ↓
Crop-Specific Model
     ↓
Irrigation Decision
```

This can improve generalization compared with treating every agricultural field identically.

---

# 🏁 Conclusion

The machine-learning subsystem transforms environmental and weather data into an irrigation recommendation.

The complete ML pipeline is:

```text
Sensor Data
     +
Weather Forecast
     ↓
Feature Vector
     ↓
Random Forest Classifier
     ↓
Binary Prediction
     ↓
Override / Safety Layer
     ↓
Final Relay Command
```

The current architecture is intentionally simple enough for a practical prototype while providing a clear path toward:

- Real field datasets
- Better validation
- Automated retraining
- Time-series prediction
- Crop-specific intelligence
- Edge AI
- Predictive irrigation optimization
