import joblib
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import os

# -----------------------------
# Step 1: Train and save a model (only if not already saved)
# -----------------------------
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

# -----------------------------
# Step 2: Load the model for inference
# -----------------------------
model = joblib.load(MODEL_FILE)

# -----------------------------
# Step 3: Inference function
# -----------------------------
def predict_iris_class(features):
    """
    Predict the Iris flower class given a list of features:
    [sepal length, sepal width, petal length, petal width]
    """
    if not isinstance(features, (list, np.ndarray)):
        raise TypeError("Features must be a list or numpy array.")
    features = np.array(features).reshape(1, -1)
    predicted_index = model.predict(features)[0]
    return load_iris().target_names[predicted_index]

# -----------------------------
# Step 4: Integrated Test Cases
# -----------------------------
def run_tests():
    iris = load_iris()
    X, y = iris.data, iris.target

    # Test 1: Known sample from dataset
    sample = X[0]
    expected_class = iris.target_names[y[0]]
    predicted_class = predict_iris_class(sample)
    assert predicted_class == expected_class, f"Test 1 Failed: Expected {expected_class}, got {predicted_class}"
    print("Test 1 Passed: Known sample prediction correct.")

    # Test 2: Invalid input type
    try:
        predict_iris_class("invalid_input")
    except TypeError:
        print("Test 2 Passed: Invalid input type correctly raised TypeError.")
    else:
        raise AssertionError("Test 2 Failed: TypeError not raised for invalid input.")

    # Test 3: Shape handling
    sample_list = [5.1, 3.5, 1.4, 0.2]
    predicted_class = predict_iris_class(sample_list)
    assert predicted_class in iris.target_names, "Test 3 Failed: Prediction not in valid class names."
    print("Test 3 Passed: List input handled correctly.")

# -----------------------------
# Step 5: Run inference and tests
# -----------------------------
if __name__ == "__main__":
    # Example inference
    sample_input = [5.1, 3.5, 1.4, 0.2]
    print(f"Predicted class for {sample_input}: {predict_iris_class(sample_input)}")

    # Run integrated tests
    run_tests()
