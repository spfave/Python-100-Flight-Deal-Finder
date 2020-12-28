import os
import requests
from dotenv import load_dotenv
from flight_search import FlightSearch
load_dotenv()


# Constants
URL_FLIGHT_DATA = "https://api.sheety.co/e9eba1a41cbfb57732df73805f81e577/flightDeals/prices"


# Variables
auth_flight_data = (os.getenv("SHEETY_AUTH_USERNAME"), os.getenv("SHEETY_AUTH_PASSWORD"))


# Classes
class DataManager:
    """ This class is responsible for talking to the Google Sheet. """
    def __init__(self):
        self.destinations = self.get_destination_data()
        self.flight_search = FlightSearch()

    def get_destination_data(self):
        response = requests.get(url=URL_FLIGHT_DATA, auth=auth_flight_data)
        response.raise_for_status()

        return response.json()["prices"]

    def check_destination_codes(self):
        for destination in self.destinations:
            if destination["iataCode"] == "":
                city_code = self.flight_search.query_city_code(destination["city"])
                destination["iataCode"] = city_code

                self.update_destination_code(destination)

    def update_destination_code(self, destination):
        destination_row = f"{URL_FLIGHT_DATA}/{destination['id']}"
        destination_data = {
            "price":{
                "iataCode": destination["iataCode"],
            },
        }
        response = requests.put(url=destination_row, json=destination_data, auth=auth_flight_data)
        response.raise_for_status()

    def update_destination_price(self):
        pass


# Main
if __name__ == "__main__":
    # pass
    dm = DataManager()
    data = dm.get_destination_data()

    print(data)