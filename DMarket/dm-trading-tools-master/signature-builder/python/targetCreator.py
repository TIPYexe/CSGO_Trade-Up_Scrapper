import json
from datetime import datetime

from nacl.bindings import crypto_sign
import requests

# replace with your api keys
public_key = "8928b349e84ed6159077e9177852fdb4839383966ba19fb71f2088d1cf929a68"
secret_key = "fb3a8b16f0f67b8c64883d6860a6bbbcd7d20b88f73bc602b5f7a41f494cb40f8928b349e84ed6159077e9177852fdb4839383966ba19fb71f2088d1cf929a68"

# change url to prod
rootApiUrl = "https://api.dmarket.com"

def get_offer_from_market():
    market_response = requests.get(rootApiUrl + "/price-aggregator/v1/aggregated-prices?Titles=Desolate%20Space&Limit=10")
    offers = json.loads(market_response.text)["objects"]
    return offers[0]


def build_target_body_from_offer(offer):
    return {"targets": [
        {"amount": 1, "gameId": offer["gameId"], "price": {"amount": "2", "currency": "USD"},
         "attributes": {"gameId": offer["gameId"],
                        "categoryPath": offer["extra"]["categoryPath"],
                        "title": offer["title"],
                        "name": offer["title"],
                        "image": offer["image"],
                        "ownerGets": {"amount": "1", "currency": "USD"}}}
    ]}


nonce = str(round(datetime.now().timestamp()))
api_url_path = "/exchange/v1/target/create"
method = "POST"
offer_from_market = get_offer_from_market()

body = build_target_body_from_offer(offer_from_market)
string_to_sign = method + api_url_path + json.dumps(body) + nonce
signature_prefix = "dmar ed25519 "
encoded = string_to_sign.encode('utf-8')
secret_bytes = bytes.fromhex(secret_key)
signature_bytes = crypto_sign(encoded, bytes.fromhex(secret_key))
signature = signature_bytes[:64].hex()
headers = {
    "X-Api-Key": public_key,
    "X-Request-Sign": signature_prefix + signature,
    "X-Sign-Date": nonce
}

resp = requests.post(rootApiUrl + api_url_path, json=body, headers=headers)
print(resp.text)
