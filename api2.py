from flask import Flask, request, jsonify
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

app = Flask(__name__)

# Sample dataset provided by the user
data = {
    'cellosaurus_id': ['ESO-26'] * 9,
    'drug_name': ['(5Z)-7-Oxozeaenol', '123138', '123829', '150412', '5-azacytidine', 
                  '5-Fluorouracil', '50869', '615590', '630600'],
    'dataset': ['All'] * 9,
    'original_datasets': ['GDSC1', 'GDSC2', 'GDSC2', 'GDSC2', 'GDSC2', 'GDSC1,GDSC2', 
                          'GDSC2', 'GDSC2', 'GDSC2'],
    'IC50': [2.96115, 1.25172, 2.57774, 2.37471, 4.54382, 5.79944, 4.16631, 3.1986, 2.61565],
    'IC90': [5.3433, 3.87167, 5.01176, 4.72883, 6.59322, 11.0065, 6.43598, 5.49324, 5.22055],
    'EC50': [1.99681, -1.01881, 0.6114, 0.612498, 3.36549, 2.63421, 0.827372, 0.755261, 0.53761],
    'Einf': [0.582433, 0.259272, 0.289834, 0.323636, 0.440804, 0.416456, 0.0759312, 0.17579, 0.295382],
    'AUC': [11.8233, 3.59021, 3.80417, 4.2037, 5.44037, 11.816, 0.818531, 2.02594, 4.16402],
    'Cancer Type': ['Aerodigestive Tract Cancer'] * 9
}

df = pd.DataFrame(data)

@app.route('/predict_cancer', methods=['POST'])
def predict_cancer():
    # Get user input for the cancer type to predict
    req_data = request.get_json()
    cancer_type_to_predict = req_data['cancer_type']

    # Since 'Cancer Type' is the only categorical variable, we perform dummy encoding
    df_encoded = pd.get_dummies(df, columns=['Cancer Type'])

    # Check if the target variable exists in the encoded dataframe
    target_variable = f'Cancer Type_{cancer_type_to_predict}'
    if target_variable not in df_encoded.columns:
        return jsonify({'error': f"The cancer type '{cancer_type_to_predict}' is not found in the dataset."}), 400

    # Split the dataset into features and target variable
    X = df_encoded.drop(['drug_name', 'cellosaurus_id', 'dataset', 'original_datasets', target_variable], axis=1)
    y = df_encoded[target_variable]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the Random Forest classifier on the training data
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    # Predict on the test set
    y_pred = clf.predict(X_test)

    # Evaluate the model accuracy on the data
    accuracy = accuracy_score(y_test, y_pred)
    return jsonify({'accuracy': accuracy})

if __name__ == '__main__':
    app.run(debug=True, port=5002)
