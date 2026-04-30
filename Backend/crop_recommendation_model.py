import pandas as pd
import numpy as np
import joblib
import os 
import matplotlib.pyplot as plt
import seaborn as sns 
from sklearn.model_selection import train_test_split, learning_curve
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay


# Define the 7 input features
CROP_FEATURES = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']


# I. DATA LOADING FUNCTIONS

def generate_synthetic_data():
    print()
    data_size = 5000
    npk = np.random.uniform(20, 100, size=(data_size, 3))
    temp = np.random.uniform(15, 40, data_size)
    humid = np.random.uniform(50, 90, data_size)
    ph = np.random.uniform(5.5, 7.5, data_size)
    rain = np.random.uniform(50, 250, data_size)
    
    data = np.hstack([npk, temp.reshape(-1, 1), humid.reshape(-1, 1), ph.reshape(-1, 1), rain.reshape(-1, 1)])
    df = pd.DataFrame(data, columns=CROP_FEATURES)
    
    # Simple rule-based logic to create a 'crop' column for the 4 synthetic classes
    def determine_crop(row):
        if row['N'] > 80 and row['K'] > 50 and row['ph'] > 6.5: return 'Rice'
        if row['temperature'] > 30 and row['humidity'] > 70: return 'Cotton'
        if row['P'] > 60 and row['rainfall'] < 100: return 'Maize'
        return 'Wheat'
    
    df['crop'] = df.apply(determine_crop, axis=1)
    return df

def load_or_generate_data(file_path=None):
    
    if file_path and os.path.exists(file_path):
        print(f"--- Loading Actual Dataset from: {file_path} ---")
        try:
            df = pd.read_csv(file_path)
            
            required_cols = CROP_FEATURES + ['label']
            if not all(col in df.columns for col in required_cols):
                 print(f"ERROR: Dataset must contain columns: {required_cols}. Falling back to synthetic data.")
                 return generate_synthetic_data()

            df = df.rename(columns={'label': 'crop'})
            
            unique_crops = df['crop'].unique()
            print("-" * 35)
            print(f"Total Unique Crop Classes Found: {len(unique_crops)} (Expected 22)")
            print("-" * 35)
            
            return df
            
        except Exception as e:
            print(f"ERROR reading file {file_path}: {e}. Falling back to synthetic data.")
            return generate_synthetic_data()
    else:
        print("--- WARNING: Dataset file not found. Generating Synthetic Data (4 crops only) ---")
        return generate_synthetic_data()


# II. TRAINING AND EVALUATION FUNCTION
 
def train_and_save_model(df):
    """Splits data (70/10/20), trains Random Forest, saves assets, and returns results."""
    
    X = df[CROP_FEATURES] # Full feature set
    y = df['crop'] 
    
    print("\n--- Splitting Data: 70% Train / 10% Validation / 20% Test ---")
    
    X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    validation_ratio = 0.125
    X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=validation_ratio, random_state=42, stratify=y_temp)
    
    print(f"Training Samples (70%): {len(X_train)} | Validation Samples (10%): {len(X_val)} | Testing Samples (20%): {len(X_test)}")
    print("\n--- Training Pipeline Started ---")
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    joblib.dump(scaler, 'crop_recommendation_scaler.pkl')
    
    model = RandomForestClassifier(n_estimators=100, random_state=42, criterion='entropy')
    model.fit(X_train_scaled, y_train)
    joblib.dump(model, 'crop_recommendation_rf_model.pkl')
    
    y_val_pred = model.predict(scaler.transform(X_val))
    val_accuracy = accuracy_score(y_val, y_val_pred)
    print(f"\nModel Accuracy on Validation Set: {val_accuracy:.4f}")

    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy on Test Set (Final Score): {accuracy:.4f}")
    print("\nClassification Report on Test Set:\n", classification_report(y_test, y_pred))
    # Return X (full feature set) for use in the learning curve plot
    return model, scaler, y_test, y_pred, X


# III. PLOTTING FUNCTIONS

def plot_correlation_matrix(df):
    print("\n" + "="*50)
    print("Generating Feature Correlation Matrix")
    print("="*50)
    
    df_features = df[CROP_FEATURES]
    correlation_matrix = df_features.corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        correlation_matrix, 
        annot=True, 
        cmap='coolwarm', 
        fmt=".2f", 
        linewidths=.5, 
        cbar_kws={'label': 'Correlation Coefficient'}
    )
    plt.title('Correlation Matrix of Crop Recommendation Features')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig('actual_feature_correlation_matrix.png')
    print("Correlation Matrix saved as 'actual_feature_correlation_matrix.png'")

