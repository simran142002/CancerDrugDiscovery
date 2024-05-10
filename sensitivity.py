from flask import Flask, request, jsonify
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

app = Flask(__name__)

# Load the dataset
data = {
    'IC50': [2.96115, 1.25172, 2.57774, 2.37471, 4.54382, 5.79944, 4.16631, 3.1986, 2.61565],
    'IC90': [5.3433, 3.87167, 5.01176, 4.72883, 6.59322, 11.0065, 6.43598, 5.49324, 5.22055],
    'EC50': [1.99681, -1.01881, 0.6114, 0.612498, 3.36549, 2.63421, 0.827372, 0.755261, 0.53761],
    'Einf': [0.582433, 0.259272, 0.289834, 0.323636, 0.440804, 0.416456, 0.0759312, 0.17579, 0.295382],
    'AUC': [11.8233, 3.59021, 3.80417, 4.2037, 5.44037, 11.816, 0.818531, 2.02594, 4.16402]
}

df = pd.DataFrame(data)

@app.route('/predict', methods=['POST'])
def predict_sensitivity():
    # Get the target variable for prediction from the request
    target = request.json['target']
    
    # Validate the target variable
    if target not in df.columns:
        return jsonify({'error': f"The target variable '{target}' is not found in the dataset."}), 400

    # Features
    X = df.drop(target, axis=1)
    y = df[target]

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predict on the test set
    y_pred = model.predict(X_test)

    # Evaluate model performance
    mse = mean_squared_error(y_test, y_pred)

    # Prepare the response
    response = {
        'target': target,
        'mse': mse,
        'predictions': y_pred.tolist()
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
