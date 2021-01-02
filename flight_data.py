from datetime import date, timedelta

# Classes


class FlightData:
    """ This class is responsible for structuring the flight data. """
    pass


class FlightQuery:

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


# Main
if __name__ == "__main__":
    fq = FlightQuery("WAS", "PAR")
    print(fq.flight_params)
