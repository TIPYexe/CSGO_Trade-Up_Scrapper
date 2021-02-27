import tkinter as tk
from PIL import ImageTk, Image
from pylightxl import readxl
import os.path
from os import path

import price_scrapper as pricey
import Case_Skins as cls
import web_scrapper as cs_scrp
import get_offer_alg as alg
import save_to_db as save


def updateDisplay(myString):
    displayVar.set(displayVar.get() + '\n' + myString)


def extract_skins(event):
    # dezactivez butonul
    btn_UpdateDB['state'] = 'disabled'
    btn_UpdateDB.unbind("<Button-1>")
    # curat fereastra de log
    displayVar.set('')
    window.update()

    # functia propriu-zisa
    Cases = cs_scrp.extract_from_cases('https://csgostash.com/containers/skin-cases', displayVar, window)
    save.to_xlsx(Cases, 'Files/Skin_names.xlsx', False)

    # reactivez butonul
    btn_UpdateDB['state'] = 'active'
    btn_UpdateDB.bind("<Button-1>", extract_skins)

    # activez si butonul pentru preturi in cazul in care era dezactivat
    btn_UpdatePrices['state'] = 'active'
    btn_UpdatePrices.bind("<Button-1>", extract_prices)


def extract_prices(event):
    # dezactivez butonul
    btn_UpdatePrices['state'] = 'disabled'
    btn_UpdatePrices.unbind("<Button-1>")
    # curat fereastra de log
    displayVar.set('')
    window.update()

    # functia propriu-zisa
    db = readxl('Files/Skin_names.xlsx')
    sheet_names = db.ws_names

    for sheet in sheet_names[1:]:
        ObjCase = cls.Case()
        ObjCase.name = sheet
        alg.read_xl(db, sheet, ObjCase)
        Cases.append(ObjCase)

    pricey.extract_prices('Files/Skin_names.xlsx', 'Files/Skin_prices.xlsx', displayVar, window)

    # reactivez butonul
    btn_UpdatePrices['state'] = 'active'
    btn_UpdatePrices.bind("<Button-1>", extract_prices)


# TODO:
#   - sa fac si eu un fisier pentru constante (nume de fisiere and shit)

def get_n_resize(skin_name):
    skin_mare = Image.open('Files/Skins/' + skin_name + '.png')
    skin_mare = skin_mare.resize((94, 71), Image.ANTIALIAS)
    skin_in = ImageTk.PhotoImage(skin_mare)
    return skin_in


def print_trade_in(skin_in):

    x = 15
    y = 390

    for i in range(0, 10):
        skin_in_label = tk.Label(frame, image=skin_in, background='gray63', width=108, height=108)

        if i == 5:
            y = 505
            x = 15

        skin_in_label.place(x=x, y=y)
        x += 115

    window.update()

def search_offer(event, risk):
    if risk == 1:
        deal = alg.get_offer('Files/Skin_prices.xlsx', 17, 0)
    if risk == 2:
        deal = alg.get_offer('Files/Skin_prices.xlsx', 0, 0)
    if risk == 3:
        deal = alg.get_offer('Files/Skin_prices.xlsx', 0, 0)

window = tk.Tk()
window.geometry('825x750')
window.title("CS:GO Trade-up Scrapper")
window.resizable(False, False)

path_logo = 'Files/logo.png'

pixel = tk.PhotoImage(width=1, height=1)

frame = tk.Frame(bg='gray15', height=750, width=825)
frame.pack()

# log_viewer = tk.Frame(master=window, weight=354.49, height=160.93, bg='white')
# log_viewer.pack(fill=tk.Y, side=tk.RIGHT)

image = Image.open(path_logo)
logo = ImageTk.PhotoImage(image)

# este o carpeala de nedescris cu asezarea butoanelor astora
# nu te uita
logo_panel = tk.Label(frame, image=logo, bd=0)
logo_panel.place(x=258, y=13)


#region Main Buttons

btn_UpdateDB = tk.Button(frame, text="EXTRACT\nNAMES", image=pixel, bd=0, background='gray63', fg='gray15',
                         font=('Montserrat Black', 12), width=153, height=63, compound="c")
btn_UpdateDB.place(x=12, y=208)

btn_UpdatePrices = tk.Button(frame, text="EXTRACT\nPRICES", image=pixel, bd=0, background='gray63', fg='gray15',
                             font=('Montserrat Black', 12), width=153, height=63, compound="c")
btn_UpdatePrices.place(x=12, y=284)


# daca fisierul Skin_names nu exista (si deci functia de pe btn-ul update prices nu are putea functiona
# dezactivez butonul
if not path.exists('Files/Skin_names.xlsx'):
    btn_UpdatePrices['state'] = 'disabled'
    btn_UpdatePrices.unbind("<Button-1>")

