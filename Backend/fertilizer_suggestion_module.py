import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib

# 1. Load the Dataset
try:
    df = pd.read_csv("C:\\Users\\Lenovo\\OneDrive\\Documents\\Dataset\\Crop and fertilizer dataset.csv")
    print("Dataset loaded successfully.")
except FileNotFoundError:
    print("Error: 'Crop and fertilizer dataset.csv' not found. Ensure it is in the same folder as this script.")

# 2. Data Exploration (Head, Info, Describe)
print(df.head())
df.info()
print(df.describe())

# 3. Data Cleaning
print(f"Missing values:\n{df.isnull().sum()}")
print(f"Duplicated rows: {df.duplicated().sum()}")

# 4. Preprocessing
le_district = LabelEncoder()
le_soil = LabelEncoder()
le_crop = LabelEncoder()
le_fert = LabelEncoder()

df['District_Name'] = le_district.fit_transform(df['District_Name'])
df['Soil_color'] = le_soil.fit_transform(df['Soil_color'])
df['Crop'] = le_crop.fit_transform(df['Crop'])
df['Fertilizer'] = le_fert.fit_transform(df['Fertilizer'])

# 5. Model Training
X = df.drop(['Fertilizer', 'Link'], axis=1)
y = df['Fertilizer']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier()
model.fit(X_train, y_train)

# 6. Evaluation
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# 7. Prediction with User Input 
user_input = {
    'District_Name': 'Satara',
    'Soil_color': 'Red',
    'Nitrogen': 75,
    'Phosphorus': 55,
    'Potassium': 100,
    'pH': 7,
    'Rainfall': 1400,
    'Temperature': 20,
    'Crop': 'Sugarcane'
}

# Convert input using the same encoders used for training
user_df = pd.DataFrame([user_input])
user_df['District_Name'] = le_district.transform(user_df['District_Name'])
user_df['Soil_color'] = le_soil.transform(user_df['Soil_color'])
user_df['Crop'] = le_crop.transform(user_df['Crop'])

prediction_encoded = model.predict(user_df)
prediction_real = le_fert.inverse_transform(prediction_encoded)

print(f"Recommended Fertilizer: {prediction_real[0]}")



joblib.dump({
    "model": model,
    "encoder": le_fert,
    "district_encoder": le_district,
    "soil_encoder": le_soil,
    "crop_encoder": le_crop
}, "fertilizer_model.pkl")

print("Model and encoders saved successfully!")