import requests
import json
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

# Define the file path
file_path = 'data/stock_price.csv'

load_dotenv()
api_key = os.getenv('API_KEY')

#Requests
url_IBM = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey={api_key}'
url_APPL = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=APPL&interval=5min&apikey={api_key}'
url_TSLA = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=TSLA&interval=5min&apikey={api_key}'
url_UNH = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=UNH&interval=5min&apikey={api_key}'


r_IBM = requests.get(url_IBM)
r_APPL = requests.get(url_APPL)
r_TSLA = requests.get(url_TSLA)
r_UNH = requests.get(url_UNH)

data_IBM = r_IBM.json()
data_APPL = r_APPL.json()
data_TSLA = r_TSLA.json()
data_UNH = r_UNH.json()

# Define the columns
columns = ['Ticker', 'Date', 'Current Price']

# Create an empty DataFrame
df = pd.DataFrame(columns=columns)

df.loc[len(df)] = [data_IBM["Meta Data"]["2. Symbol"], data_IBM["Meta Data"]["3. Last Refreshed"], data_IBM["Time Series (5min)"][data_IBM["Meta Data"]["3. Last Refreshed"]]["1. open"]]
df.loc[len(df)] = [data_APPL["Meta Data"]["2. Symbol"], data_APPL["Meta Data"]["3. Last Refreshed"], data_APPL["Time Series (5min)"][data_APPL["Meta Data"]["3. Last Refreshed"]]["1. open"]]
df.loc[len(df)] = [data_TSLA["Meta Data"]["2. Symbol"], data_TSLA["Meta Data"]["3. Last Refreshed"], data_TSLA["Time Series (5min)"][data_TSLA["Meta Data"]["3. Last Refreshed"]]["1. open"]]
df.loc[len(df)] = [data_UNH["Meta Data"]["2. Symbol"], data_UNH["Meta Data"]["3. Last Refreshed"], data_UNH["Time Series (5min)"][data_UNH["Meta Data"]["3. Last Refreshed"]]["1. open"]]


# Check if the file exists
if os.path.exists(file_path):
    # If file exists, read the existing data
    existing_df = pd.read_csv(file_path)

    # Append the new data
    combined_df = pd.concat([existing_df, df], ignore_index=True)

    # Write the combined data back to the CSV file without the index column
    combined_df.to_csv(file_path, index=False)

    # Read the data back from the CSV file to ensure all data is written
    final_df = pd.read_csv(file_path)

    # Remove duplicate rows if any
    final_df.drop_duplicates(inplace=True)

    # Write the cleaned DataFrame back to the CSV file without the index column
    final_df.to_csv(file_path, index=False)

else:
    # If file does not exist, create new CSV with column names and add data to it
    df.to_csv(file_path, index=False)
    
# Display the final DataFrame to ensure data is appended correctly and duplicates are removed    
print("Final data written to file")