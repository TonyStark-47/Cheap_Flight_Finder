import requests
from flight_data import FlightData
import os


IATA_endpoint = 'https://api.tequila.kiwi.com/locations/query'
flight_search_endpoint = 'https://api.tequila.kiwi.com/v2/search'

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.

    def __init__(self):
        self.headers = {
            'apikey': os.getenv('FLIGHT_API_KEY'),
        }

    def get_IATA_code(self, city):
        '''Search for the IATA code for the given city and return it.'''
        self.location_query = {
            'term': f'{city}'
        }
        response = requests.get(url=IATA_endpoint, params=self.location_query, headers=self.header)
        data = response.json()
        IATA_code = data['locations'][0]['code']
        return IATA_code

    def find_cheap_flight(self, origin_city_code: str, destination_city_code: str, from_time, to_time):
        '''Search for the cheapest flight in upcoming 6 months time.'''

        search_parameters = {
            'fly_from': origin_city_code,  # IATA code (multiple code seperated by comma)
            'fly_to': destination_city_code,
            'date_from': from_time.strftime("%d/%m/%Y"),   # dd/mm/yyyy
            'date_to': to_time.strftime("%d/%m/%Y"),    
            "nights_in_dst_from": 7,    # round trip
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP",
            # 'one_per_date': 1,  # returns the cheapest flights for each date in the range defined by date_from and date_to.
            # 'selected_cabins': 'M', # M - economy, C - business class
            # 'curr': 'INR',   #EUR(default), use this parameter to change the currency in the response.
            # 'price_to': max_price, # maximum price
            # 'vehicle_type': 'aircraft',  # aircraft(default), bus, train.
            # 'sort': 'date',   #Available values : price(default), duration, quality, date
        }

        response = requests.get(url=flight_search_endpoint, params=search_parameters, headers=self.headers)

        try:
            data = response.json()['data'][0]
            print(f"{destination_city_code}: Rs.{round(data['price'] * 90.3, 2)}")
        except IndexError:
            print(f"No flights found for {destination_city_code}.")
            return None
        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                origin_country=data['countryFrom']['name'],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                destination_country=data['countryTo']['name'],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0]
            )
            return flight_data
