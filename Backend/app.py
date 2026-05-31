from passlib.context import CryptContext

# Initialize Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

import os
import io
import json
import joblib
import numpy as np
import pandas as pd
import tensorflow as tf

from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from PIL import Image
from tensorflow.keras.applications.efficientnet import preprocess_input
from motor.motor_asyncio import AsyncIOMotorClient

# IMPORT GOOGLE DRIVE MODEL DOWNLOADER
import download_models


# =========================================================
# 1. BASE DIRECTORY & DATABASE SETUP
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# MODELS FOLDER
MODELS_DIR = os.path.join(BASE_DIR, "Models")

ML_ASSETS = {}

# MongoDB Atlas Configuration
MONGO_DETAILS = os.getenv("MONGO_URI")

client = AsyncIOMotorClient(MONGO_DETAILS)

database = client.plant_disease_db

user_collection = database.get_collection("users")


# =========================================================
# 2. LOAD MODELS ON STARTUP
# =========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    print(f"\n--- Starting Backend in: {BASE_DIR} ---")

    # -----------------------------
    # LOAD CROP & FERTILIZER MODELS
    # -----------------------------
    try:

        ML_ASSETS["crop"] = joblib.load(
            os.path.join(MODELS_DIR, "crop_recommendation_rf_model.pkl")
        )

        ML_ASSETS["scaler"] = joblib.load(
            os.path.join(MODELS_DIR, "crop_recommendation_scaler.pkl")
        )

        fert_data = joblib.load(
            os.path.join(MODELS_DIR, "fertilizer_model.pkl")
        )

        ML_ASSETS["fert_model"] = fert_data['model']
        ML_ASSETS["fert_enc"] = fert_data['encoder']
        ML_ASSETS["district_enc"] = fert_data['district_encoder']
        ML_ASSETS["soil_enc"] = fert_data['soil_encoder']
        ML_ASSETS["crop_enc"] = fert_data['crop_encoder']

        print("SUCCESS: Crop & Fertilizer Models Loaded")

    except Exception as e:
        print(f"CROP/FERTILIZER MODEL ERROR: {e}")

    # -----------------------------
    # LOAD DISEASE MODEL
    # -----------------------------
    try:

        model_path = os.path.join(
            MODELS_DIR,
            "plant_disease_model.keras"
        )

        json_path = os.path.join(
            MODELS_DIR,
            "class_indices.json"
        )

        if os.path.exists(model_path):

            base_model = tf.keras.applications.EfficientNetB3(
                weights=None,
                include_top=False,
                input_shape=(224, 224, 3)
            )

            rebuilt_model = tf.keras.models.Sequential([
                base_model,
                tf.keras.layers.GlobalAveragePooling2D(),
                tf.keras.layers.BatchNormalization(),
                tf.keras.layers.Dense(512, activation='relu'),
                tf.keras.layers.Dropout(0.4),
                tf.keras.layers.Dense(10, activation='softmax')
            ])

            rebuilt_model.load_weights(model_path)

            ML_ASSETS["disease"] = rebuilt_model

            print("SUCCESS: Disease Model Loaded")

            with open(json_path, 'r') as f:

                raw_indices = json.load(f)

                ML_ASSETS["labels"] = {
                    str(value): key
                    for key, value in raw_indices.items()
                }

            print("SUCCESS: Labels Loaded")

        else:
            print("ERROR: Disease model not found")

    except Exception as e:
        print(f"DISEASE MODEL ERROR: {e}")

    yield

    ML_ASSETS.clear()


# =========================================================
# 3. APP INITIALIZATION
# =========================================================

app = FastAPI(
    title="Smart Farming API",
    lifespan=lifespan
)

# =========================================================
# 4. CORS CONFIGURATION
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# 5. DATA SCHEMAS
# =========================================================

