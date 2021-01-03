import os
import requests
from dotenv import load_dotenv
from flight_search import FlightSearch
from flight_data import FlightQuery, FlightData
from notification_manager import NotificationManager
load_dotenv()


# Constants
URL_FLIGHT_DATA = os.getenv("URL_FLIGHT_DATA")
AUTH_FLIGHT_DATA = (os.getenv("SHEETY_AUTH_USERNAME"),
                    os.getenv("SHEETY_AUTH_PASSWORD"))
DEPARTURE_CITY = "WAS"


# Classes
class DataManager:
    """ This class is responsible for talking to the Google Flight Deals Sheet. """

    def __init__(self):
        self.destinations = self.get_destination_data()
        self.flight_search = FlightSearch()

    @staticmethod
    def get_destination_data():
        response = requests.get(url=URL_FLIGHT_DATA, auth=AUTH_FLIGHT_DATA)
        response.raise_for_status()

        return response.json()["prices"]

    def check_destination_codes(self):
        """ Evaluate if destination (city) IATA code is empty string. 
            If so populate with city IATA code and update in spreadsheet data
        """

        for destination in self.destinations:
            if destination["iataCode"] == "":
                city_code = self.flight_search.query_city_code(
                    destination["city"])
                destination["iataCode"] = city_code

                self.update_destination_code(destination)

    def update_destination_code(self, destination):
        destination_row = f"{URL_FLIGHT_DATA}/{destination['id']}"
        destination_data = {
            "price": {
                "iataCode": destination["iataCode"],
            },
        }
        response = requests.put(url=destination_row,
                                json=destination_data, auth=AUTH_FLIGHT_DATA)
        response.raise_for_status()

    def check_destination_prices(self):
        for destination in self.destinations:
            flight = self.find_flight(destination)

            if flight == None:
                continue

            flight_data = FlightData(flight)
            if flight_data.price <= destination["maxPrice"]:
                flight_notification = NotificationManager(flight_data)
                flight_notification.send_flight_price_email()

    def find_flight(self, destination):
        fq = FlightQuery(departure_loc=DEPARTURE_CITY,
                         arrival_loc=destination["iataCode"],
                         nights_min=7, nights_max=28,
                         max_stopovers=0,
                         currency="USD")
        flight = self.flight_search.query_flight(fq.flight_params)
        if flight == None:
            fq.flight_params['max_stopovers'] = 1
            flight = self.flight_search.query_flight(fq.flight_params)

        return flight


# Main
if __name__ == "__main__":
    from pprint import pprint

    dm = DataManager()
    # pprint(dm.destinations)

    # dm.check_destination_codes()
    # pprint(dm.destinations)

    dm.check_destination_prices()
