# forms.py
from django import forms

class PredictionForm(forms.Form):
    # Age Group as a select input
    Age_Group = forms.IntegerField(
        label='Enter Age :',
        min_value=1,
        error_messages={
            'required': 'This field is required.',
        }
    )

    Gender = forms.ChoiceField(choices=[
        (0, 'Female'),
        (1, 'Male')
    ])

    Pregnancy = forms.BooleanField(required=False, label="Pregnancy (Yes = 1, No = 0)")

    # Family History of Thyroid as a checkbox (Yes/No)
    Family_History_of_Thyroid = forms.BooleanField(required=False, label="Family History of Thyroid (Yes = 1, No = 0)")

    # Goiter as a checkbox (Yes/No)
    Goiter = forms.BooleanField(required=False, label="Goiter (Yes = 1, No = 0)")

    # Fatigue as a checkbox (Yes/No)
    Fatigue = forms.BooleanField(required=False, label="Fatigue (Yes = 1, No = 0)")

    # Hair Loss as a checkbox (Yes/No)
    Hair_Loss = forms.BooleanField(required=False, label="Hair Loss (Yes = 1, No = 0)")

    # Sensitivity to Cold or Heat as a checkbox (Yes/No)
    Sensitivity_to_Cold_or_Heat = forms.BooleanField(required=False,
                                                     label="Sensitivity to Cold or Heat (Yes = 1, No = 0)")

    # Increased Sweating as a checkbox (Yes/No)
    Increased_Sweating = forms.BooleanField(required=False, label="Increased Sweating (Yes = 1, No = 0)")

    # Constipation or More Bowel Movements as a checkbox (Yes/No)
    Constipation_or_More_Bowel_Movements = forms.BooleanField(required=False,
                                                              label="Constipation or More Bowel Movements (Yes = 1, No = 0)")

    # Depression or Anxiety as a checkbox (Yes/No)
    Depression_or_Anxiety = forms.BooleanField(required=False, label="Depression or Anxiety (Yes = 1, No = 0)")

    # Difficulty Concentrating or Memory Problems as a checkbox (Yes/No)
    Difficulty_Concentrating_or_Memory_Problems = forms.BooleanField(required=False,
                                                                     label="Difficulty Concentrating or Memory Problems (Yes = 1, No = 0)")

    # Dry or Itchy Skin as a checkbox (Yes/No)
    Dry_or_Itchy_Skin = forms.BooleanField(required=False, label="Dry or Itchy Skin (Yes = 1, No = 0)")

    # Weight Change as a select input with subcategories
    Weight_Change = forms.ChoiceField(choices=[
        (0, 'Normal'),
        (1, 'Medium'),
        (2, 'High')
    ])

    # Heart Rate Changes as a select input with subcategories
    Heart_Rate_Changes = forms.ChoiceField(choices=[
        (0, 'Normal'),
        (1, 'Medium'),
        (2, 'High')
    ])

    # Muscle Weakness as a select input with subcategories
    Muscle_Weakness = forms.ChoiceField(choices=[
        (0, 'Normal'),
        (1, 'Medium'),
        (2, 'High')
    ])
