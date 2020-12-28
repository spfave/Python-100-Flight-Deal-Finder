import os
import requests
from dotenv import load_dotenv
from datetime import date, timedelta
from flight_data import FlightData
from pprint import pprint

from requests.models import Response
load_dotenv()


# Constants
URL_KIWI = "https://tequila-api.kiwi.com"
DEPARTURE_CITY = "WAS"


# Variables
kiwi_key = os.getenv("KIWI_KEY")
kiwi_loc = f"{URL_KIWI}/locations/query"
kiwi_search = f"{URL_KIWI}/search"


# Classes
class FlightSearch:
    """ This class is responsible for talking to the Flight Search API. """

    def __init__(self):
        self.headers = {"apikey": kiwi_key,}

    def query_city_code(self, search_city):
        search_params = {
            "term": search_city,
            "location_types": "airport",
        }
        response = requests.get(url=kiwi_loc, params=search_params, headers=self.headers)
        response.raise_for_status()

        location_data = response.json()["locations"]
        city_code = location_data[0]["city"]["code"]
        return city_code

    def query_flight(self, flight_search_params):
        response = requests.get(url=kiwi_search, params=flight_search_params, headers=self.headers)
        response.raise_for_status()

        return response.json()



# Main
if __name__ == "__main__":
    # pass
    fs = FlightSearch()
    fd = FlightData(DEPARTURE_CITY, "PAR", currency="USD", price_max=199)
    data = fs.query_flight(fd.flight_params)
    pprint(data)
