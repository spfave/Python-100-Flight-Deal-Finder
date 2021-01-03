import os
import requests
from dotenv import load_dotenv
from flight_search import FlightSearch
from flight_data import FlightQuery, FlightData
from notification_manager import NotificationManager
load_dotenv()


# Constants
URL_FLIGHT_DATA = os.getenv("URL_FLIGHT_DATA")
DEPARTURE_CITY = "WAS"


# Variables
auth_flight_data = (os.getenv("SHEETY_AUTH_USERNAME"),
                    os.getenv("SHEETY_AUTH_PASSWORD"))


# Classes
class DataManager:
    """ This class is responsible for talking to the Google Flight Deals Sheet. """

    def __init__(self):
        self.destinations = self.get_destination_data()
        self.flight_search = FlightSearch()

    def get_destination_data(self):
        response = requests.get(url=URL_FLIGHT_DATA, auth=auth_flight_data)
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
                                json=destination_data, auth=auth_flight_data)
        response.raise_for_status()

    def check_destination_prices(self):
        for destination in self.destinations:
            fq = FlightQuery(departure_loc=DEPARTURE_CITY,
                             arrival_loc=destination["iataCode"],
                             nights_min=7, nights_max=28,
                             currency="USD")
            flight = self.flight_search.query_flight(fq.flight_params)
            flight_data = FlightData(flight)

            if flight_data.price <= destination["maxPrice"]:
                flight_notification = NotificationManager(flight_data)
                flight_notification.send_flight_price_email()


# Main
if __name__ == "__main__":
    # pass
    dm = DataManager()
    data = dm.get_destination_data()

    print(data)
