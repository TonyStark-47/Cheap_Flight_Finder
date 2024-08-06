import requests
import os


sheety_endpoint = os.getenv('SHEETY_ENDPOINT')
users_data_endpoint = os.getenv('SHEETY_USERS')

class DataManager:
    #This class is responsible for talking to the Google Sheet.

    def __init__(self): 
        self.headers = {
            'Authorization': f"Bearer {os.getenv('AUTH')}"
        }

    def update_codes(self, row_id, code):
        '''Updates the IATA code of city in google sheets'''
        self.sheety_edit_endpoint = f"{os.getenv('SHEETY_ENDPOINT')}/{row_id}"

        self.flights_data = {
            'price': {
                'iataCode': code
            }
        }

        response = requests.put(url=self.sheety_edit_endpoint, json=self.flights_data, headers=self.headers)
        print(response.text)


    def get_all_data(self): 
        '''Get all data from the google sheet'''
        response = requests.get(url=str(sheety_endpoint), headers=self.headers)
        data = response.json()
        return data['prices']

    def get_users_details(self):
        '''Get all users name and email address from google sheet'''
        response = requests.get(url=users_data_endpoint, headers=self.headers)
        data = response.json()
        return data['users']
