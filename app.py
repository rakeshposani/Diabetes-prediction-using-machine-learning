from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load model
with open("model.pkl", "rb") as file:
    model = pickle.load(file)

# Load scaler
with open("scaler.pkl", "rb") as file:
    scaler = pickle.load(file)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    try:
        data = [
            float(request.form["Pregnancies"]),
            float(request.form["Glucose"]),
            float(request.form["BloodPressure"]),
            float(request.form["SkinThickness"]),
            float(request.form["Insulin"]),
            float(request.form["BMI"]),
            float(request.form["DiabetesPedigreeFunction"]),
            float(request.form["Age"])
        ]

        data = np.array(data).reshape(1, -1)
        data = scaler.transform(data)

        prediction = model.predict(data)

        if prediction[0] == 1:
            result = "🩺 The Person is Diabetic"
        else:
            result = "✅ The Person is Not Diabetic"

        return render_template("index.html", prediction=result)

    except Exception as e:
        return render_template("index.html", prediction=str(e))


if __name__ == "__main__":
    app.run(debug=True)