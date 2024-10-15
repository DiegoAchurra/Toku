import requests

SUPERHERO_API_KEY='734f9f77079f5b0c9dfe786f8d072cb6'

def fetch_superhero_data(hero_id):
    url = f"https://superheroapi.com/api/{SUPERHERO_API_KEY}/{hero_id}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None
