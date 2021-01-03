from datetime import date, timedelta


# Classes
class FlightData:
    """ This class is responsible for structuring the flight data. """

    def __init__(self, flight_data):
        self.process_data(flight_data)
        self.process_route(flight_data)

    def process_data(self, flight_data):
        self.departure_city = flight_data["cityFrom"]
        self.destination_city = flight_data["cityTo"]

        self.departure_airport = flight_data["flyFrom"]
        self.destination_airport = flight_data["flyTo"]

        self.departure_date = flight_data["route"][0][
            "local_departure"].split("T")[0]
        self.return_date = flight_data["route"][-1][
            "local_arrival"].split("T")[0]

        self.price = flight_data["price"]

    def process_route(self, flight_data):
        self.route_to = []
        self.route_from = []

        route = self.route_to
        for flight in flight_data["route"]:
            start = flight["cityFrom"]
            end = flight["cityTo"]

            if start == self.departure_city or start == self.destination_city:
                route.append(start)

            if end == self.destination_city:
                route.append(end)
                route = self.route_from
            else:
                route.append(end)

        self.num_flights_to = len(self.route_to)-1
        self.num_flights_from = len(self.route_from)-1


class FlightQuery:
    """ This class is responsible for structuring the flight query data. """

    def __init__(self, departure_loc, arrival_loc, **kwargs):
        self.required_params(departure_loc, arrival_loc, **kwargs)
        self.optional_params(**kwargs)

    def required_params(self, departure_loc, arrival_loc, **kwargs):
        date_travel_start = kwargs.get(
            "date_travel_start", date.today()+timedelta(days=1))
        date_travel_end = kwargs.get(
            "date_travel_end", date.today()+timedelta(days=180))

        self.flight_params = {
            "fly_from": departure_loc,
            "fly_to": arrival_loc,
            "date_from": date_travel_start.strftime("%d/%m/%Y"),
            "date_to": date_travel_end.strftime("%d/%m/%Y"),
        }

    def optional_params(self, **kwargs):
        if "nights_min" in kwargs and "nights_max" in kwargs:
            self.flight_params["nights_in_dst_from"] = kwargs.get("nights_min")
            self.flight_params["nights_in_dst_to"] = kwargs.get("nights_max")
        if "currency" in kwargs:
            self.flight_params["curr"] = kwargs.get("currency")
        if "price_max" in kwargs:
            self.flight_params["price_to"] = kwargs.get("price_max")
        if "flight_type" in kwargs:
            self.flight_params["flight_type"] = kwargs.get("flight_type")
        if "one_per_date" in kwargs:
            self.flight_params["one_per_date"] = kwargs.get("one_per_date")
        if "max_stopovers" in kwargs:
            self.flight_params["max_stopovers"] = kwargs.get("max_stopovers")


# Main
if __name__ == "__main__":
    fq = FlightQuery("WAS", "PAR")
    print(fq.flight_params)
