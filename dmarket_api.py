import requests
import json
import time

# change url to prod
rootApiUrl = "https://api.dmarket.com/exchange/v1/market/items?gameId=a8db&limit=100&offset=1&orderBy=price&orderDir=asc&currency=USD&priceFrom=0&priceTo=0&title="


# Exemplu cu Minimal Wear
# &title=M4A4%20%7C%20Desolate%20Space%20%28Minimal%20Wear%29&limit=50&offset=1&orderBy=title&orderDir=asc&currency=USD&priceFrom=0&priceTo=0

# Exemplu cu StatTrak
# &title=StatTrak%E2%84%A2%20M4A4%20%7C%20Desolate%20Space%20%28Factory%20New%29&limit=50&offset=1&orderBy=title&orderDir=asc&currency=USD&priceFrom=0&priceTo=0
# fara TM (merge la fel)
# &title=StatTrak%20M4A4%20%7C%20Desolate%20Space%20%28Factory%20New%29&limit=50&offset=1&orderBy=title&orderDir=asc&currency=USD&priceFrom=0&priceTo=0
# Ordonarea: &orderBy=price&orderDir=asc

def tradable_only(offer):
    if str(offer['extra']["tradable"]).lower() == 'true':
        return True
    return False


def no_StatTrak(offer):
    if ('stattrak' in offer['title'].lower()):
        return False
    return True


quality = ['Factory New', 'Minimal Wear', 'Field Tested', 'Well Worn', 'Battle Scarred']


def get_offer_from_market(skin_name):
    # pun %20 in loc de spatii pentru a creea link-ul
    market_response = requests.get(
        rootApiUrl + str(skin_name).replace(' ', '%20'))
    offers = json.loads(market_response.text)["objects"]
    return offers


def add_price(skin, price, index):
    if index == 0:
        skin.extra.FN = price
        # print('FN: ' + str(skin.extra.FN))
    if index == 1:
        skin.extra.MW = price
        # print('WW: ' + str(skin.extra.MW))
    if index == 2:
        skin.extra.FT = price
        # print('FT: ' + str(skin.extra.FT))
    if index == 3:
        skin.extra.WW = price
        # print('WW: ' + str(skin.extra.WW))
    if index == 4:
        skin.extra.BS = price
        # print('BS: ' + str(skin.extra.BS))
    if index == 5:
        skin.extra.SFN = price
        # print('SFN: ' + str(skin.extra.SFN))
    if index == 6:
        skin.extra.SMW = price
        # print('SMW: ' + str(skin.extra.SMW))
    if index == 7:
        skin.extra.SFT = price
        # print('SFT: ' + str(skin.extra.SFT))
    if index == 8:
        skin.extra.SWW = price
        # print('SWW: ' + str(skin.extra.SWW))
    if index == 9:
        skin.extra.SBS = price
        # print('SBS: ' + str(skin.extra.SBS))


def insert_offer_to_DB(Cases, procent):
    for case in set(Cases):
        for skin in case.Skins:

            # fara StatTrak
            for index, q in enumerate(quality):

                # am limita de 2 request-uri pe secunda. Si nu vreau sa fortez mai multe requesturi
                # pentru ca nu stiu daca ar ramane in coada, sau pur si simplu ar fi ignorate request-urile
                # facute in timpul cooldown-ului. Iar asta ar crea confuzie in baza de date
                time.sleep(1)

                # Factory New = FN
                short_q = q.split(' ')[0][0] + q.split(' ')[1][0]

                # filtrez doar ofertele de skin-uri fara stattrak prima oara,
                # si care sunt tradeable (ca sa fiu sigur ca pot face tranzactia pe loc, fara sa astept cate zile de
                # tradeban are skin-ul
                # 7C = '|'
                offer_from_market = get_offer_from_market(skin.weapon + ' ' + skin.name + ' ' + q)
                filtered_offers = [d for d in offer_from_market if str(d['extra']['tradable']).lower() == 'true']
                no_stattrak_offers = [d for d in filtered_offers if ~('stattrak' in d['title'].lower())]

                # daca exista cel putin o oferta
                if len(no_stattrak_offers) > 0:

                    total_price = int(no_stattrak_offers[0]['price']['USD'])
                    nr_prices = 1
                    for offerr in no_stattrak_offers[1:]:

                        # iau o oferta in considerare doar daca e cu maxim 20% mai scumpa decat oferta medie
                        # pentru ca mereu sunt oameni care incearca sa vanda la un pret mult mai mare, si ar
                        # face calculele irelevante. Doar pt ca unul vinde la 1000$ un skin de 10$ risc sa nu
                        # iau in considerare skin-ul respectiv.
                        if int(offerr['price']['USD']) <= total_price / nr_prices * (1 + procent / 100):
                            total_price += int(offerr['price']['USD'])
                            nr_prices = nr_prices + 1

                    # Salvez pretul mediu de vanzare a skinului de calitatea short_q
                    # print(skin.weapon + ' | ' + skin.name)
                    add_price(skin, total_price / nr_prices / 100, index)

                # cu StatTrak
                offer_from_market = get_offer_from_market(
                    'StatTrak ' + skin.weapon + ' ' + skin.name + ' ' + q)
                filtered_offers = [d for d in offer_from_market if str(d['extra']['tradable']).lower() == 'true']

                if len(filtered_offers) > 0:
                    total_price = int(filtered_offers[0]['price']['USD'])
                    nr_prices = 1
                    for offer in filtered_offers[1:]:
                        if int(offer['price']['USD']) <= total_price / nr_prices * (1 + procent / 100):
                            total_price += int(offer['price']['USD'])
                            nr_prices += 1

                    # print(skin.weapon + ' | ' + skin.name)
                    add_price(skin, total_price / nr_prices / 100, index + 5)
                    # print()
