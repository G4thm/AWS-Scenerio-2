import pandas as pd

print("Data Processor 2 running...")
df = pd.read_csv('../data_proc_1/processed_data_1.csv')
df['discounted_price'] = df['adjusted_price'] * 0.95
df.to_csv('processed_data_2.csv', index=False)
print("Data Processor 2 completed.")
