import os
import io
import pickle
import numpy as np
from celery import Celery
from PIL import Image

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
from tensorflow.keras.models import load_model

# --- Celery Configuration ---
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

celery_app = Celery('disease_worker', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
)

# --- ML Assets ---
MODEL_PATH = 'disease_detection_model.h5'
CLASS_NAMES_PATH = 'disease_class_names.pkl'
IMG_SIZE = (224, 224)

global_model = None
global_class_names = None


def load_ml_assets():
    """Loads the Keras model and class names dictionary."""
    global global_model, global_class_names

    if global_model is None:
        try:
            print("Worker: Loading model...")
            global_model = load_model(MODEL_PATH)
            print("Worker: Model loaded.")
        except Exception as e:
            print(f"Error loading model: {e}")
            global_model = None

    if global_class_names is None:
        try:
            print("Worker: Loading classes...")
            with open(CLASS_NAMES_PATH, 'rb') as f:
                global_class_names = pickle.load(f)
            print("Worker: Classes loaded.")
        except Exception as e:
            print(f"Error loading classes: {e}")
            global_class_names = None

    return global_model, global_class_names


def preprocess_image(image_bytes: bytes):
    """Preprocess image exactly like training."""
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img = img.resize(IMG_SIZE, Image.BILINEAR)

        img_array = np.array(img).astype("float32") / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        return img_array
    except Exception as e:
        print(f"Preprocessing failed: {e}")
        return None


@celery_app.task(bind=True, name='tasks.process_disease_image', max_retries=3, default_retry_delay=10)
def process_disease_image(self, image_bytes: bytes):
    print(f"Worker: Task {self.request.id} started.")

    model, class_names = load_ml_assets()
    if model is None or class_names is None:
        raise self.retry(exc=RuntimeError("Model not loaded"), countdown=10)

    try:
        # Preprocess
        input_tensor = preprocess_image(image_bytes)
        if input_tensor is None:
            raise ValueError("Image preprocessing failed")

        # Predict → model already outputs softmax
        preds = model.predict(input_tensor)
        idx = int(np.argmax(preds))
        confidence = float(np.max(preds))

        predicted_class = class_names.get(idx, "Unknown")

        print(f"Worker: Prediction -> {predicted_class} ({confidence:.2f})")

        return {
            "prediction": predicted_class,
            "confidence": round(confidence * 100, 2),
            "model_version": "EfficientNetB3-v1.0"
        }

    except Exception as e:
        msg = f"Prediction failed: {e}"
        print(msg)
        raise RuntimeError(msg)


if __name__ == "__main__":
    print("Worker starting…")
    load_ml_assets()
    print("Worker ready.")
