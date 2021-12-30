import flask
from flask import Flask, jsonify, request
import json
import pickle
from data_input import data_input
import numpy as np

def load_models():
    file_name = "models/model_file.p"
    with open(file_name, "rb") as pickled:
        data = pickle.load(pickled)
        model = data["model"]
    return model

app = Flask(__name__)
@app.route("/predict", methods=["GET"]) #endpoint predict

def predict():
    # stub input features
    # default input
    # x = np.array(data_input).reshape(1,-1)
    
    # input from user to be predicted
    request_json = request.get_json()
    x = request_json["input"]
    x_in = np.array(x).reshape(1,-1)
    
    # load model
    model = load_models()
    prediction = model.predict(x_in)[0]
    response = json.dumps({'Predicted Salary' : prediction})
    return response, 200

if __name__ == "__main__":
    application.run(debug = True)