import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
import joblib

# 1. Load Dataset (use raw string to avoid path error)
df = pd.read_csv(r"C:\Users\Anjali Chimane\OneDrive\Desktop\fertilizer\Crop and fertilizer dataset.csv")
print("Dataset loaded successfully.\n")

# 2. Basic Info
print(df.head())
print("\nMissing values:\n", df.isnull().sum())

# 3. Label Encoding
le_district = LabelEncoder()
le_soil = LabelEncoder()
le_crop = LabelEncoder()
le_fert = LabelEncoder()

df['District_Name'] = le_district.fit_transform(df['District_Name'])
df['Soil_color'] = le_soil.fit_transform(df['Soil_color'])
df['Crop'] = le_crop.fit_transform(df['Crop'])
df['Fertilizer'] = le_fert.fit_transform(df['Fertilizer'])

# 4. Features & Target
X = df.drop(['Fertilizer', 'Link'], axis=1)
y = df['Fertilizer']

# 5. Train-Test Split (stratify important for imbalance)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 6. Apply SMOTE (fix: k_neighbors=2)
smote = SMOTE(k_neighbors=2, random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

print("\nBefore SMOTE:\n", y_train.value_counts())
print("\nAfter SMOTE:\n", pd.Series(y_train_res).value_counts())

# 7. Model Training
model = RandomForestClassifier(
    n_estimators=200,
    class_weight='balanced',
    random_state=42
)

model.fit(X_train_res, y_train_res)

# 8. Evaluation
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"\nModel Accuracy: {accuracy * 100:.2f}%")

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# 9. Prediction with User Input
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

user_df = pd.DataFrame([user_input])

# Safe transform
try:
    user_df['District_Name'] = le_district.transform(user_df['District_Name'])
    user_df['Soil_color'] = le_soil.transform(user_df['Soil_color'])
    user_df['Crop'] = le_crop.transform(user_df['Crop'])
except:
    print("Error: Unknown category in input!")
    exit()

prediction_encoded = model.predict(user_df)
prediction_real = le_fert.inverse_transform(prediction_encoded)

print(f"\nRecommended Fertilizer: {prediction_real[0]}")

# 10. Save Model
joblib.dump({
    "model": model,
    "fertilizer_encoder": le_fert,
    "district_encoder": le_district,
    "soil_encoder": le_soil,
    "crop_encoder": le_crop
}, "fertilizer_model.pkl")

print("\nModel and encoders saved successfully!")