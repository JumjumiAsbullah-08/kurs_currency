import streamlit as st
import requests
from datetime import datetime
import time

# Dictionary untuk nama mata uang lengkap
currency_names = {
    "USD": "United States Dollar (USD)",
    "SGD": "Singapore Dollar (SGD)",
    "MYR": "Malaysia Ringgit (MYR)",
    "HKD": "Hong Kong Dollar (HKD)",
    "CNY": "Chinese Yuan (CNY)",
    "AUD": "Australian Dollar (AUD)",
    "EUR": "Euro (EUR)",
    "THB": "Thailand Baht (THB)",
    "TWD": "Taiwan Dollar (TWD)",
    "JPY": "Japanese Yen (JPY)",
    "GBP": "Great Britain Pound Sterling (GBP)",
    "SAR": "Saudi Riyal (SAR)",
    "KRW": "Korean Won (KRW)",
    "VND": "Vietnamese Dong (VND)",
    "IDR": "Indonesian Rupiah (IDR)"
}

# Title of the app
st.header("PT. Deli Megah Sejahtera | Exchange Rate")

# Function to fetch exchange rate data from a given API
def get_exchange_rate_from_api(base_currency, target_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if "rates" in data:
            return data["rates"].get(target_currency, None)
        else:
            st.error("The 'rates' key is missing in the API response.")
            return None
    else:
        st.error("Failed to retrieve data from ExchangeRate-API.")
        return None

# Function to get IDR rate from each currency
def get_idr_rate(currency):
    rate = get_exchange_rate_from_api(currency, "IDR")
    return rate

# Function to calculate Buy and Sell rates in IDR
def calculate_buy_sell_in_idr(rate):
    buy_rate = rate * 1.01  # 1% margin for buy rate
    sell_rate = rate * 0.99  # 1% margin for sell rate
    return round(buy_rate, 2), round(sell_rate, 2)

# Display the static data table
st.write("### Exchange Rates (Converted to IDR)")

table_data = []

for currency in currency_names.keys():
    if currency != "IDR":
        idr_rate = get_idr_rate(currency)
        if idr_rate:
            buy_rate, sell_rate = calculate_buy_sell_in_idr(idr_rate)
            table_data.append({
                "Nama Mata Uang": currency_names[currency],
                "Buy": f"Rp {buy_rate:,.2f}",
                "Sell": f"Rp {sell_rate:,.2f}"
            })

# Display the dataframe
st.table(table_data)

# Display dynamic time
time_container = st.empty()

while True:
    now = datetime.now()
    current_date_time = now.strftime("%A, %d %B %Y %H:%M:%S")
    time_container.write(f"**Date and Time:** {current_date_time}")

    # Wait for 1 second before updating
    time.sleep(1)
