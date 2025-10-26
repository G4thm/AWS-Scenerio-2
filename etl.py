import pandas as pd
import boto3
import io

print("ETL job started...")

# Example: Read CSV from local or S3
data = pd.DataFrame({
    'product': ['Apple', 'Banana', 'Orange'],
    'price': [50, 30, 40]
})

# Transform (e.g., adjust price)
data['adjusted_price'] = data['price'] * 1.1
data.to_csv('transformed_data.csv', index=False)
print("ETL complete, saved as transformed_data.csv")

