
# from flask import Flask, request, jsonify
# import numpy as np
# import joblib
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# # Load pre-trained models
# model_1 = joblib.load("plan_1_model.pkl")
# model_2 = joblib.load("plan_2_model.pkl")
# scaler = joblib.load("scaler_model.pkl")

# @app.route("/predict", methods=["POST"])
# def predict():
#     try:
#         data = request.json

#         # Convert categorical fields properly
#         marital_status = 1 if data["MaritalStatus"] == "Married" else 0  

#         # Ensure all fields have valid numeric values
#         age = int(data["Age"])
#         income = float(data["Income"])
#         num_children = int(data["NumChildren"]) if data["NumChildren"] else 0
#         age_child_1 = float(data["AgeChild1"]) if data["AgeChild1"] else 0.0
#         age_child_2 = float(data["AgeChild2"]) if data["AgeChild2"] else 0.0

#         # Convert input to the correct feature order
#         features = np.array([[ 
#             age, marital_status, income, num_children, age_child_1, age_child_2
#         ]])

#         # Scale input features
#         features_scaled = scaler.transform(features)

#         # Predict the best plans
#         best_plan_1 = int(model_1.predict(features_scaled)[0])  # Convert to int
#         best_plan_2 = int(model_2.predict(features_scaled)[0])  # Convert to int

#         return jsonify({"Best Plan 1": best_plan_1, "Best Plan 2": best_plan_2})

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500  # Return error message

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, request, jsonify
import numpy as np
import joblib
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load pre-trained models
model_1 = joblib.load("plan_1_model.pkl")
model_2 = joblib.load("plan_2_model.pkl")
scaler = joblib.load("scaler_model.pkl")

# Mapping numerical predictions to actual plan names
plan_mapping = {
    0: "Smart Privilege",
    1: "Smart Platina Supreme",
    2: "Smart Shield",
    3: "Smart Platina Assure",
    4: "Fortune Builder",
    5: "Retire Smart",
}

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json

        # Convert categorical fields properly
        marital_status = 1 if data["MaritalStatus"] == "Married" else 0  

        # Ensure all fields have valid numeric values
        age = int(data["Age"])
        income = float(data["Income"])
        num_children = int(data["NumChildren"]) if data["NumChildren"] else 0
        age_child_1 = float(data["AgeChild1"]) if data["AgeChild1"] else 0.0
        age_child_2 = float(data["AgeChild2"]) if data["AgeChild2"] else 0.0

        # Convert input to the correct feature order
        features = np.array([[ 
            age, marital_status, income, num_children, age_child_1, age_child_2
        ]])

        # Scale input features
        features_scaled = scaler.transform(features)

        # Predict the best plans
        best_plan_1 = int(model_1.predict(features_scaled)[0])  # Convert to int
        best_plan_2 = int(model_2.predict(features_scaled)[0])  # Convert to int

        # Map predictions to plan names
        plan_1_name = plan_mapping.get(best_plan_1, "Unknown Plan")
        plan_2_name = plan_mapping.get(best_plan_2, "Unknown Plan")

        return jsonify({"Best Plan 1": plan_1_name, "Best Plan 2": plan_2_name})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return error message

if __name__ == "__main__":
    app.run(debug=True)
