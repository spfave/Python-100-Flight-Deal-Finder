import os
import requests
from dotenv import load_dotenv
load_dotenv()


# Constants
URL_FLIGHT_DATA = "https://api.sheety.co/e9eba1a41cbfb57732df73805f81e577/flightDeals/prices"


# Variables
auth_flight_data = (os.getenv("SHEETY_AUTH_USERNAME"), os.getenv("SHEETY_AUTH_PASSWORD"))


# Classes
class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        pass

    def get_destination_data(self):
        response = requests.get(url=URL_FLIGHT_DATA, auth=auth_flight_data)
        response.raise_for_status()

        return response.json()

    def update_destination_price(self):
        pass


# Main
if __name__ == "__main__":
    # pass
    dm = DataManager()
    data = dm.get_destination_data()

    print(data)