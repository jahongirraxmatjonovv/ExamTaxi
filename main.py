import psycopg2

class Place:
    def __init__(self, address, district, neighborhood):
        self.address = address
        self.district = district
        self.neighborhood = neighborhood

    def __str__(self):
        return f"{self.address}, {self.district}, {self.neighborhood}"

class Taxi:
    def __init__(self, taxi_id):
        self.taxi_id = taxi_id

    def __str__(self):
        return f"Taxi ID: {self.taxi_id}"

class TaxiCompany:
    def __init__(self):
        self.taxis = []

    def add_taxi(self, taxi):
        if taxi.taxi_id in [t.taxi_id for t in self.taxis]:
            raise ValueError("Xato TaxiName: .")
        self.taxis.append(taxi)

    def get_available(self):
        return [str(taxi) for taxi in self.taxis]

class Passenger:
    def __init__(self, place):
        self.place = place

    def get_place(self):
        return str(self.place)

class Trip:
    def __init__(self, start_place, end_place):
        self.start_place = start_place
        self.end_place = end_place

    def __str__(self):
        return f"Trip: {self.start_place} -> {self.end_place}"

class TaxiSystem:
    def __init__(self):
        self.taxi_company = TaxiCompany()
        self.trips = []

    def start_trip(self, taxi_id, destination):
        taxi = next((taxi for taxi in self.taxi_company.taxis if taxi.taxi_id == taxi_id), None)
        if taxi:
            trip = Trip(taxi, destination)
            self.trips.append(trip)
        else:
            raise ValueError("taxi yoq")

    def end_trip(self, taxi_id):
        trips = [str(trip) for trip in self.trips if trip.start_place.taxi_id == taxi_id]
        if trips:
            self.trips = [trip for trip in self.trips if trip.start_place.taxi_id != taxi_id]
            return trips
        else:
            raise ValueError("taxi yoq")

    def get_all_trips(self):
        return [str(trip) for trip in self.trips]
if __name__ == "__main__":
    try:
        with psycopg2.connect(database="taxidb", user="postgres", password="ress1234", host="localhost", port="5432") as conn:
            with conn.cursor() as cur:
                schema = """
                CREATE TABLE IF NOT EXISTS places (
                    id SERIAL PRIMARY KEY,
                    address VARCHAR(255) NOT NULL,
                    district VARCHAR(255) NOT NULL,
                    neighborhood VARCHAR(255) NOT NULL
                );

                CREATE TABLE IF NOT EXISTS taxis (
                    id SERIAL PRIMARY KEY
                );

                CREATE TABLE IF NOT EXISTS taxi_trips (
                    id SERIAL PRIMARY KEY,
                    taxi_id INTEGER REFERENCES taxis(id),
                    start_place_id INTEGER REFERENCES places(id),
                    end_place_id INTEGER REFERENCES places(id)
                );
                """
                cur.execute(schema)

                places_data = [
                    ("IbnSino street", "Shayhontohur", "15 dom"),
                    ("Shirin street", "Chilonzor", "12 kocha"),
                ]
                for place_data in places_data:
                    cur.execute("INSERT INTO places (address, district, neighborhood) VALUES (%s, %s, %s)", place_data)

                taxis_data = [
                    (1,),
                    (2,),
                ]
                for taxi_data in taxis_data:
                    cur.execute("INSERT INTO taxis DEFAULT VALUES")

                conn.commit()

    except psycopg2.Error as e:
        print(f"Error: {e}")
    taxi_system = TaxiSystem()

    taxi_system.taxi_company.add_taxi(Taxi(taxi_id=1))
    taxi_system.taxi_company.add_taxi(Taxi(taxi_id=2))

    try:
        taxi_system.start_trip(taxi_id=1, destination=Place("IbnSino street", "Shayhontohur", "15-dom"))
    except ValueError as e:
        print(f"Error: {e}")

    try:
        ended_trips = taxi_system.end_trip(taxi_id=1)
        print("Ended :")
        for trip in ended_trips:
            print(trip)
    except ValueError as e:
        print(f"Error: {e}")

    all_trips = taxi_system.get_all_trips()
    print("All :")
    for trip in all_trips:
        print(trip)