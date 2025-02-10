from flask import Flask, render_template, request, jsonify,url_for,redirect
import joblib
import numpy as np

app = Flask(__name__)

# Load the trained model
model = joblib.load('heart.pkl')
model1=joblib.load('diabetes.pkl')
scaler = joblib.load('scaler.pkl')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/heart-disease-prediction',methods=['GET'])
def heart_disease_prediction():
    return render_template('prediction.html')

@app.route('/diabetes-prediction',methods=['GET'])
def diabetes_prediction():
    return render_template('diabetes.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form
    features = np.array([
        float(data['Age']),
        int(data['Sex']),
        int(data['ChestPainType']),
        float(data['RestingBP']),
        float(data['Cholesterol']),
        int(data['FastingBS']),
        int(data['RestingECG']),
        float(data['MaxHR']),
        int(data['ExerciseAngina']),
        float(data['Oldpeak']),
        int(data['ST_Slope'])
    ]).reshape(1, -1)

    # Make a prediction
    prediction = model.predict(features)
    if prediction[0] == 1:
        result = "Heart Disease Found"
        care_instructions = (
            "1. Maintain a healthy weight.<br>"
            "2. Exercise regularly (30 minutes/day).<br>"
            "3. Eat a heart-healthy diet: more fruits, vegetables, and whole grains.<br>"
            "4. Reduce sodium, sugar, and saturated fat intake.<br>"
            "5. Manage stress and avoid smoking.<br>"
            "6. Take prescribed medications and monitor your blood pressure.<br>"
            "7. Visit your doctor regularly for check-ups."
        )
    else:
        result = "No Heart Disease Found"
        care_instructions = (
            "1. Continue living a healthy lifestyle.<br>"
            "2. Maintain a balanced diet.<br>"
            "3. Stay physically active.<br>"
            "4. Monitor your health and visit your doctor for regular check-ups."
        )

    # Pass the result to the result.html template
    return render_template('result.html', prediction=result, care=care_instructions)


@app.route('/diabetesPredict', methods=['POST'])
def diabetesPredict():
    data = request.form
    features = np.array([
        int(data['pregnancie']),
        int(data['glucose']),
        int(data['bloodpressure']),
        int(data['skinthickness']),
        int(data['insulin']),
        float(data['bmi']),
        float(data['diabetespedigreefunction']),
        int(data['age'])
    ]).reshape(1, -1)
    print(features)

    input_scaled = scaler.transform(features)



    prediction = model1.predict(input_scaled)
    if prediction[0] == 1:
        result = "Diabetes Found"
        care_instructions = (
            "1.Maintain a Healthy Weight to reduce risk.<br>"
            "2.Eat a Balanced Diet with fiber, protein, and healthy fats.<br>"
            "3.Limit Sugar & Processed Carbs to prevent insulin resistance.<br>"
            "4.Stay Active with regular exercise (at least 30 minutes daily).<br>"
            "5.Drink Plenty of Water and avoid sugary drinks.<br>"
            "6.Get Enough Sleep (7–9 hours) to regulate hormones.<br>"
            "7.Manage Stress to prevent blood sugar spikes.<br>"
            "8.Have Regular Checkups to monitor blood sugar levels.<br>"
            "9.Avoid Smoking & Excess Alcohol for better metabolic health.<br>"
            "10.Stay Consistent with a healthy lifestyle.<br>"
        )
    else:
        result="No Diabetes Found"
        care_instructions=(
            "1.Eat a Balanced Diet – Include whole foods, fiber, and healthy fats.<br>"
            "2.Stay Active – Exercise at least 30 minutes daily.<br>"
            "3.Drink Enough Water – Stay hydrated and avoid sugary drinks.<br>"
            "3.Get Quality Sleep – Aim for 7–9 hours per night.<br>"
            "4.Manage Stress – Practice mindfulness, meditation, or hobbies.<br>"
            "5.Maintain a Healthy Weight – Keep BMI in a healthy range.<br>"
            "6.Limit Processed Foods & Sugar – Prevent future health issues.<br>"
            "7.Avoid Smoking & Limit Alcohol – Protect overall well-being.<br>"
            "8.Have Regular Checkups – Monitor blood pressure, cholesterol, and sugar levels.<br>"
            "9.Stay Consistent – Build sustainable healthy habits for long-term wellness.<br>"
        )

    return render_template('result.html', prediction=result, care=care_instructions)

@app.route('/result')
def result():
    # Get the prediction and care instructions from the query parameters
    prediction = request.args.get('prediction')
    care = request.args.get('care')
    return render_template('result.html', prediction=prediction, care=care)



        

if __name__ == '__main__':
    app.run(debug=True,port=5003,host='0.0.0.0')
