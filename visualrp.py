from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS from flask_cors
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the dataset
data = {
    'cellosaurus_id': ['ESO-26'] * 9,
    'drug_name': ['(5Z)-7-Oxozeaenol', '123138', '123829', '150412', '5-azacytidine', 
                  '5-Fluorouracil', '50869', '615590', '630600'],
    'IC50': [2.96115, 1.25172, 2.57774, 2.37471, 4.54382, 5.79944, 4.16631, 3.1986, 2.61565],
    'IC90': [5.3433, 3.87167, 5.01176, 4.72883, 6.59322, 11.0065, 6.43598, 5.49324, 5.22055],
    'Cancer Type': ['Aerodigestive Tract Cancer'] * 9
}

df = pd.DataFrame(data)

@app.route('/visualize', methods=['POST'])
def visualize_data():
    # Receive data from the request
    request_data = request.get_json()
    cancer_type_input = request_data.get('cancerType')
    attribute_input = request_data.get('attribute')

    # Filter the dataframe based on the user input
    df_filtered = df[df['Cancer Type'] == cancer_type_input]

    # Check if the attribute entered by the user is valid
    if attribute_input not in df.columns:
        return jsonify({'error': f"The attribute '{attribute_input}' is not found in the dataset."}), 400

    # Create a scatter plot for the selected attribute values
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df_filtered, x='Cancer Type', y=attribute_input, hue='drug_name', style='drug_name', s=100)
    plt.title(f'Drug Response Profiles - {attribute_input} Across Different Cancer Types')
    plt.xlabel('Cancer Type')
    plt.ylabel(attribute_input)
    plt.xticks(rotation=45, ha='right')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    # Save the plot to a bytes object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    # Encode the bytes object to base64
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')

    return jsonify({'image_base64': image_base64}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5004)