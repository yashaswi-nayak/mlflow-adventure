# Imports
from flask import Flask, jsonify, request
import mlflow as mlflow
import pickle
import pandas as pd

# Global variables, model and scaler loaded once on start
app = Flask(__name__)
model = None
scaler = None

# Function to load objects
def load_model():
    global model, scaler
    try:
        model = mlflow.pyfunc.load_model("./")     # Should be pointing to the folder where model is present
        with open("./scaler-knn.pkl", "rb") as fp:
            scaler = pickle.load(fp)
        print("Loaded Model and Scaler.")
    except Exception as e:
        print("Error: Loading objects", e)

# API /health - Check if app is running
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"App": "OK"})

# API /predict -  Prediction of model
@app.route('/predict', methods=['POST'])
def predict():
    global model, scaler
    try:
        data = request.json
        datadf = pd.DataFrame.from_dict(data)
        datadf = scaler.transform(datadf)
        result = model.predict(datadf)
        return jsonify({"result": result.tolist()})
    except Exception as e:
        print("Error: Issue with prediction.", e)


if __name__ == "__main__":
    load_model()
    app.run(host="0.0.0.0", port=5000, debug=True)
