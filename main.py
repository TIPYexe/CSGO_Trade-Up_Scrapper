import web_scrapper as scrapper
import dmarket_api as api
import save_to_db as save

URL = 'https://csgostash.com/containers/skin-cases'



if __name__ == '__main__':

    Cases = scrapper.extract_from_cases(URL)

    # Lista de cutii si procentul pe care sa nu il depaseasca un skin
    # (daca skin-ul valoreaza 10$ si cineva se gaseste sa il vanda cu un pret iesit din comun rau de tot, gen 20$
    # sa nu il luam in calcul)
    api.insert_offer_to_DB(Cases, 10)

    print("Gata extractia de preturi")

    # Salvez datele extrase intr-un Excel
    save.to_xlsx(Cases, 'Case_data.xlsx')

    '''
    for case in set(Cases):
        print("Case Name: " + case.name)
        print("Link: " + case.link)
        for skin in case.Skins:
            print("Weapon: " + skin.weapon + " | Skin: " + skin.name)
            print("FN " + skin.extra['FN'])
            print("FT " + skin.extra['FT'])
            print("SFN " + skin.extra['SFN'])
        print()
    #'''

