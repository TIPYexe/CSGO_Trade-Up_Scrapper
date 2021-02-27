import requests
from bs4 import BeautifulSoup as bs
import Case_Skins as cls
from PIL import Image

#region Extrag numele cutiilor


def extract_case_link_name(data):
    return (data.find('a').get('href'), data.find('img').get('alt'))


# pastrez doar diviziunile cu date despre cutii
# adica fara datele extrase gresit
def filter_cases(case_text):

    img_stat = case_text.find('img') is not None
    if not img_stat:
        return False

    case_name = case_text.find('img').get('alt')
    except_1 = case_name != 'All Skin Cases'
    except_2 = case_name != 'Souvenir Packages'
    except_3 = case_name != 'Gift Packages'

    if except_1 and except_2 and except_3:
        return True

def extract_data(data):
    data_filtered = set(filter(filter_cases, data))
    return set(map(extract_case_link_name, data_filtered))

#endregion


def extract_skin_from(URL, ObjCase, text_Var, window):
    page = requests.get(URL)
    soup = bs(page.content, features='html.parser')

    case_name = soup.find('h1', {'class': 'margin-top-sm'}).text

    skin_boxes = soup.findAll('div', {'class': 'col-lg-4 col-md-6 col-widen text-center'})


    # nu iau prima fereastra pentru ca este cu cutite, si nu poti face trade cu ele
    for box in skin_boxes[1:]:
        ObjSkin = cls.Skin()

        # extrage numele skinului si al armei, separat
        ObjSkin.weapon = box.find('h3').text.split(" | ")[0]
        ObjSkin.name = box.find('h3').text.split(" | ")[1]
        ObjSkin.rarity = box.find('p', {'class': 'nomargin'}).text.split(' ')[0]
        ObjCase.Skins.append(ObjSkin)

        # salvez imaginea skin-ului pentru a o folosi in interfata
        image = box.find('img')
        image_url = image['src']
        image_final = Image.open(requests.get(image_url, stream=True).raw)
        image_final.save('Files/Skins/' + ObjSkin.weapon + ' ' + ObjSkin.name + '.png', 'PNG')

        # afisez in log viewer detalii despre skin, ca sa arat ca programul functioneaza

        print_to_log('Extracted skin: ' + ObjSkin.name + ' | ' + ObjSkin.weapon + ' from case: ' + ObjCase.name,
                     text_Var, window)


# adaug text in log viewer
# dau window.update() pentru ca altfel ar rula algoritmul pana la final si abia atunci ar afisa ce e de afisat
# iar eu vreau infromatia sa fie afisata live, pe masura ce este gasita de scrapper
def print_to_log(text, text_Var, window):
    text_Var.set(text_Var.get() + '\n' + text)
    window.update()


def extract_from_cases(URL, text_Var, window):
    page = requests.get(URL)
    soup = bs(page.content, features='html.parser')

    menu = soup.find('div', {'id': 'navbar-expandable'}).find('ul')
    all_buttons = menu.findAll('li', {'class': 'dropdown'})

    ok = 0
    for button in all_buttons:

        menu = button.findAll('a', {'href': '#'})

        # Cand gasesc butonul 'Cases' ok devine 1 si for-ul se opreste
        for row in menu:
            if (row.contents[0] == 'Cases'):
                ok = 1
                break

        if ok == 1:
            break

    elem_menu = button.findAll('li')  # accesez lista de elemente din dropdown_menu
    elem_menu_set = set(elem_menu)  # o transform intr-o lista numarabila

    print_to_log("Gata extractia din meniu", text_Var, window)

    Cases = []
    for case_Link, case_Name in extract_data(elem_menu_set):
        ObjCase = cls.Case()
        ObjCase.name = case_Link.split('/')[5].replace('-', ' ')
        ObjCase.link = case_Link
        extract_skin_from(ObjCase.link, ObjCase, text_Var, window)
        Cases.append(ObjCase)

    print_to_log("Gata extractia din cutii", text_Var, window)

    return Cases

