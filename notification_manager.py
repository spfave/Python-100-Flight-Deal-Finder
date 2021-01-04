from flight_data import FlightData
import os
import smtplib
from user_manager import UserManager
from dotenv import load_dotenv
load_dotenv()


# Classes
class NotificationManager:
    """ This class is responsible for sending notifications with the deal flight details. """

    def __init__(self):
        pass

    def send_flight_price_email(self, flight_data):
        message = self.generate_flight_price_alert_message(flight_data)
        self.send_email(message, os.getenv("TO_EMAIL"))

    def send_flight_price_emails(self, flight_data):
        message = self.generate_flight_price_alert_message(flight_data)

        users = UserManager.get_user_data()
        for user in users:
            self.send_email(user["email"], message)

    def generate_flight_price_alert_message(self, flight_data: FlightData):
        fd = flight_data

        bluf = f"Low price flight alert for {fd.destination_city}!"
        main = f"Fly to {fd.destination_city}-{fd.destination_airport} from {fd.departure_city}-{fd.departure_airport} for only ${fd.price}. Travel dates are from {fd.departure_date} to {fd.return_date}. "

        if fd.num_flights_to == 2:
            main += f"Outbound flight has {fd.num_flights_to-1} layover in {fd.route_to[1]}"
        elif fd.num_flights_to > 2:
            main += f"Outbound flight has {fd.num_flights_to-1} layovers in {', '.join(fd.route_to[1:-3])} and {fd.route_to[-2]}"

        url_google_flights = "https://www.google.co.uk/flights?hl=en#flt="
        flight_link = f"{url_google_flights}{fd.departure_airport}.{fd.destination_airport}.{fd.departure_date}*{fd.destination_airport}.{fd.departure_airport}.{fd.return_date}"

        return f"{bluf}\n{main}\n\n{flight_link}"

    def send_email(self, user_email, message):
        (bluf, body) = message.split("\n", 1)
        email_msg = f"Subject: {bluf}\n\n{body}".encode("utf-8")

        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=os.getenv("MY_EMAIL"),
                             password=os.getenv("EMAIL_PASSWORD"))
            connection.sendmail(
                from_addr=os.getenv("MY_EMAIL"),
                to_addrs=user_email,
                msg=email_msg
            )
