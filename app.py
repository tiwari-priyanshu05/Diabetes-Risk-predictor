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

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "").lower()
        
        # Advanced rule-based chatbot intelligence for diabetes
        default_response = "I'm DiaPredict Assistance! Ask me about diabetes symptoms, causes, diet, types, or prevention."
        
        responses = {
            "symptom": "Common symptoms of diabetes include frequent urination, excessive thirst, extreme hunger, unexplained weight loss, fatigue, blurry vision, and slow-healing sores.",
            "sign": "Common symptoms of diabetes include frequent urination, excessive thirst, extreme hunger, unexplained weight loss, fatigue, blurry vision, and slow-healing sores.",
            "cure": "Currently, there is no known cure for diabetes. However, it can be effectively managed and sometimes put into remission through diet, exercise, weight loss, and medication.",
            "type 1": "Type 1 diabetes is an autoimmune condition where the body attacks insulin-producing cells in the pancreas. It usually requires lifelong insulin therapy.",
            "type i": "Type 1 diabetes is an autoimmune condition where the body attacks insulin-producing cells in the pancreas. It usually requires lifelong insulin therapy.",
            "type 2": "Type 2 diabetes is a condition where the body becomes resistant to insulin or doesn't make enough. It is often linked to lifestyle factors like diet and weight.",
            "type ii": "Type 2 diabetes is a condition where the body becomes resistant to insulin or doesn't make enough. It is often linked to lifestyle factors like diet and weight.",
            "diet": "A healthy diabetes diet focuses on whole grains, lean proteins, healthy fats, and plenty of vegetables. It's important to limit refined carbs, sugary drinks, and highly processed foods.",
            "food": "A healthy diabetes diet focuses on whole grains, lean proteins, healthy fats, and plenty of vegetables. It's important to limit refined carbs, sugary drinks, and highly processed foods.",
            "eat": "A healthy diabetes diet focuses on whole grains, lean proteins, healthy fats, and plenty of vegetables. It's important to limit refined carbs, sugary drinks, and highly processed foods.",
            "prevent": "You can reduce your risk of Type 2 diabetes by maintaining a healthy weight, exercising regularly (like 150 minutes a week), eating a balanced diet, and avoiding smoking.",
            "avoid": "You can reduce your risk of Type 2 diabetes by maintaining a healthy weight, exercising regularly (like 150 minutes a week), eating a balanced diet, and avoiding smoking.",
            "sugar": "Blood sugar (glucose) is your body's main source of energy. In diabetes, the body struggles to move glucose from the blood into cells, leading to high blood sugar levels.",
            "glucose": "Blood sugar (glucose) is your body's main source of energy. In diabetes, the body struggles to move glucose from the blood into cells, leading to high blood sugar levels.",
            "cause": "Type 1 is caused by an autoimmune reaction. Type 2 develops over time and is heavily linked to genetics, obesity, and physical inactivity.",
            "what is diabetes": "Diabetes is a chronic health condition that affects how your body turns food into energy. Your body either doesn't make enough insulin or can't use it as well as it should.",
            "hello": "Hello! I'm Aura, your DiaPredict Assistant. Ask me anything about diabetes!",
            "hi": "Hello! I'm Aura, your DiaPredict Assistant. Ask me anything about diabetes!"
        }
        
        response = None
        for key, val in responses.items():
            if key in user_message:
                response = val
                break
                
        if not response:
            if "?" in user_message:
                response = "That's a great question, but my current knowledge base is focused primarily on diabetes symptoms, types, diet, causes, and prevention. Could you rephrase your question around those topics?"
            else:
                response = default_response

        return jsonify({
            "success": True,
            "response": response
        })
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
