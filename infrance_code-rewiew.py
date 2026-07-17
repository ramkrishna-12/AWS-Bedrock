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
# Code review comment -> Consider making MODEL_FILE configurable via environment variable or CLI argument for flexibility.

if not os.path.exists(MODEL_FILE):
    # Load dataset
    iris = load_iris()  
    # Code review comment -> Good use of sklearn's built-in dataset for demonstration; no external dependencies needed.

    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=0.2, random_state=42
    )
    # Code review comment -> Using a fixed random_state ensures reproducibility, which is good practice.

    # Train a Random Forest model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    # Code review comment -> 100 estimators is reasonable for small datasets; could be parameterized for flexibility.
    model.fit(X_train, y_train)

    # Save the trained model
    joblib.dump(model, MODEL_FILE)
    print("Model trained and saved.")
    # Code review comment -> Consider logging instead of print for production readiness.

# -----------------------------
# Step 2: Load the model for inference
# -----------------------------
model = joblib.load(MODEL_FILE)
# Code review comment -> No exception handling here; consider wrapping in try/except to handle file corruption or missing file.

# -----------------------------
# Step 3: Inference function
# -----------------------------
def predict_iris_class(features):
    """
    Predict the Iris flower class given a list of features:
    [sepal length, sepal width, petal length, petal width]
    """
    # Code review comment -> Good docstring; could also specify expected units or value ranges for clarity.
    if not isinstance(features, (list, np.ndarray)):
        raise TypeError("Features must be a list or numpy array.")
    features = np.array(features).reshape(1, -1)
    # Code review comment -> Reshaping ensures compatibility with sklearn; good defensive programming.
    predicted_index = model.predict(features)[0]
    return load_iris().target_names[predicted_index]
    # Code review comment -> Loading iris dataset inside function each time is inefficient; consider caching target names globally.

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
    # Code review comment -> Good use of assert for validation; in production, consider unittest or pytest for structured testing.

    # Test 2: Invalid input type
    try:
        predict_iris_class("invalid_input")
    except TypeError:
        print("Test 2 Passed: Invalid input type correctly raised TypeError.")
    else:
        raise AssertionError("Test 2 Failed: TypeError not raised for invalid input.")
    # Code review comment -> Properly tests error handling; could also test for empty lists or wrong feature length.

    # Test 3: Shape handling
    sample_list = [5.1, 3.5, 1.4, 0.2]
    predicted_class = predict_iris_class(sample_list)
    assert predicted_class in iris.target_names, "Test 3 Failed: Prediction not in valid class names."
    print("Test 3 Passed: List input handled correctly.")
    # Code review comment -> Covers basic valid input; could add boundary value tests for robustness.

# -----------------------------
# Step 5: Run inference and tests
# -----------------------------
if __name__ == "__main__":
    # Example inference
    sample_input = [5.1, 3.5, 1.4, 0.2]
    print(f"Predicted class for {sample_input}: {predict_iris_class(sample_input)}")
    # Code review comment -> Example inference is clear; could also show multiple predictions in batch mode.

    # Run integrated tests
    run_tests()
    # Code review comment -> Running tests automatically is good for demonstration; in production, separate test execution from main logic.

# code revirew comment -> Overall, the code is well-structured and demonstrates good practices in model training, saving, loading, and inference. Consider adding more comprehensive error handling, logging, and parameterization for production readiness.
# code review comment -> Additionally, consider adding comments on the expected input ranges and types for the inference function to improve usability and maintainability.
# code commite review comment -> Finally, consider implementing a more robust testing framework (like pytest) for better test management and reporting in larger projects.
# final code review comment -> Overall, the code is clear and functional, but could benefit from additional documentation, error handling, and configurability for production use.
#