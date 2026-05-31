import gdown
import os

os.makedirs("models", exist_ok=True)

files = {
    "crop_model.pkl": "1uRlDwXQzC5Mb4r4ozlJnvWqfoQF4YOVL",
    "crop_recommendation_scaler.pkl": "1-Wkj5ee949-UALUO7P3lVdksz9g3_xS-",
    "fertilizer_model.pkl": "10TZHNYfcPLGLNR7UMd0SXE_5nsb4lt4h",
    "disease_model.pkl": "1HfH57BtrvpBcdaVAeFwCnbb6U9FdE0H7"
}

for filename, file_id in files.items():
    output = f"models/{filename}"

    if not os.path.exists(output):
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, output, quiet=False)

print("All models downloaded successfully!")