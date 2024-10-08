import pandas as pd
import os

# Directory containing your CSV files
directory = '../datasets/stock_prices'

# List to hold DataFrames
df_list = []

# Iterate over each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        filepath = os.path.join(directory, filename)
        df = pd.read_csv(filepath)
        df_list.append(df)

# Concatenate all DataFrames
combined_df = pd.concat(df_list, ignore_index=True)

# Save the combined DataFrame to a new CSV file
combined_df.to_csv(f'{directory}/stock_prices_dataset.csv', index=False)
