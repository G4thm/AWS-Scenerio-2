import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

print("Training model...")

data = pd.read_csv('../data_proc_2/processed_data_2.csv')
X = data[['adjusted_price']]
y = data['discounted_price']

model = LinearRegression()
model.fit(X, y)
joblib.dump(model, 'smv_predictor_v1.pkl')

print("Model saved as smv_predictor_v1.pkl")

