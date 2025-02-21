class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, price, origin_city, origin_airport, origin_country, destination_city, destination_airport, destination_country, out_date, return_date, stop_overs=0, via_city=""):
        self.price = price
        self.origin_city = origin_city
        self.origin_airport = origin_airport
        self.origin_country = origin_country,
        self.destination_city = destination_city
        self.destination_airport = destination_airport
        self.destination_country = destination_country,
        self.out_date = out_date
        self.return_date = return_date

        self.stop_overs = stop_overs
        self.via_city = via_city
