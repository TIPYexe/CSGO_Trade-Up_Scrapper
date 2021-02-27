import json
import requests

# change url to prod
rootApiUrl = "https://api.dmarket.com/exchange/v1/market/items?gameId=a8db"
# Exemplu cu Minimal Wear
# &title=M4A4%20%7C%20Desolate%20Space%20%28Minimal%20Wear%29&limit=50&offset=1&orderBy=title&orderDir=asc&currency=USD&priceFrom=0&priceTo=0

# Exemplu cu StatTrak
# &title=StatTrak%E2%84%A2%20M4A4%20%7C%20Desolate%20Space%20%28Factory%20New%29&limit=50&offset=1&orderBy=title&orderDir=asc&currency=USD&priceFrom=0&priceTo=0
# fara TM (merge la fel)
# &title=StatTrak%20M4A4%20%7C%20Desolate%20Space%20%28Factory%20New%29&limit=50&offset=1&orderBy=title&orderDir=asc&currency=USD&priceFrom=0&priceTo=0

def get_offer_from_market():
    market_response = requests.get(
        rootApiUrl + "&title=desolate%20space&limit=100&offset=1&orderBy=price&orderDir=asc&currency=USD&priceFrom=0&priceTo=0")
    offers = json.loads(market_response.text)["objects"]
    return offers

offer_from_market = get_offer_from_market()
for offer in offer_from_market:
    print("Nume: " + offer["title"] + " Price: " + offer['price']['USD'] + " " + str(offer['extra']["tradable"]))
