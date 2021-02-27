from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pylightxl as xl
import Case_Skins as cls
import save_to_db as save


def search_skin(Cases, driver, displayVar, window):
    for case in Cases:
        for skin in case.Skins:

            # initializez toate preturile skinului cu -1
            for i in range(0, 11):
                skin.prices.append(-1)

            input_element = driver.find_element_by_id('searchInput')
            input_element.clear()
            input_element.send_keys(skin.weapon + ' ' + skin.name)
            input_element.send_keys(Keys.ENTER)

            # Astept sa se incarce pagina (adica sa apara numele skin-ului in prima caseta din tabel)
            WebDriverWait(driver, 120).until(EC.text_to_be_present_in_element((By.XPATH, '/html/body/div[22]/div/div/div[4]/div/div/div[2]/div/table/tbody/tr[1]'), skin.name))

            # fac media preturilor de pe site-uri si o adaug lui skin, la calitatea care trebuie
            for i in range(1, 11):
                try:
                    table_row = driver.find_element_by_xpath(
                        '/html/body/div[22]/div/div/div[4]/div/div/div[2]/div/table/tbody/tr[' + str(
                            i) + ']').text
                    data = table_row.split(' ')

                    # numar cate caractere sar pentru a ajunge la preturi
                    count = 0
                    for index, elem in enumerate(data):
                        if '(' in elem:
                            count = index + 1
                            break

                    if 'Dragon King' in table_row:
                        count += 2

                    plus1 = 0
                    if 'stattrak' in data[0].lower():
                        plus1 += 1

                    # adaug pretul la CALITATEA care trebuie
                    if '(FN)' in table_row:
                        skin.prices[plus1 * 5 + 0] = data[count]
                    if '(MW)' in table_row:
                        skin.prices[plus1 * 5 + 1] = data[count]
                    if '(FT)' in table_row:
                        skin.prices[plus1 * 5 + 2] = data[count]
                    if '(WW)' in table_row:
                        skin.prices[plus1 * 5 + 3] = data[count]
                    if '(BS)' in table_row:
                        skin.prices[plus1 * 5 + 4] = data[count]

                    print_to_log(skin.weapon + ' | ' + skin.name + ' sells for ' + data[count] + '$ on average.', displayVar, window)

                except NoSuchElementException:
                    print(skin.name + ' nu se gaseste pe atatea calitati.')


# va fi apelata pentru fiecare cutie
def read_xl(db, sheet_name, Cases):
    [roww, coll] = db.ws(sheet_name).size
    data = db.ws(sheet_name).range('A2:N' + str(roww))
    for row in data:
        ObjSkin = cls.Skin()
        ObjSkin.name = row[0]
        ObjSkin.weapon = row[1]
        ObjSkin.rarity = row[2]
        Cases.Skins.append(ObjSkin)

def print_to_log(text, text_Var, window):
    text_Var.set(text_Var.get() + '\n' + text)
    window.update()

def extract_prices(input_file, output_file, displayVar, window):
    Cases = []
    db = xl.readxl(input_file)
    sheet_names = db.ws_names

    for sheet in sheet_names[1:]:
        ObjCase = cls.Case()
        ObjCase.name = sheet
        read_xl(db, sheet, ObjCase)
        Cases.append(ObjCase)


    # adaug niste setari care sa faca Chrome-ul sa nu se mai deschida in forma de testare (asa cum deschide Selenium)
    # pentru ca fara asta nu as putea trece de verificarea Cloudflare
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options)

    driver.get('https://csgo.steamanalyst.com/markets')

    # Am nevoie de 13 secunde sa creez un nou tab de chrome in care sa deschid acelasi link
    # Pe acel nou tab voi trece de verificarea Cloudflare, si dupa se va incarca pagina si pe tabul de lucru
    # iar programul poate rula fara probleme
    time.sleep(13)

    # minimizez fereastra, si o pozitionez intr-un loc inaccesibil
    # astfel, daca utilizatorul nu inchide fereastra, nu poate afecta procesul de cautare
    driver.minimize_window()
    driver.set_window_position(-10000, -10000, windowHandle='current')

    search_skin(Cases, driver, displayVar, window)

    driver.close()

    save.to_xlsx(Cases, output_file, True)