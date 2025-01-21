# Downtime Prediction Web Application

## Overview
This project provides a web application for predicting machine downtime based on input features. The application uses a pre-trained machine learning model and Flask for backend services. Users can submit machine parameters in JSON format to receive predictions about potential downtime along with confidence levels.

## Features
- **Model Training**: Train a `DecisionTreeClassifier` model using your dataset.
- **Downtime Prediction**: Predict machine downtime with confidence scores.
- **JSON Input/Output**: Accepts and returns data in JSON format for seamless integration.

## Setup Instructions

### Prerequisites
- Python 3.9 or higher
- Required Python libraries:
  * Flask
  * scikit-learn
  * joblib

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/downtime-prediction.git
   cd downtime-prediction
   
2. Install the dependencies:
```bash
pip install -r requirements.txt
```
### Run the Application
1. Start the Flask server:
```bash
python app.py
```
2. Open your browser and navigate to http://127.0.0.1:5000.
## API Endpoints
### 1. Train Model
**Endpoint**: `/train`  
**Method**: `POST`

No input is required to train the model.

**Response Example**:
```json
{
  "message": "Model trained successfully!"
}
```
### 2. Predict Downtime
**Endpoint:** `/predict`
**Method**: `POST`

**Request Example:**

```json
{
  "Hydraulic_Pressure(bar)": 100,
  "Coolant_Pressure(bar)": 200,
  "Air_System_Pressure(bar)": 300,
  "Coolant_Temperature": 25,
  "Hydraulic_Oil_Temperature(?C)": 50,
  "Spindle_Bearing_Temperature(?C)": 60,
  "Spindle_Vibration(?m)": 0.5,
  "Tool_Vibration(?m)": 0.3,
  "Spindle_Speed(RPM)": 2000,
  "Voltage(volts)": 220,
  "Torque(Nm)": 50,
  "Cutting(kN)": 0.3
}


```
**Response Example:**
``` json
{
  "Downtime": "Yes",
  "Confidence": 0.85
}
```
## Model Details
- Type: DecisionTreeClassifier
- Library: scikit-learn
### Features:
- Hydraulic Pressure
- Coolant Pressure
- Air System Pressure
- Coolant Temperature
- Hydraulic Oil Temperature
- Spindle Bearing Temperature
- Spindle Vibration
- Tool Vibration
- Spindle Speed
- Voltage
- Torque
- Cutting
## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests for improvements.


