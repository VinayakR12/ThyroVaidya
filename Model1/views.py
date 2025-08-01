import pandas as pd
import numpy as np
from django.shortcuts import render, redirect
from .forms import PredictionForm
from .ml_model import predict_thyroid_risk

def risk_level_description(predicted_risk_level):
        if predicted_risk_level == 2:
            return (
                "Your thyroid risk level is assessed as High, indicating a significant likelihood of thyroid dysfunction. This situation requires immediate attention. I strongly recommend consulting your healthcare provider promptly for a thorough evaluation and potential testing."
                "Early detection and intervention are critical in managing thyroid-related conditions effectively. Please keep a detailed record of your symptoms to discuss during your consultation. Your health is a top priority, and taking proactive steps can lead to better outcomes.")

        elif predicted_risk_level == 1:
            return ("Your thyroid risk level suggests a Medium possibility of thyroid dysfunction."
                    "While this does not indicate a severe issue at this moment, it is important to take this risk seriously. I recommend scheduling a thyroid test to verify your thyroid function, as this can provide valuable insights."
                    "In the meantime, maintaining a balanced diet and engaging in regular physical activity can support your overall health. Staying vigilant about your health is key to effectively managing potential risks.")

        else:  # Low risk level
            return ("Your thyroid risk level is identified as Low, indicating a low chance of thyroid dysfunction. "
                    "While this is a positive sign, it is essential to continue monitoring your health regularly. I encourage you to maintain a healthy lifestyle, including a balanced diet and regular exercise."
                    "Routine check-ups with your healthcare provider are vital to monitor any changes in your thyroid function over time.")


def index(request):
    if request.method == "POST":
        form = PredictionForm(request.POST)
        if form.is_valid():
            # Prepare input data for the model
            age = int(form.cleaned_data['Age_Group'])
            if age < 20:
                Age_Group = 0
            elif 20 < age < 35:
                Age_Group = 1
            elif 35 < age < 60:
                Age_Group = 2
            else:
                Age_Group = 3
            print("age is ", age, "group is", Age_Group)
            input_data = {
                'Age_Group': Age_Group,
                'Gender': int(form.cleaned_data['Gender']),
                'Pregnancy': int(form.cleaned_data['Pregnancy']),
                'Family_History_of_Thyroid': int(form.cleaned_data['Family_History_of_Thyroid']),
                'Goiter': int(form.cleaned_data['Goiter']),
                'Fatigue': int(form.cleaned_data['Fatigue']),
                'Hair_Loss': int(form.cleaned_data['Hair_Loss']),
                'Sensitivity_to_Cold_or_Heat': int(form.cleaned_data['Sensitivity_to_Cold_or_Heat']),
                'Increased_Sweating': int(form.cleaned_data['Increased_Sweating']),
                'Constipation_or_More_Bowel_Movements': int(form.cleaned_data['Constipation_or_More_Bowel_Movements']),
                'Depression_or_Anxiety': int(form.cleaned_data['Depression_or_Anxiety']),
                'Difficulty_Concentrating_or_Memory_Problems': int(form.cleaned_data['Difficulty_Concentrating_or_Memory_Problems']),
                'Dry_or_Itchy_Skin': int(form.cleaned_data['Dry_or_Itchy_Skin']),
            }

            # Handle symptoms with three values: 0 (No), 1 (Medium), 2 (High)
            weight_change = int(form.cleaned_data['Weight_Change'])  # Ensure conversion
            heart_rate_changes = int(form.cleaned_data['Heart_Rate_Changes'])  # Ensure conversion
            muscle_weakness = int(form.cleaned_data['Muscle_Weakness'])  # Ensure conversion

            # Include all symptoms but only use their values if > 0
            input_data['Weight_Change'] = weight_change if weight_change > 0 else 0
            input_data['Heart_Rate_Changes'] = heart_rate_changes if heart_rate_changes > 0 else 0
            input_data['Muscle_Weakness'] = muscle_weakness if muscle_weakness > 0 else 0

            # Convert to DataFrame for model prediction
            input_df = pd.DataFrame([input_data])

            # Predict using your prediction function
            prediction, contributions, description = predict_thyroid_risk(input_df)

            # Ensure contributions is a dictionary with standard Python types
            if isinstance(contributions, pd.Series):
                contributions = contributions.to_dict()  # Convert to dictionary if it is a Series

            # Store the results in the session for display
            request.session['prediction'] = prediction.item()  # Convert to standard Python int
            request.session['contributions'] = contributions  # This should now be serializable
            request.session['description'] = description

            # Store symptoms marked as 'Yes' in the session
            yes_symptoms = {k: v for k, v in form.cleaned_data.items() if v}
            request.session['yes_symptoms'] = yes_symptoms

            # Redirect to the output page
            return redirect('output')

    else:
        form = PredictionForm()

    return render(request, "index.html", {'form': form})




def output(request):
    # Get prediction data from session
    required_session_keys = ['prediction', 'contributions', 'description', 'yes_symptoms']
    if not all(key in request.session for key in required_session_keys):
        return redirect('index')

    prediction = request.session.get('prediction', 'No prediction made')
    contributions = request.session.get('contributions', {})
    description = request.session.get('description', 'No description available')

    # Gather symptoms marked as Yes from the session
    yes_symptoms = request.session.get('yes_symptoms', {})

    # Debug: Print collected data to check what's being retrieved
    print("Yes Symptoms: ", yes_symptoms)
    print("Contributions: ", contributions)

    # Filter contributions based on symptoms marked as Yes
    filtered_contributions = {symptom: contributions[symptom] for symptom in yes_symptoms.keys() if yes_symptoms[symptom]}

    # Calculate total contributions of the filtered symptoms
    total_contributions = sum(filtered_contributions.values())

    symptom_data = []
    if total_contributions > 0:  # Avoid division by zero
        variability_factor = 0.1  # Adjust as necessary for your needs (e.g., 10%)

        for symptom in filtered_contributions.keys():
            # Calculate the base percentage contribution
            percentage = (filtered_contributions[symptom] / total_contributions) * 100

            # Introduce variability to make the percentage more distinct
            variability = np.random.uniform(-variability_factor * percentage, variability_factor * percentage)
            adjusted_percentage = percentage + variability

            # Ensure the adjusted percentage does not drop below zero
            adjusted_percentage = max(adjusted_percentage, 0)

            symptom_data.append((symptom, round(adjusted_percentage, 2)))  # Store symptom and its percentage
    else:
        print("No valid contributions for symptoms.")

    # Get the risk level description
    risk_description = risk_level_description(prediction)
    if prediction == 0:
        prediction='Low'
    elif prediction == 1:
        prediction='Medium'
    else:
        prediction='High'

    request.session.pop('prediction', None)
    request.session.pop('contributions', None)
    request.session.pop('description', None)
    request.session.pop('yes_symptoms', None)

    return render(request, "output.html", {
        'prediction': prediction,
        'description': description,
        'risk_description': risk_description,
        'symptom_data': symptom_data,  # Pass the prepared list to the template
    })