btn_UpdateDB.bind("<Button-1>", extract_skins)
btn_UpdatePrices.bind("<Button-1>", extract_prices)

#endregion


displayVar = tk.StringVar()
# justify = left (aliniez textul la stanga)
# anchor = 'sw' (ultimul text introdus ramane in josul paginii si oricum redimensionez Label-ul
#               el ramane jos de tot, fara a da resize la fereastra)
displayLab = tk.Label(frame, textvariable=displayVar, height=10, width=55, justify='left', anchor='sw')
displayLab.place(x=178, y=208)


# region Select Risk Level.txt

select_risk = tk.Text(frame, font=('Montserrat Black', 25), bd=0, fg='tan2', bg='gray15', width=10, height=2)
select_risk.tag_configure('center', justify='center')
select_risk.insert('1.0', 'SELECT\nRISK LEVEL')
select_risk.tag_add('center', '1.0', 'end')
select_risk.place(x=575, y=205)

# endregion


# region Butoane Risk

btn_risk1 = tk.Button(frame, text="1", image=pixel, relief='solid', bd=0, background='gold', fg='chocolate2',
                      font=('Montserrat Black', 19), width=35, height=35, compound="c")
btn_risk1.place(x=610, y=310)
btn_risk2 = tk.Button(frame, text="2", image=pixel, relief='solid', bd=0, background='gold', fg='chocolate2',
                      font=('Montserrat Black', 19), width=35, height=35, compound="c")
btn_risk2.place(x=670, y=310)
btn_risk3 = tk.Button(frame, text="3", image=pixel, relief='solid', bd=0, background='gold', fg='chocolate2',
                      font=('Montserrat Black', 19), width=35, height=35, compound="c")
btn_risk3.place(x=730, y=310)

# endregion


bg_trade_up = tk.Label(frame, image=pixel, background='gray80', width=825, height=360)
bg_trade_up.place(x=0, y=379)


skin = cls.Skin()
skin.prices.append(0)
skin.prices.append(125.3154332)
# i = indicele calitatii skin-ului
i = 1


# skin_in trebuie sa fie global, altfel se va sterge poza dupa executarea functiei, si va ramane label-ul gol
skin_in = get_n_resize('AK-47 Aquamarine Revenge')
# afisez cele 10 skinuri
print_trade_in(skin_in)
# afisez date despre skinul de cumparat
skin_in_data = tk.Label(frame, image=skin_in, text='   PRICE\n   ' + str(round(skin.prices[i], 2)) + '$\n   Q: ' + alg.num_to_quality(i),
                        font=('Montserrat Black', 16), fg='Dark green', background='SpringGreen3', width=221, height=108, compound='left')
skin_in_data.place(x=15, y=620)

#region skin_out

skin_out_1 = get_n_resize('AK-47 Aquamarine Revenge')
skin_in_data = tk.Label(frame, image=skin_out_1, text='   PRICE\n   ' + str(round(skin.prices[i], 2)) + '$\n   Q: ' + alg.num_to_quality(i),
                        font=('Montserrat Black', 16), fg='red4', background='brown1', width=216, height=106, compound='left')
skin_in_data.place(x=591, y=390)

skin_out_2 = get_n_resize('AK-47 Aquamarine Revenge')
skin_in_data = tk.Label(frame, image=skin_out_2, text='   PRICE\n   ' + str(round(skin.prices[i], 2)) + '$\n   Q: ' + alg.num_to_quality(i),
                        font=('Montserrat Black', 16), fg='red4', background='brown1', width=216, height=106, compound='left')
skin_in_data.place(x=591, y=505)

skin_out_3 = get_n_resize('AK-47 Aquamarine Revenge')
skin_in_data = tk.Label(frame, image=skin_out_3, text='   PRICE\n   ' + str(round(skin.prices[i], 2)) + '$\n   Q: ' + alg.num_to_quality(i),
                        font=('Montserrat Black', 16), fg='red4', background='brown1', width=216, height=106, compound='left')
skin_in_data.place(x=591, y=620)

#endregion

#region TOTAL
select_risk = tk.Text(frame, font=('Montserrat Black', 22), bd=0, fg='gray34', bg='gray80', width=15, height=3)
select_risk.tag_configure('center', justify='center')
select_risk.insert('1.0', 'TOTAL: ' + str(round(skin.prices[i]*10, 2)) + '$\n'
                                    + 'MAX LOSS: ' + '100' + '$\n'
                                    + 'MIN WIN: ' + '202' + '$')
select_risk.tag_add('center', '1.0', 'end')
select_risk.place(x=265, y=617)
#endregion

# TODO:
#   - la catergoria de get offer sa am 3 butoane care sa reprezinte
#   - gradul de risc pentru trade-ul care urmeaza sa pice
#    1 = spre 0 pierdere
#    3 = sanse la castiguri mari, dar si la pierderi mari


Cases = []



window.mainloop()
