from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)
model = joblib.load('smv_predictor_v1.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    price = data['adjusted_price']
    prediction = model.predict([[price]])[0]
    return jsonify({'predicted_discounted_price': prediction})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
