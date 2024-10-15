import requests
from django.conf import settings

def fetch_superhero_data(hero_id):
    url = f"https://superheroapi.com/api/{settings.SUPERHERO_API_KEY}/{hero_id}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None
