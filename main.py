# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from pprint import pprint


# Main
flight_manager = DataManager()

# flight_data.get_destination_data()
# pprint(flight_manager.destinations)
flight_manager.check_destination_codes()
# pprint(flight_manager.destinations)

flight_manager.check_destination_prices()
