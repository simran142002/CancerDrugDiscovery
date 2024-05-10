from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import itertools

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the dataset
data = [
    {'cellosaurus_id': 'ESO-26', 'drug_name': '(5Z)-7-Oxozeaenol', 'IC50': 2.96115, 'IC90': 5.3433, 'Cancer Type': 'Aerodigestive Tract Cancer'},
    {'cellosaurus_id': 'ESO-26', 'drug_name': '123138', 'IC50': 1.25172, 'IC90': 3.87167, 'Cancer Type': 'Aerodigestive Tract Cancer'},
    # ... (other data entries) ...
    {'cellosaurus_id': 'ESO-26', 'drug_name': '630600', 'IC50': 2.61565, 'IC90': 5.22055, 'Cancer Type': 'Aerodigestive Tract Cancer'}
]

# Define function to calculate combined response
def calculate_combined_response(response_values, method='product'):
    if method == 'product':
        return np.product(response_values)
    elif method == 'sum':
        return np.sum(response_values)
    else:
        raise ValueError("Unsupported method. Supported methods are 'product' and 'sum'.")

@app.route('/calculate_combined_response', methods=['POST'])
def calculate_combined_response_api():
    # Receive input from the request
    request_data = request.json
    
    # Parse user input
    method = request_data.get('method')
    drugs = request_data.get('drugs')
    
    # Validate input
    if method not in ['product', 'sum']:
        return jsonify({'error': 'Unsupported method. Supported methods are "product" and "sum".'}), 400
    if not isinstance(drugs, list) or len(drugs) != 2:
        return jsonify({'error': 'Please provide a list of two drugs.'}), 400
    
    # Define drug combinations
    drug_combinations = list(itertools.combinations(set(d['drug_name'] for d in data), 2))
    
    # Initialize results dictionary
    results = {}
    
    # Analyze drug combinations
    for combination in drug_combinations:
        drug1 = combination[0]
        drug2 = combination[1]
        
        # Check if the current combination matches the input drugs
        if all(drug in drugs for drug in [drug1, drug2]):
            # Filter data for the two drugs in the combination
            drug1_data = [d for d in data if d['drug_name'] == drug1]
            drug2_data = [d for d in data if d['drug_name'] == drug2]
            
            # Calculate combined response for each cancer type
            combined_responses = []
            for cancer_type in set(d['Cancer Type'] for d in data):
                drug1_response = next((d['IC50'] for d in drug1_data if d['Cancer Type'] == cancer_type), None)
                drug2_response = next((d['IC50'] for d in drug2_data if d['Cancer Type'] == cancer_type), None)
                if drug1_response is not None and drug2_response is not None:
                    combined_response = calculate_combined_response([drug1_response, drug2_response], method)
                    combined_responses.append(combined_response)
            
            # Store results for the drug combination
            results[f"{drug1} + {drug2}"] = combined_responses
    
    # Return results
    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True, port=5003)
