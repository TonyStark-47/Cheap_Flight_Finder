from datetime import datetime, timedelta

from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

ORIGIN_CITY_IATA = "BOM"

data_manager = DataManager()
flightSearch = FlightSearch()
notificationManager = NotificationManager()


sheet_data = data_manager.get_all_data()

# to update IATA code in google sheets.
if sheet_data[0]['iataCode'] == "":
    city_names = [row['city'] for row in sheet_data]
    print(city_names)
    IATA_code = [flightSearch.get_IATA_code(city) for city in city_names]
    for row, code in zip(sheet_data, IATA_code):
        data_manager.update_codes(row['id'], code)


tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination in sheet_data:
    flight = flightSearch.find_cheap_flight(
        origin_city_code=ORIGIN_CITY_IATA,
        destination_city_code=destination['iataCode'],
        from_time=tomorrow,
        to_time=six_month_from_today
    )

    if flight is None:
        continue

    if flight.price <= destination['lowestPrice']:
        message = f'''Low price alert! Only Rs.{round(flight.price * 90.3, 2)} to fly from {flight.origin_city}-{flight.origin_airport}, {flight.origin_country} to {flight.destination_city}-{flight.destination_airport}, {flight.destination_country}, from {flight.out_date} to {flight.return_date}.'''

        print(message)
        # notificationManager.notify_me(message)    # less balance
        all_users_data = data_manager.get_users_details()
        names = [f"{user['firstName']} {user['lastName']}" for user in all_users_data]
        emails = [user['email'] for user in all_users_data]
        notificationManager.send_emails(message=message, user_names=names, user_emails=emails)
