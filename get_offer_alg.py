import pylightxl as xl
import Case_Skins as cls
from itertools import chain
import random


# skins = skin-uri care pot pica (cu duplicate)
# skins_set = skin-uri care pot pica (fara duplicate)
def calc_procent(skins, skins_set):
    # numar aparitiile fiecarui skin din skins_set in skins
    # (nu exista skin in skins_set care sa nu existe in skins, sau invers)
    nr = []
    for index, skin in enumerate(skins_set):
        nr_aux = 0
        for i in skins:
            if i == skin:
                nr_aux += 1

        nr[index] = nr_aux

    # atribui sansa pentru fiecare skin in parte
    for i, sansa in enumerate(nr):
        nr[i] = nr[i] / len(skins)

    return nr


# va fi apelata pentru fiecare cutie
def read_xl(db, sheet_name, Cases):
    Covert = []
    Classified = []
    Restricted = []
    Mil = []
    [roww, coll] = db.ws(sheet_name).size
    data = db.ws(sheet_name).range('A2:N' + str(roww))
    for row in data:
        ObjSkin = cls.Skin()
        ObjSkin.name = row[0]
        ObjSkin.weapon = row[1]

        for i in range(0, 10):
            ObjSkin.prices.append(row[i + 3])

        if row[2] == 'Covert':
            Covert.append(ObjSkin)
        if row[2] == 'Classified':
            Classified.append(ObjSkin)
        if row[2] == 'Restricted':
            Restricted.append(ObjSkin)
        if row[2] == 'Mil-Spec':
            Mil.append(ObjSkin)

    Cases.byRarity.append(Covert)
    Cases.byRarity.append(Classified)
    Cases.byRarity.append(Restricted)
    Cases.byRarity.append(Mil)


def cheapest_skin(skin_list, i):
    minimum = 99999
    index = -1

    # cel mai ieftin din raritatea la care ne aflam la acest pas
    # index_2 = indicele skinului curent
    for index_2, skin in enumerate(skin_list):
        if skin.prices[i] != '' and skin.prices[i] != 'N/A':
            if float(skin.prices[i]) < minimum:
                minimum = float(skin.prices[i])
                index = index_2
    if index != -1:
        return skin_list[index]
    else:
        return -1


def expensive_skin(skin_list, i):
    maxim = -1
    index = -1

    # cel mai ieftin din raritatea la care ne aflam la acest pas
    # index_2 = indicele skinului curent
    for index_2, skin in enumerate(skin_list):
        if skin.prices[i] != '' and skin.prices[i] != 'N/A':
            if float(skin.prices[i]) > maxim:
                maxim = float(skin.prices[i])
                index = index_2
    if index != -1:
        return skin_list[index]
    else:
        return -1


# TODO:
#   - trebuie sa adaug si procent de castig minim
#   - sau sa sortez intr-un fel ofertele dupa castigul maxim, iar la categoria 3 sa intre top 33%
#   - functia trebuie sa returneze o oferta random din toate cele posibile pentru gradul primit
#     ca altfel se va afisa mereu aceeasi oferta si nu facem nimic

def generate_offer(Cases, procent_min_win, procent_max_loss):
    best_deals = []
    for case in Cases:

        # luam calitatile pe rand (FN, MW, FT, ...)
        concatenated = chain(range(0, 4), range(5, 9))
        for i in concatenated:

            # pentru fiecare raritate de skin
            # index_0 = indecele raritatii cu 1 mai mare
            for index_0, skin_list in enumerate(case.byRarity[1:]):

                cheap_skin = cheapest_skin(skin_list, i)
                if cheap_skin != -1:

                    # pretul skinului de cumparat * 10
                    trade_price = 10 * float(cheap_skin.prices[i])

                    # desi toate cele 10 skin-uri bagate in trade au aceeasi calitate,
                    # in functie de o valoarea numita float (unica pentru fiecare skin) sunt si sanse sa imi pice un
                    # skin cu o calitate mai mica. Ca sa am acest float pentru fiecare skin, trebuia sa fac o cautare pe
                    # fiecare site in parte si sa fac cate o extractie a float-ului personalizata pentru fiecare.
                    # Pentru moment vom avea o sansa de 50/50 pentru calitatea skin-ului care va pica sa fie de aceeasi
                    # calitate, sau cu una mai proasta.
                    float_chance = random.randint(0, 1)

                    float_chance = 0

                    cheap_skin_2 = cheapest_skin(case.byRarity[index_0], i + float_chance)
                    expensive_skin_2 = expensive_skin(case.byRarity[index_0], i + float_chance)
                    if cheap_skin_2 != -1 and expensive_skin_2 != -1:
                        float(cheap_skin_2.prices[i + float_chance])
                        float(expensive_skin_2.prices[i + float_chance])
                        if float(cheap_skin_2.prices[i + float_chance]) / trade_price >= (
                                1 - procent_max_loss / 100) and float(
                                expensive_skin_2.prices[i + float_chance]) / trade_price >= (1 + procent_min_win / 100):
                            # case.name = numele cutiei din care sunt skin-urile
                            # cheap_skin = skin-ul de cumparat (cel mai ieftin de CALITATEA i si RARITATEA index_0-1)
                            # i = indicele calitatii la care sa il cumparam
                            # float_chance = indicele calitatii skin-ului/urilor care poate pica
                            # case.byRarity[index_0] = lista cu skin-ul/urile care pot pica
                            best_deals.append([case.name, cheap_skin, i, float_chance, case.byRarity[index_0],
                                               cheap_skin_2, expensive_skin_2])

    return best_deals


def num_to_quality(number):
    if number == 0:
        return 'FN'
    if number == 1:
        return 'MW'
    if number == 2:
        return 'FT'
    if number == 3:
        return 'WW'
    if number == 4:
        return 'BS'
    if number == 5:
        return 'SFN'
    if number == 6:
        return 'SMW'
    if number == 7:
        return 'SFT'
    if number == 8:
        return 'SWW'
    if number == 9:
        return 'SBS'


def get_offer(prices_list, min_profit_procent, max_loss_procent):
    Cases = []
    db = xl.readxl(prices_list)
    sheet_names = db.ws_names

    for sheet in sheet_names[1:]:
        ObjCase = cls.Case()
        ObjCase.name = sheet
        read_xl(db, sheet, ObjCase)
        Cases.append(ObjCase)

    best_deals = generate_offer(Cases, min_profit_procent, max_loss_procent)

    # returnez o oferta random din cele ce respecta procentele
    # random_trade = random.randint(0, len(best_deals)-1)

    return best_deals  # [random_trade]


# region Print in consola
'''


best_deals = get_offer('Case_data_2.xlsx', 100, 100)

for deal in best_deals:
    index = -1
    for skin in deal[4]:
        if '.' not in skin.prices[deal[2]]:
            index = 1

    if index == -1:
        print()
        print('Cutie: ' + deal[0])
        print('Skin to buy: ' + deal[1].name + ' | ' + deal[1].weapon)

        quality_1 = num_to_quality(deal[2])
        quality_2 = num_to_quality(deal[3])

        print('Quality: ' + quality_1)
        print('Skin cost: ' + str(deal[1].prices[deal[2]]) + '$')
        print('Total invest: ' + str(10 * float(deal[1].prices[deal[2]])) + '$')
        print("Skins' quality: " + quality_2)
        print('Skins to get:')

        for skin in deal[4]:
            print(skin.name + ' ' + skin.weapon + ' ' + str(skin.prices[deal[2]]) + '$')
# '''
# endregion
