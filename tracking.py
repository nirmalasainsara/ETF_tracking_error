import os
import sys
import requests
import base64
from datetime import timedelta, date, datetime

symbol_first = "SETFNIF50.XNSE"
symbol_second = "SETFNN50.XNSE"
base_url = "http://api.marketstack.com/v1/tickers"
params = {"access_key": os.environ.get("MARKETSTACK_KEY")}  # store in env
name = 'nirmalasainsara'
etf_name = 'NIFTY 50'

def filter_weekend_dates(date_):
    # since market is closed on weekends
    if date_.weekday() == 5:
        return date_ - timedelta(1)
    elif date_.weekday() == 6:
        return date_ - timedelta(2)
    return date_


def get_closing_value(symbol, date_):
    try:
        response = requests.get(f"{base_url}/{symbol}/eod/{date_}", params=params)
    except Exception:
        print("Invalid call to marketstack backend")
        sys.exit()
    closing_value = response.json()["close"]
    print(f"closing value for {symbol} on {date_}: {closing_value}")
    return closing_value


def get_tracking_error(eod1, eod2, eoy1, eoy2):
    print("Getting tracking error...")
    result1 = eod1 / (eoy1 - 1) * 100
    result2 = eod2 / (eoy2 - 1) * 100
    result = result1 - result2
    encrypted_data = base64.b64encode(b'result')
    data = {"username": name, "etf_name": etf_name, "encrypted_data": encrypted_data}
    data1 = requests.post("https://d715-2405-201-c00b-8930-1f1-f3f1-f950-1cc0.ngrok.io/api/assignment", data=data)
    return data1



if __name__ == "__main__":
    date_ = input("enter any date of past in yyyy-mm-dd format > ")
    try:
        date_ = datetime.strptime(date_, "%Y-%m-%d")
        date_ = date_.date()
    except Exception:
        print("Enter date in Valid format")
        sys.exit()
    if date_ >= date.today():
        print("Enter date of past")
        sys.exit()

    date_ = filter_weekend_dates(date_)
    last_year_date = date_ - timedelta(90)
    last_year_date = filter_weekend_dates(last_year_date)
    eod1 = get_closing_value(symbol_first, date_)
    eoy1 = get_closing_value(symbol_first, last_year_date)
    eod2 = get_closing_value(symbol_second, date_)
    eoy2 = get_closing_value(symbol_second, last_year_date)
    result = get_tracking_error(eod1, eod2, eoy1, eoy2)
    print(f"Tracking error is {result}")