import os
import requests
from dotenv import load_dotenv
from datetime import date, timedelta
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
        pass

    def query_city_code(self, search_city):
        search_params = {
            "apikey": kiwi_key,
            "term": search_city,
            "location_types": "airport",
        }
        response = requests.get(url=kiwi_loc, params=search_params)
        response.raise_for_status()

        location_data = response.json()["locations"]
        city_code = location_data[0]["city"]["code"]
        return city_code

    def query_flight(self, departure_loc, arrival_loc, **kwargs):

        date_travel_start = kwargs.get("date_travel_start", date.today()+timedelta(days=1))
        date_travel_end = kwargs.get("date_travel_end", date.today()+timedelta(days=180))

        flight_params = {
            "apikey": kiwi_key,
            "fly_from": departure_loc,
            "fly_to": arrival_loc,
            "date_from": date_travel_start.strftime("%d/%m/%Y"),
            "date_to": date_travel_end.strftime("%d/%m/%Y"),
        }
        if "nights_min" in kwargs and "nights_max" in kwargs:
            flight_params["nights_in_dst_from"] = kwargs.get("nights_min")
            flight_params["nights_in_dst_to"] = kwargs.get("nights_max")
        if "currency" in kwargs:
            flight_params["curr"] = kwargs.get("currency") 
        if "price_max" in kwargs:
            flight_params["price_to"] = kwargs.get("price_max")
        
        response = requests.get(url=kiwi_search, params=flight_params)
        response.raise_for_status()

        return response.json()



# Main
if __name__ == "__main__":
    # pass
    fs = FlightSearch()
    data = fs.query_flight(DEPARTURE_CITY, "PAR", currency="USD", price_max=199)
    pprint(data)
