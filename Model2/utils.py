import numpy as np
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()


GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

# Define normal ranges for thyroid hormone comparison
NORMAL_RANGES = {
    "TSH": {"low": 0.4, "high": 4.0},
    "T3": {"low": 2.0, "high": 4.4},
    "TT4": {"low": 5.0, "high": 12.0},
    "T4U": {"low": 0.7, "high": 1.48},
    "FTI": {"low": 1.0, "high": 4.0},
    "TBG": {"low": 20, "high": 40},
    "T4": {"low": 4.5, "high": 11.5},
}

# Define fallback recommendations for hypothyroidism and hyperthyroidism
RECOMMENDATIONS = {
    "Hypothyroidism": {
        "Diet": [
            "Increase intake of iodine-rich foods such as fish, dairy products, and eggs.",
            "Consume selenium-rich foods like Brazil nuts, sunflower seeds, and legumes.",
            "Include zinc sources like meat, shellfish, and nuts.",
            "Eat plenty of fresh fruits and vegetables to provide necessary vitamins and minerals.",
            "Limit soy products as they can interfere with thyroid hormone absorption.",
        ],
        "Exercises": [
            "Engage in regular cardiovascular exercises such as walking, jogging, or cycling to boost metabolism.",
            "Incorporate strength training to build muscle mass.",
            "Practice yoga or stretching exercises to improve flexibility and reduce fatigue.",
            "Ensure a balanced exercise routine to prevent excessive strain.",
        ],
    },
    "Hyperthyroidism": {
        "Diet": [
            "Consume a balanced diet with adequate carbohydrates to prevent weight loss.",
            "Include calcium and vitamin D-rich foods to counteract bone loss.",
            "Limit intake of caffeine and stimulants to reduce anxiety and palpitations.",
            "Eat small, frequent meals to maintain energy levels.",
            "Ensure sufficient protein intake to support muscle maintenance.",
        ],
        "Exercises": [
            "Focus on low-impact exercises like swimming or walking to avoid excessive fatigue.",
            "Incorporate strength training to maintain muscle mass.",
            "Practice relaxation techniques such as tai chi or gentle yoga to manage stress.",
            "Ensure adequate rest between exercise sessions to prevent overexertion.",
        ],
    },
}

def preprocess_input(user_input):
    """Prepares the input features for the model prediction."""
    sex = 1 if user_input["sex"] == "F" else 0
    features = [
        user_input["age"],
        sex,
        user_input["goiter"],
        user_input.get("pregnancy", 0),
        user_input["TSH"],
        user_input["T3"],
        user_input["TT4"],
        user_input["T4U"],
        user_input["FTI"],
        user_input["TBG"],
        user_input["T4"],
    ]
    return np.array(features).reshape(1, -1)

def determine_condition(user_input):
    """Determines thyroid condition based on TSH levels."""
    if "TSH" in user_input:
        tsh = user_input["TSH"]
        if tsh < NORMAL_RANGES["TSH"]["low"]:
            return "Hyperthyroidism"
        elif tsh > NORMAL_RANGES["TSH"]["high"]:
            return "Hypothyroidism"
    return None  # No condition detected if within normal range

def compare_with_normal(user_input):
    """Compares user input lab values with normal ranges."""
    comparisons = {}
    for feature, ranges in NORMAL_RANGES.items():
        value = user_input.get(feature, None)
        if value is not None:
            if value < ranges["low"]:
                status = "Below normal range"
            elif value > ranges["high"]:
                status = "Above normal range"
            else:
                status = "Within normal range"
            comparisons[feature] = {
                "Your_Value": value,
                "Normal_Range": f"{ranges['low']} - {ranges['high']}",
                "Status": status,
            }
        else:
            comparisons[feature] = {
                "Your_Value": "Not provided",
                "Normal_Range": f"{ranges['low']} - {ranges['high']}",
                "Status": "Data missing",
            }
    return comparisons


def get_recommendations(user_input,condition):
    """Fetch diet and exercise recommendations from the Gemini API based on the condition."""

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(history=[])

    message = (
        f"Provide only thyroid pateint diet and exercise based give patient detail and give suitable recommendations for a patient with {condition}. based on the following details: {user_input}, give response in simple font without ** this symbol and without bold.  "
        "Please provide 8 statements clear and actionable points for each category without any disclaimers. "
        "Format your response as follows: 'Following Diet:' followed by the recommendations and 'Following Exercise:' followed by the exercise recommendations. "
    )
    print(message)
    response = chat_session.send_message(message)
    print("/n Response is /n",response)
    # Split response into lines and categorize recommendations
    diet_recommendations = []
    exercise_recommendations = []
    is_diet_section = False
    is_exercise_section = False

    response_lines = response.text.split("\n")
    for line in response_lines:
        line = line.strip()
        if line.startswith("Following Diet:"):
            is_diet_section = True
            is_exercise_section = False
            continue

        if line.startswith("Following Exercise:"):
            is_diet_section = False
            is_exercise_section = True
            continue

        if is_diet_section and line:
            diet_recommendations.append(line)

        if is_exercise_section and line:
            exercise_recommendations.append(line)

    return {
        "Diet": diet_recommendations[:8],
        "Exercises": exercise_recommendations[:8],
    }









# utils.py
import os
import re
import pdfplumber
import pandas as pd
import pickle
from django.conf import settings

def extract_data_from_pdf(file_path):
    name, age, gender, t3, t4, tsh = None, None, None, None, None, None

    with pdfplumber.open(file_path) as pdf:
        pdf_text = ""
        for page in pdf.pages:
            pdf_text += page.extract_text()

    # Extracting name, age, gender, T3, T4, and TSH values using regex
    name_match = re.search(r"Name\s*[:\-]?\s*(.*?)(?=\s*Age)", pdf_text)
    if name_match:
        name = name_match.group(1).strip()

    age_match = re.search(r"Age\s*[:\-]?\s*(\d+)", pdf_text)
    if age_match:
        age = int(age_match.group(1).strip())

    gender_match = re.search(r"Gender\s*[:\-]?\s*(\w+)", pdf_text)
    if gender_match:
        gender = gender_match.group(1).strip()

    t3_match = re.search(r"T3\s+(\d+(\.\d+)?)", pdf_text)
    if t3_match:
        t3 = float(t3_match.group(1).strip())

    t4_match = re.search(r"T4\s+(\d+(\.\d+)?)", pdf_text)
    if t4_match:
        t4 = float(t4_match.group(1).strip())

    tsh_match = re.search(r"TSH\s+(\d+(\.\d+)?)", pdf_text)
    if tsh_match:
        tsh = float(tsh_match.group(1).strip())

    return name, age, gender, t3, t4, tsh
