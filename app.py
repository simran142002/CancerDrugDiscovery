from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

app = Flask(__name__)
CORS(app)

# Load the dataset
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

@app.route('/cluster', methods=['POST'])
def cluster_data():
    req_data = request.get_json()
    features = req_data.get('features', ['IC50', 'IC90', 'EC50', 'Einf', 'AUC'])
    
    # Select numerical features for clustering
    X = df[features]

    # Standardize the data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Perform PCA to reduce dimensionality
    pca = PCA(n_components=min(X.shape[0], X.shape[1]))
    X_pca = pca.fit_transform(X_scaled)

    # Perform KMeans clustering
    kmeans = KMeans(n_clusters=req_data.get('n_clusters', 3), random_state=42)
    df['cluster'] = kmeans.fit_predict(X_scaled)

    return jsonify(df['cluster'].tolist())

if __name__ == '__main__':
    app.run(debug=True)
