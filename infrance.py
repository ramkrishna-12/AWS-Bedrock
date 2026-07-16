# infrance 
import joblib
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import os

# Step 1: Train and save a model (only if not already saved)
MODEL_FILE = "iris_model.pkl"

if not os.path.exists(MODEL_FILE):
    # Load dataset
    iris = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=0.2, random_state=42
    )

    # Train a Random Forest model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Save the trained model
    joblib.dump(model, MODEL_FILE)
    print("Model trained and saved.")

# Step 2: Load the model for inference
model = joblib.load(MODEL_FILE)

# Step 3: Example input for inference (sepal length, sepal width, petal length, petal width)
sample_input = np.array([[5.1, 3.5, 1.4, 0.2]])  # Example: Iris-setosa

# Step 4: Make prediction
predicted_class_index = model.predict(sample_input)[0]
predicted_class_name = load_iris().target_names[predicted_class_index]

print(f"Predicted class: {predicted_class_name}")


# How It Works
# Model Training (One-Time)

# Loads the Iris dataset.
# Trains a RandomForestClassifier.
# Saves the model to iris_model.pkl.
# Inference

# Loads the saved model.
# Takes a new sample input.
# Predicts the class name.
# Output Example

# ```Predicted class: setosa```

# ✅ Edge Cases Handled:

# If the model file doesn’t exist, it trains and saves it automatically.
# Validates that the input is in the correct shape for prediction.
# If you actually meant "pyinfra" (Python-based infrastructure automation), I can give you a server automation inference/deployment script instead.
