import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import EfficientNetB3
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras import layers, models, callbacks

# 1. SETUP PATHS & CONFIG
DATA_DIR = r"C:\\Users\\Lenovo\\OneDrive\\Documents\\Dataset\\Plant_leave_diseases_dataset_with_augmentation"
IMG_SIZE = (224, 224)
BATCH_SIZE = 20 
SEED = 42

# 2. DATA AUGMENTATION 
datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    rotation_range=25,
    zoom_range=0.2,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.1,
    horizontal_flip=True,
    validation_split=0.2
)

train_gen = datagen.flow_from_directory(
    DATA_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training',
    seed=SEED
)

val_gen = datagen.flow_from_directory(
    DATA_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation',
    shuffle=False,
    seed=SEED
)

# 3. BUILD MODEL (EfficientNetB3)
base_model = EfficientNetB3(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False 

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.BatchNormalization(),
    layers.Dense(512, activation='relu'),
    layers.Dropout(0.4),
    layers.Dense(train_gen.num_classes, activation='softmax')
])

# 4. TRAINING CALLBACKS
early_stop = callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
checkpoint = callbacks.ModelCheckpoint("plant_disease_model.keras", monitor="val_accuracy", save_best_only=True)

# PHASE 1: Feature Extraction
model.compile(optimizer=tf.keras.optimizers.Adam(1e-3), 
              loss='categorical_crossentropy', metrics=['accuracy'])

print("Starting Phase 1 Training...")
model.fit(train_gen, validation_data=val_gen, epochs=5, callbacks=[early_stop, checkpoint])

# PHASE 2: Fine-Tuning 
base_model.trainable = True
for layer in base_model.layers:
    if isinstance(layer, layers.BatchNormalization):
        layer.trainable = False 

model.compile(optimizer=tf.keras.optimizers.Adam(1e-5), 
              loss='categorical_crossentropy', metrics=['accuracy'])

print("Starting Phase 2 Fine-Tuning...")
model.fit(train_gen, validation_data=val_gen, epochs=10, callbacks=[early_stop, checkpoint])

print("Model saved successfully as plant_disease_model.keras")