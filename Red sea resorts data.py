import random
import json
from faker import Faker

fake = Faker()

def get_Resorts_data(resortId):
    print("Executing get_Resorts_data ...")

    
    resort_names = [
        'Coral Beach Resort', 'Red Sea Oasis', 'Azure Bay Resort', 'Sunrise Paradise',
        'Blue Horizon', 'Lagoon Retreat', 'Ocean Breeze', 'Sunny Shores'
    ]
    locations = ['Hurghada', 'Sharm El-Sheikh', 'Marsa Alam', 'Dahab', 'Ain Sokhna']
    room_types = ['Single', 'Double', 'Suite', 'Family Suite']
    activities = ['Diving', 'Snorkeling', 'Spa', 'Beach Volleyball', 'Wind Surfing', 'Boat Tours']

    resort_data = {
        "resort_id": resortId,
        "name": random.choice(resort_names),
        "location": random.choice(locations),
        "rooms_available": random.randint(50, 300),
        "average_price_per_night": round(random.uniform(100, 500), 2),
        "room_types": random.sample(room_types, k=random.randint(1, len(room_types))),
        "popular_activities": random.sample(activities, k=random.randint(1, len(activities))),
        "rating": round(random.uniform(3.0, 5.0), 1),
        "contact_email": fake.email(),
        "contact_phone": fake.phone_number(),
        "website": fake.url(),
        "is_open": random.choice([True, False]),
        "last_renovation_date": fake.date_between(start_date='-10y', end_date='today').strftime('%Y-%m-%d')
    }

    return json.dumps(resort_data, indent=4)


print(get_Resorts_data("R12345"))