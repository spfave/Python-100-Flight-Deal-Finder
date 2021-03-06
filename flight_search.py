import os
import requests
from dotenv import load_dotenv
from flight_data import FlightData, FlightQuery
from pprint import pprint
load_dotenv()


# Constants
URL_KIWI = "https://tequila-api.kiwi.com/v2"
DEPARTURE_CITY = "WAS"


# Variables
kiwi_key = os.getenv("KIWI_KEY")
kiwi_loc = f"{URL_KIWI}/locations/query"
kiwi_search = f"{URL_KIWI}/search"


# Classes
class FlightSearch:
    """ This class is responsible for talking to the Flight Search API. """

    def __init__(self):
        self.headers = {"apikey": kiwi_key, }

    def query_city_code(self, search_city):
        search_params = {
            "term": search_city,
            "location_types": "airport",
        }
        response = requests.get(
            url=kiwi_loc, params=search_params, headers=self.headers)
        response.raise_for_status()

        location_data = response.json()["locations"]
        city_code = location_data[0]["city"]["code"]
        return city_code

    def query_flight(self, flight_search_params):
        response = requests.get(
            url=kiwi_search, params=flight_search_params, headers=self.headers)
        response.raise_for_status()

        try:
            flight = response.json()["data"][0]
        except IndexError:
            print(
                f"No flights found to {flight_search_params['fly_to']}")
            return None
        else:
            print(
                f"{flight_search_params['fly_to']} {flight['price']}")
            return flight


# Main
if __name__ == "__main__":
    fs = FlightSearch()
    fq = FlightQuery(DEPARTURE_CITY, "IST",
                     nights_min=7, nights_max=28,
                     currency="USD", max_stopovers=1)
    data = fs.query_flight(fq.flight_params)
    pprint(data)
    fd = FlightData(data)
    pprint(fd.__dict__)
