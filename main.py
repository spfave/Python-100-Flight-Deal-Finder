#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from pprint import pprint


# Main
flight_data = DataManager()

flight_destination_data = flight_data.get_destination_data()
pprint(flight_destination_data)