class UserSchema(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class CropInput(BaseModel):
    N: float
    P: float
    K: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float


class FertilizerInput(BaseModel):
    District_Name: str
    Soil_color: str
    Nitrogen: float
    Phosphorus: float
    Potassium: float
    pH: float
    Rainfall: float
    Temperature: float
    Crop: str


# =========================================================
# 6. AUTH ROUTES
# =========================================================

@app.post("/signup/")
async def signup(user: UserSchema):

    existing_user = await user_collection.find_one({
        "email": user.email
    })

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = pwd_context.hash(user.password)

    user_data = user.model_dump()

    user_data["password"] = hashed_password

    await user_collection.insert_one(user_data)

    return {
        "message": "Account Created Successfully!"
    }


@app.post("/login/")
async def login(user: LoginSchema):

    found_user = await user_collection.find_one({
        "email": user.email
    })

    if found_user and pwd_context.verify(
        user.password,
        found_user["password"]
    ):

        return {
            "token": "fake-jwt-token",
            "name": found_user["name"],
            "message": "Login Successful"
        }

    raise HTTPException(
        status_code=401,
        detail="Invalid email or password"
    )


# =========================================================
# 7. STATUS ROUTE
# =========================================================

@app.get("/status")
def get_status():

    return {
        "crop_ready": "crop" in ML_ASSETS,
        "fert_ready": "fert_model" in ML_ASSETS,
        "disease_ready": "disease" in ML_ASSETS
    }


# =========================================================
# 8. CROP RECOMMENDATION
# =========================================================

@app.post("/predict/crop")
async def predict_crop(data: CropInput):

    if "crop" not in ML_ASSETS:
        raise HTTPException(
            status_code=503,
            detail="Crop model not loaded"
        )

    try:

        input_data = pd.DataFrame([[
            data.N,
            data.P,
            data.K,
            data.temperature,
            data.humidity,
            data.ph,
            data.rainfall
        ]], columns=[
            'N',
            'P',
            'K',
            'temperature',
            'humidity',
            'ph',
            'rainfall'
        ])

        scaled_data = ML_ASSETS["scaler"].transform(input_data)

        prediction = ML_ASSETS["crop"].predict(
            scaled_data
        )[0]

        probabilities = ML_ASSETS["crop"].predict_proba(
            scaled_data
        )

        confidence = np.max(probabilities) * 100

        return {
            "prediction": str(prediction),
            "confidence": round(float(confidence), 2),
            "status": "success"
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Crop prediction error: {e}"
        )


# =========================================================
# 9. FERTILIZER RECOMMENDATION
# =========================================================

@app.post("/predict/fertilizer")
async def predict_fertilizer(data: FertilizerInput):

    if "fert_model" not in ML_ASSETS:
        raise HTTPException(
            status_code=503,
            detail="Fertilizer model not loaded"
        )

    try:

        district = ML_ASSETS["district_enc"].transform([
            data.District_Name.strip().title()
        ])[0]

        soil = ML_ASSETS["soil_enc"].transform([
            data.Soil_color.strip().title()
        ])[0]

        crop = ML_ASSETS["crop_enc"].transform([
            data.Crop.strip().title()
        ])[0]

        input_df = pd.DataFrame([[
            district,
            soil,
            data.Nitrogen,
            data.Phosphorus,
            data.Potassium,
            data.pH,
            data.Rainfall,
            data.Temperature,
            crop
        ]], columns=[
            'District_Name',
            'Soil_color',
            'Nitrogen',
            'Phosphorus',
            'Potassium',
            'pH',
            'Rainfall',
            'Temperature',
            'Crop'
        ])

        pred_encoded = ML_ASSETS["fert_model"].predict(
            input_df
        )

        probabilities = ML_ASSETS["fert_model"].predict_proba(
            input_df
        )

        confidence = np.max(probabilities) * 100

        fertilizer_name = ML_ASSETS["fert_enc"].inverse_transform(
            pred_encoded
        )[0]

        return {
            "prediction": str(fertilizer_name),
            "confidence": round(float(confidence), 2),
            "status": "success"
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Fertilizer prediction failed: {e}"
        )


# =========================================================
# 10. DISEASE PREDICTION
# =========================================================

@app.post("/predict/disease")
async def predict_disease(
    file: UploadFile = File(...)
):

    if "disease" not in ML_ASSETS:
        raise HTTPException(
            status_code=503,
            detail="Disease model not loaded"
        )

    try:

        contents = await file.read()

        img = Image.open(
            io.BytesIO(contents)
        ).convert('RGB').resize((224, 224))

        img_array = np.array(img).astype(np.float32)

        img_array = np.expand_dims(img_array, axis=0)

        img_preprocessed = preprocess_input(img_array)

        predictions = ML_ASSETS["disease"].predict(
            img_preprocessed
        )

        result_index = np.argmax(predictions[0])

        confidence = float(np.max(predictions[0]))

        disease_name = ML_ASSETS["labels"].get(
            str(result_index),
            "Unknown Disease"
        )

        return {
            "prediction": disease_name,
            "confidence": round(confidence * 100, 2),
            "status": "success"
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# 11. MAIN
# =========================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=5000,
        reload=True
    )