import os
import requests
from dotenv import load_dotenv
load_dotenv()


# Constants
URL_USERS_DATA = os.getenv("URL_USER_DATA")
AUTH_FLIGHT_DATA = (os.getenv("SHEETY_AUTH_USERNAME"),
                    os.getenv("SHEETY_AUTH_PASSWORD"))


# Classes
class User():
    """  """

    def __init__(self):
        self.first_name = input("Enter your first name: ")
        self.last_name = input("Enter your last name: ")
        self.get_email()

    def get_email(self):
        email1 = input("Enter your email: ")
        email2 = input("Enter your email again: ")
        self.validate_email(email1, email2)
        self.email = email1

    def validate_email(self, email1, email2):
        if email1 != email2:
            print("\nYour email entries don't match, please enter them again")
            self.get_email()


class UserManager():
    """  """

    def __init__(self):
        pass

    def new_user(self):
        user = User()
        self.add_user(user)

    def add_user(self, user: User):
        user_data = {
            "user": {
                "firstName": user.first_name,
                "lastName": user.last_name,
                "email": user.email,
            }
        }
        response = requests.post(
            url=URL_USERS_DATA, json=user_data, auth=AUTH_FLIGHT_DATA)
        response.raise_for_status()

    @staticmethod
    def get_user_data():
        response = requests.get(url=URL_USERS_DATA, auth=AUTH_FLIGHT_DATA)
        response.raise_for_status()

        return response.json()["users"]


# Main
if __name__ == "__main__":
    from pprint import pprint

    um = UserManager()
    # um.new_user()
    pprint(um.get_user_data())
