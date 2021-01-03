import os
import requests
from dotenv import load_dotenv
load_dotenv()


# Constants
URL_USERS_DATA = os.getenv("URL_USER_DATA")


# Variables
auth_flight_data = (os.getenv("SHEETY_AUTH_USERNAME"),
                    os.getenv("SHEETY_AUTH_PASSWORD"))


# Classes
class UserManager():
    """  """

    def __init__(self):
        pass

    def new_user(self):
        pass

    def add_user(self, user):
        pass


class User():
    """  """

    def __init__(self):
        self.first_name = input("Enter your first name: ")
        self.last_name = input("Enter your last name: ")
        self.get_email()

    def get_email(self):
        self.email1 = input("Enter your email: ")
        self.email2 = input("Enter your email again: ")
        self.validate_email()

    def validate_email(self):
        if self.email1 != self.email2:
            print("\nYour email entries don't match, please enter them again")
            self.get_email()


# Main
if __name__ == "__main__":
    user = User()
