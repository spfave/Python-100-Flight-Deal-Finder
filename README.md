# Python 100 Days of Code

Course: 100 Days of Code - The Complete Python Pro Bootcamp for 2021
Course url: https://www.udemy.com/course/100-days-of-code/

## Section 39: Flight Deal Finder

Flight price deal alert notification app

Sheety API: https://sheety.co/
Flight Search API: https://partners.kiwi.com/
Twilio API: https://www.twilio.com/docs

### Program Requirements:

Use the Flight Search and Sheety API to populate your own copy of the Google Sheet with International Air Transport Association (IATA) codes for each city. Most of the cities in the sheet include multiple airports, you want the city code, not the airport code see here.

Use the Flight Search API to check for the cheapest flights from tomorrow to 6 months later for all the cities in the Google Sheet.

If the price is lower than the lowest price listed in the Google Sheet then send a SMS to your own number with the Twilio API.

- Use smptlib to send email instead

The SMS/email should include the departure airport IATA code, destination airport IATA code, departure city, destination city, flight price and flight dates.

## Section 40: Flight Club

Flight price deal alert notification app modification to message multiple users and notify of flight price alert.

### Program Requirements

New users will be able to sign up for flight price deal notifications

The Flight price deal app will notify all registered users via email of a flight price deal