def plot_confusion_matrix(y_true, y_pred):
    labels = sorted(list(y_true.unique()))
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)

    fig, ax = plt.subplots(figsize=(12, 10))
    disp.plot(cmap=plt.cm.Blues, ax=ax, xticks_rotation=45)
    plt.title('Confusion Matrix for Crop Recommendation (Final)')
    plt.tight_layout()
    plt.savefig('confusion_matrix_final.png')
    print("Confusion Matrix saved as 'confusion_matrix_final.png'")
    
def plot_classification_metrics(y_true, y_pred):
    """Generates and saves the Classification Metrics Bar Chart."""
    report_dict = classification_report(y_true, y_pred, output_dict=True)
    df_report = pd.DataFrame(report_dict).transpose()
    metrics_to_plot = ['precision', 'recall', 'f1-score']
    class_metrics = df_report.iloc[:-3][metrics_to_plot]

    fig, ax = plt.subplots(figsize=(14, 8))
    class_metrics.plot(kind='bar', ax=ax)
    plt.title('Classification Metrics Per Crop Class (Final)')
    plt.ylabel('Score')
    plt.xlabel('Crop Class')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Metric')
    plt.grid(axis='y', linestyle='--')
    plt.tight_layout()
    plt.savefig('accuracy_metrics_barchart_final.png')
    print("Accuracy metrics bar chart saved as 'accuracy_metrics_barchart_final.png'")

def plot_learning_curve(model, X, y, scaler, title="Learning Curve (Accuracy)"):
    
    X_scaled = scaler.transform(X) # Use the trained scaler
    
    train_sizes, train_scores, test_scores = learning_curve(
        model, 
        X_scaled, 
        y, 
        cv=5, 
        n_jobs=-1,
        train_sizes=np.linspace(.1, 1.0, 5),
        scoring='accuracy'
    )

    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)

    plt.figure(figsize=(10, 6))
    plt.title(title)
    plt.xlabel("Training Examples")
    plt.ylabel("Accuracy Score")
    plt.grid()

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1, color="r")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r", label="Training Score")

    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g", label="Cross-Validation Score")

    plt.legend(loc="best")
    plt.tight_layout()
    plt.savefig('learning_curve_accuracy.png')
    print("Learning Curve (Accuracy) saved as 'learning_curve_accuracy.png'")


# IV. DEPLOYMENT PREDICTION FUNCTION (Used by Uvicorn app.py)

def predict_crop(N, P, K, temp, humidity, ph, rainfall):
    try:
        loaded_model = joblib.load('crop_recommendation_rf_model.pkl')
        loaded_scaler = joblib.load('crop_recommendation_scaler.pkl')
        new_data = pd.DataFrame([[N, P, K, temp, humidity, ph, rainfall]], columns=CROP_FEATURES)
        data_scaled = loaded_scaler.transform(new_data)
        prediction = loaded_model.predict(data_scaled)[0]
        probabilities = loaded_model.predict_proba(data_scaled)[0]
        confidence = np.max(probabilities)

        return prediction, confidence

    except FileNotFoundError:
        print("ERROR: Model or Scaler file not found. Run the training function first.")
        return "ERROR", 0.0
    except Exception as e:
        # Added general error handling for robustness
        print(f"An unexpected error occurred during prediction: {e}") 
        return "ERROR", 0.0


# V. EXECUTION BLOCK (ONLY runs when script is executed directly)

if __name__ == '__main__':
    
    # Use raw string for cleaner Windows path handling
    DATASET_PATH = r"C:\Users\Lenovo\OneDrive\Documents\Dataset\Crop_recommendation.csv"

    dataset = load_or_generate_data(file_path=DATASET_PATH)
    
    if dataset is not None and 'crop' in dataset.columns:

        # 1. Plot Feature Analysis (Correlation)
        plot_correlation_matrix(dataset)

        # 2. Train Model and Get Test Results
        # NOTE: X_full is the full feature set DataFrame used for the learning curve.
        model, scaler, y_test, y_pred, X_full = train_and_save_model(dataset)

        print("\n" + "="*50)
        print("ML Model Training Complete. Assets Saved.")
        print("="*50)
        
        # 3. Plot Evaluation Metrics
        plot_confusion_matrix(y_test, y_pred)
        plot_classification_metrics(y_test, y_pred)
        
        # 4. Plot Learning Curve (Accuracy Curve)
        y_full = dataset['crop']
        print("\n" + "="*50)
        print("Generating Learning Curve (Accuracy)")
        print("="*50)
        plot_learning_curve(model, X_full, y_full, scaler)

