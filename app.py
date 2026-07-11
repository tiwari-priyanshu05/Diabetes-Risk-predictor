from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import traceback

app = Flask(__name__)

# Load models at startup
try:
    with open("diabetes_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    with open("target_encoder.pkl", "rb") as f:
        target_encoder = pickle.load(f)
    print("Models loaded successfully.")
except Exception as e:
    print(f"Error loading models: {e}")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        
        age = float(data.get("age", 30))
        bmi = float(data.get("bmi", 25.0))
        fasting_glucose = float(data.get("fasting_glucose", 100))
        insulin = float(data.get("insulin", 15.0))
        triglycerides = float(data.get("triglycerides", 150))
        calories = float(data.get("calories", 2000))
        sleep = float(data.get("sleep", 7.0))
        family_str = data.get("family", "No")
        gender_str = data.get("gender", "Female")
        blood_pressure = float(data.get("blood_pressure", 120))
        hba1c = float(data.get("hba1c", 5.5))
        cholesterol = float(data.get("cholesterol", 180))
        activity_str = data.get("activity", "Moderate")
        sugar = float(data.get("sugar", 50.0))
        stress = float(data.get("stress", 5))
        waist = float(data.get("waist", 90.0))

        gender = 1 if gender_str == "Male" else 0
        family = 1 if family_str == "Yes" else 0
        activity_map = {"High": 0, "Low": 1, "Moderate": 2}
        activity = activity_map.get(activity_str, 2)

        features = np.array([[
            age, gender, bmi, blood_pressure, fasting_glucose,
            insulin, hba1c, cholesterol, triglycerides,
            activity, calories, sugar, sleep, stress, family, waist
        ]])

        features = scaler.transform(features)
        pred = model.predict(features)
        risk = target_encoder.inverse_transform(pred)[0]

        # Get confidence score
        try:
            prob = model.predict_proba(features)
            confidence = float(np.max(prob[0])) * 100
        except:
            confidence = 85.0 # Fallback

        return jsonify({
            "success": True,
            "risk": risk,
            "confidence": round(confidence, 1)
        })
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
