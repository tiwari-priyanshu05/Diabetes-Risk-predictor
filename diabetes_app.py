
import streamlit as st
import pickle
import numpy as np

st.set_page_config(
    page_title="Diabetes Risk Prediction",
    page_icon="🩺",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

html, body, [class*="css"]{
    font-family:'Poppins',sans-serif;
}

.stApp{
background:
radial-gradient(circle at top left,#5B21B6 0%,transparent 35%),
radial-gradient(circle at bottom right,#0891B2 0%,transparent 30%),
linear-gradient(135deg,#090B1A,#111827,#0F172A);
color:white;
}

.block-container{
padding-top:2rem;
}

.glass{
background:rgba(255,255,255,0.08);
border:1px solid rgba(255,255,255,0.15);
backdrop-filter:blur(12px);
padding:20px;
border-radius:20px;
box-shadow:0 0 30px rgba(0,212,255,.15);
}

div.stButton>button{
width:100%;
height:60px;
border-radius:18px;
background:linear-gradient(90deg,#6C63FF,#00D4FF);
color:white;
font-size:20px;
font-weight:bold;
border:none;
box-shadow:0 0 20px #00D4FF;
}

div.stButton>button:hover{
transform:scale(1.02);
}

[data-testid="stSidebar"]{
background:#0B1026;
}

h1,h2,h3{
color:#F8FAFC;
}
</style>
""", unsafe_allow_html=True)

with open("diabetes_model.pkl","rb") as f:
    model=pickle.load(f)

with open("scaler.pkl","rb") as f:
    scaler=pickle.load(f)

with open("target_encoder.pkl","rb") as f:
    target_encoder=pickle.load(f)

st.sidebar.title("🩺 DiaPredict")
st.sidebar.markdown("### AI Powered Health Screening")
st.sidebar.markdown("---")
st.sidebar.info("""✨ WHY CHOOSE DIAPREDICT

⚡ Instant Prediction

Get diabetes risk analysis in seconds.

🧠 AI-Powered Analysis

Advanced machine learning for reliable insights.

🔒 Privacy First

Your health information is processed securely.

📈 Early Detection

Supports timely awareness and preventive care.""")
st.sidebar.markdown("---")
st.sidebar.info("""
***OUR DEVELOPERS***

Madiha Khan

Priyanshu Tiwari

Anushka Srivastava

Prakhar Dwivedi

       B.Tech AI & ML
""")

st.markdown("""<div class="glass" style="text-align:center;">""", unsafe_allow_html=True)
st.title("🩺 Diabetes Risk Prediction")
st.write("Your journey toward proactive health starts here. Complete the assessment for an intelligent diabetes risk evaluation")
st.markdown("</div>",unsafe_allow_html=True)

col1,col2=st.columns(2)

with col1:
    age=st.number_input("👤 Age",1,120,30)
    bmi=st.number_input("⚖️ BMI",value=25.0)
    fasting_glucose=st.number_input("🍬 Fasting Glucose",value=100)
    insulin=st.number_input("💉 Insulin",value=15.0)
    triglycerides=st.number_input("🧪 Triglycerides",value=150)
    calories=st.number_input("🍽 Daily Calories",value=2000)
    sleep=st.number_input("😴 Sleep Hours",value=7.0)
    family=st.selectbox("👨‍👩‍👧 Family History",["No","Yes"])

with col2:
    gender=st.selectbox("⚧ Gender",["Female","Male"])
    blood_pressure=st.number_input("🩸 Blood Pressure",value=120)
    hba1c=st.number_input("🧬 HbA1c",value=5.5)
    cholesterol=st.number_input("❤️ Cholesterol",value=180)
    activity=st.selectbox("🏃 Physical Activity",["Low","Moderate","High"])
    sugar=st.number_input("🍫 Sugar Intake",value=50.0)
    stress=st.slider("😰 Stress Level",1,10,5)
    waist=st.number_input("📏 Waist Circumference",value=90.0)

gender=1 if gender=="Male" else 0
family=1 if family=="Yes" else 0
activity_map={"High":0,"Low":1,"Moderate":2}
activity=activity_map[activity]

if st.button("🚀 Show Diabetes Risk"):
    features=np.array([[
        age,gender,bmi,blood_pressure,fasting_glucose,
        insulin,hba1c,cholesterol,triglycerides,
        activity,calories,sugar,sleep,stress,family,waist
    ]])

    features=scaler.transform(features)
    pred=model.predict(features)
    risk=target_encoder.inverse_transform(pred)[0]
    st.write("DiaPredict  Analysis:", risk)

    st.markdown("---")

    if risk == "Low Risk":
        st.success("🟢 LOW RISK")
        st.progress(30)
        st.info("""### 🌿 Great News!
Your current health profile indicates a *low risk of diabetes*.

*To stay healthy:*
- 🥗 Continue eating a balanced and nutritious diet.
- 🏃 Stay physically active for at least *30 minutes daily*.
- 💧 Drink plenty of water and maintain a healthy weight.
- 🩺 Schedule routine health checkups to monitor your well-being.

*Remember:* Prevention is always better than treatment. Keep up your healthy lifestyle!""")

    elif risk == "Prediabetes":
        st.warning("🟡 PREDIABETES")
        st.progress(60)
        st.info("""### ⚠️ You're at Risk
Your health profile suggests you may be in the *prediabetes stage*, where blood sugar levels are higher than normal but not yet diabetic.

*Recommended Actions:*
- 🍎 Reduce sugary foods and refined carbohydrates.
- 🚶 Exercise for *150 minutes per week*.
- ⚖️ Maintain a healthy body weight.
- 🩸 Monitor your blood glucose levels regularly.
- 👨‍⚕️ Consider consulting a healthcare professional for personalized guidance.

*Early lifestyle changes can significantly reduce the risk of developing Type 2 Diabetes.*""")

    elif risk == "High Risk":
        st.error("🔴 HIGH RISK")
        st.progress(90)
        st.info("""### 🚨 Immediate Attention Recommended
Your health profile indicates a *high risk of diabetes*.

*Please consider the following:*
- 🏥 Consult a qualified healthcare professional as soon as possible.
- 🩸 Get diagnostic tests such as *Fasting Blood Sugar (FBS)* and *HbA1c*.
- 🥗 Begin adopting a diabetes-friendly diet under medical guidance.
- 🚶 Incorporate regular physical activity as advised by your doctor.
- 💊 Follow prescribed medications or treatment plans if recommended.

*This assessment is AI-generated and should not replace professional medical diagnosis.*""")

st.markdown("---")
st.caption("🌌 Galaxy Theme • Developed by Madiha Khan")
