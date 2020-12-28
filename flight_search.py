import os
import requests
from dotenv import load_dotenv
from pprint import pprint
load_dotenv()


# Constants
URL_KIWI = "https://tequila-api.kiwi.com"


# Variables
kiwi_key = os.getenv("KIWI_KEY")
kiwi_loc = f"{URL_KIWI}/locations/query"


# Classes
class FlightSearch:
    """ This class is responsible for talking to the Flight Search API. """

    def __init__(self):
        pass

    def query_city_code(self, search_city):
        search_params = {
            "term": search_city,
            "location_types": "airport",
            "apikey": kiwi_key,
        }
        response = requests.get(url=kiwi_loc, params=search_params)
        response.raise_for_status()

        location_data = response.json()["locations"]
        city_code = location_data[0]["city"]["code"]
        return city_code


# Main
if __name__ == "__main__":
    # pass
    fs = FlightSearch()
    data = fs.query_city_code("Paris")
    pprint(data)
