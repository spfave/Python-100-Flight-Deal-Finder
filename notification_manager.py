from flight_data import FlightData
import os
import smtplib
from dotenv import load_dotenv
load_dotenv()


# Classes
class NotificationManager:
    """ This class is responsible for sending notifications with the deal flight details. """

    def __init__(self, flight_data: FlightData):
        self.flight_data = flight_data

    def generate_flight_price_alert_message(self):
        fd = self.flight_data

        bluf = f"Low price flight alert for {fd.destination_city}!"
        main = f"Fly to {fd.destination_city}-{fd.destination_airport} from {fd.departure_city}-{fd.departure_airport} for only ${fd.price}. Travel dates are from {fd.departure_date[0]} to {fd.return_date[0]}. "

        if fd.num_flights_to == 2:
            main += f"Outbound flight has {fd.num_flights_to-1} layover in {fd.route_to[1]}"
        elif fd.num_flights_to > 2:
            main += f"Outbound flight has {fd.num_flights_to-1} layovers in {', '.join(fd.route_to[1:-3])} and {fd.route_to[-2]}"

        self.message = f"{bluf}\n{main}"

    def send_flight_price_email(self):
        self.generate_flight_price_alert_message()

        (bluf, body) = self.message.split("\n", 1)
        email_msg = f"Subject: {bluf}\n\n{body}".encode("utf-8")

        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=os.getenv("MY_EMAIL"),
                             password=os.getenv("EMAIL_PASSWORD"))
            connection.sendmail(
                from_addr=os.getenv("MY_EMAIL"),
                to_addrs=os.getenv("TO_EMAIL"),
                msg=email_msg
            )
