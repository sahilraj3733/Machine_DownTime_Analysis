from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, f1_score

app = Flask(__name__)
model = None

@app.route('/')
def home():
    return render_template('index.html')

# data uploaing
@app.route('/upload', methods=['POST'])
def upload_data():
    file = request.files['file']
    data = pd.read_csv(file)
    data.to_csv('data/uploaded_data.csv', index=False)
    return jsonify({"message": "File uploaded successfully!"})


# For Training 
@app.route('/train', methods=['POST'])
def train_model():
    global model
    data = pd.read_csv('data/uploaded_data.csv')

    # Dropping unnecessary columns
    data = data.drop(['Date', 'Machine_ID', 'Assembly_Line_No'], axis=1)

    # Mapping Downtime column correctly
    data['Downtime'] = data['Downtime'].map({'No_Machine_Failure': 0, 'Machine_Failure': 1})

    # Fill mean values for missing data
    columns_with_nulls = [col for col in data.columns if data[col].isna().sum() > 0]
    for col in columns_with_nulls:
        data[col] = data[col].fillna(data[col].mean())

   

    X = data.drop("Downtime", axis=1)
    y = data["Downtime"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = DecisionTreeClassifier(max_depth=5,random_state=42)
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)



    # Evaluate model performance
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    # Debug: Check the accuracy and f1 score
    print(f"Accuracy: {accuracy}")
    print(f"F1-Score: {f1}")

    # Save the trained model
    joblib.dump(model, 'app/models/model.pkl')

    # Return the results in the response
    return jsonify({"Accuracy": accuracy, "F1-Score": f1})

@app.route('/predict', methods=['POST'])
def predict():
    global model
    if model is None:
        model = joblib.load('app/models/model.pkl')

    # Get JSON input
    data = request.get_json()

    # Define expected feature names 
    expected_columns = [
        'Hydraulic_Pressure(bar)', 'Coolant_Pressure(bar)', 'Air_System_Pressure(bar)', 'Coolant_Temperature', 
        'Hydraulic_Oil_Temperature(?C)', 'Spindle_Bearing_Temperature(?C)', 'Spindle_Vibration(?m)', 
        'Tool_Vibration(?m)', 'Spindle_Speed(RPM)', 'Voltage(volts)', 'Torque(Nm)', 'Cutting(kN)'
    ]
    
    # Extract features and check for missing data
    features = []
    for column in expected_columns:
        feature_value = data.get(column)
        if feature_value is None:
            return jsonify({"message": f"Missing required feature: {column}"}), 400
        features.append(feature_value)
    
    # Convert features into a pandas DataFrame to match the training format
    input_data = pd.DataFrame([features], columns=expected_columns)

    # Predict using the model
    prediction = model.predict(input_data)[0]
    confidence = model.predict_proba(input_data)[0][prediction]
    print(" d",model.predict_proba(input_data)[0])
    # Prepare the output
    result = {
        "Downtime": "Yes" if prediction == 1 else "No",
        "Confidence": confidence
    }
    print(confidence)
    # Return the JSON response
    return jsonify(result)



if __name__ == '__main__':
    app.run(debug=True)
