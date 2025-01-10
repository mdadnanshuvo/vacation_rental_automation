# config/locations.py

from faker import Faker

fake = Faker()

def get_random_location():
    return fake.city()


