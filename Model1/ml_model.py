
import pandas as pd
import pickle
with open('thyroid_symptoms_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)


def predict_thyroid_risk(input_data):

    prediction = model.predict(input_data)

    importances = model.feature_importances_
    feature_names = input_data.columns
    contributions = dict(zip(feature_names, importances))

    description = f"Based on the provided symptoms, the predicted risk level is '{prediction[0]}'."

    return prediction[0], contributions, description
