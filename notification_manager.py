from flight_data import FlightData
import os
import smtplib
from dotenv import load_dotenv
load_dotenv()


# Classes
class NotificationManager:
    """ This class is responsible for sending notifications with the deal flight details. """

    def _init__(self, flight_data: FlightData):
        self.flight_data = flight_data

    def generate_flight_price_alert_message(self):
        fd = self.flight_data

        bluf = "Low price flight alert!"
        main = f"Fly to {fd.destination_city}-{fd.destination_airport} from {fd.departure_city}-{fd.departure_airport} for only {fd.price} from {fd.departure_date[0]} to {fd.return_date[0]}"

        self.message = f"{bluf}\n{main}"

    def send_flight_price_email(self):
        (bluf, body) = self.message.split("\n", 1)
        email_msg = f"Subject: {bluf}\n\n{body}".encode("utf-8")

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=os.getenv("MY_EMAIL"),
                             password=os.getenv("EMAIL_PASSWORD"))
            connection.sendmail(
                from_addr=os.getenv("MY_EMAIL"),
                to_addrs=os.os.getenv("TO_EMAIL"),
                msg=email_msg
            )
