import tkinter as tk
from PIL import ImageTk, Image
from pylightxl import readxl
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

    # activez butoanele pt cautarea de oferta
    btn_risk1['state'] = 'active'
    btn_risk1.bind("<Button-1>", lambda event, risk=1: search_offer(event, risk))
    btn_risk2['state'] = 'active'
    btn_risk2.bind("<Button-1>", lambda event, risk=2: search_offer(event, risk))
    btn_risk3['state'] = 'active'
    btn_risk3.bind("<Button-1>", lambda event, risk=3: search_offer(event, risk))



# TODO:
#   - sa fac si eu un fisier pentru constante (nume de fisiere and shit)


def get_n_resize(skin_name):
    skin_mare = Image.open('Files/Skins/' + skin_name + '.png')
    skin_mare = skin_mare.resize((94, 71), Image.ANTIALIAS)
    skin = ImageTk.PhotoImage(skin_mare)
    return skin


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


def search_offer(event, risk):
    deal = []

    if risk == 1:
        # max_loss = 0 deci nu poate iesi in pierdere,
        # dar de regula si castigurile sunt mici
        deal = alg.get_offer('Files/Skin_prices.xlsx', 0, 0)
    if risk == 2:
        deal = alg.get_offer('Files/Skin_prices.xlsx', 100, 40)
    if risk == 3:
        # max_loss = 100 sunt dispus sa pierd toti banii intr-un trade (imposibil oricum)
        deal = alg.get_offer('Files/Skin_prices.xlsx', 200, 100)

    # afisez cele 10 skinuri
    skin_in = get_n_resize(deal[1].weapon + ' ' + deal[1].name)
    print_trade_in(skin_in)

    # afisez date despre skinul de cumparat
    skin_in_q = alg.num_to_quality(deal[2])

    invalid_values = ['N/A', ' ', '']

    if deal[1].prices[deal[2]] not in invalid_values:
        price_0 = str(round(float(deal[1].prices[deal[2]]), 2))
    else:
        price_0 = '-'

    skin_in_data = tk.Label(frame, image=skin_in,
                            text= ' ' + deal[1].name + '\n PRICE: ' + price_0 + '$\n Q: ' + skin_in_q,
                            font=('Montserrat Black', 16), justify='left', fg='Dark green', background='SpringGreen3', width=270,
                            height=108, compound='left')
    skin_in_data.place(x=15, y=620)

    # region skin_out

    skin_out_q = alg.num_to_quality(deal[2] + deal[3])
    if len(deal[4]) >= 1:

        skin_out_1 = get_n_resize(deal[4][0].weapon + ' ' + deal[4][0].name)

        if deal[4][0].prices[deal[2] + deal[3]] not in invalid_values:
            price_1 = str(round(float(deal[4][0].prices[deal[2] + deal[3]]), 2))
        else:
            price_1 = '-'

        skin_out_data_1 = tk.Label(frame, image=skin_out_1,
                                text=' ' + deal[4][0].name + '\n PRICE: ' + price_1 + '$\n Q: ' + skin_out_q,
                                font=('Montserrat Black', 16), justify='left', fg='red4', background='brown1', width=270, height=106,
                                compound='left')
        skin_out_data_1.place(x=605, y=390)

    if len(deal[4]) >= 2:
        skin_out_2 = get_n_resize(deal[4][1].weapon + ' ' + deal[4][1].name)

        if deal[4][1].prices[deal[2] + deal[3]] not in invalid_values:
            price_2 = str(round(float(deal[4][1].prices[deal[2] + deal[3]]), 2))
        else:
            price_2 = '-'

        skin_out_data_2 = tk.Label(frame, image=skin_out_2,
                                text=' ' + deal[4][1].name + '\n PRICE: ' + price_2 + '$\n Q: ' + skin_out_q,
                                font=('Montserrat Black', 16), justify='left', fg='red4', background='brown1', width=270, height=106,
                                compound='left')
        skin_out_data_2.place(x=605, y=505)

    if len(deal[4]) >= 3:
        skin_out_3 = get_n_resize(deal[4][2].weapon + ' ' + deal[4][2].name)

        if deal[4][2].prices[deal[2] + deal[3]] not in invalid_values:
            price_3 = str(round(float(deal[4][2].prices[deal[2] + deal[3]]), 2))
        else:
            price_3 = '-'

        skin_out_data_3 = tk.Label(frame, image=skin_out_3,
                                text=' ' + deal[4][2].name + '\n PRICE: ' + price_3 + '$\n Q: ' + skin_out_q,
                                font=('Montserrat Black', 16), justify='left', fg='red4', background='brown1', width=270, height=106,
                                compound='left')
        skin_out_data_3.place(x=605, y=620)

    # endregion

    # region TOTAL

    max_loss = alg.cheapest_skin(deal[4], deal[2] + deal[3])
    max_win = alg.expensive_skin(deal[4], deal[2] + deal[3])
    max_loss_f = float(max_loss.prices[deal[2] + deal[3]])
    max_win_f = float(max_win.prices[deal[2] + deal[3]])
    total = round(float(price_0) * 10, 3)

    print(max_loss.name, max_win.name)

    select_risk = tk.Text(frame, font=('Montserrat Black', 22), bd=0, fg='gray34', bg='gray80', width=15, height=3)
    select_risk.tag_configure('center', justify='center')
    select_risk.insert('1.0', 'TOTAL: ' + str(total) + '$\n'
                       + 'MAX LOSS: ' + str(round(total - max_loss_f, 2)) + '$\n'
                       + 'MAX WIN: ' + str(round(max_win_f - total, 2)) + '$')
    select_risk.tag_add('center', '1.0', 'end')
    select_risk.place(x=300, y=617)
    # endregion

    # eroare intentionata care nu lasa functia sa se incheie
    # daca s-ar incheia, variabilele locale pentru poze s-ar sterge, si implicit
    # s-ar sterge si din interfata
    a = ''
    b = float(a)

    #TODO:
    #   - fac calculele relevante pentru max loss si max win

window = tk.Tk()
window.geometry('895x750')
window.title("CS:GO Trade-up Scrapper")
window.resizable(False, False)

path_logo = 'Files/logo.png'

pixel = tk.PhotoImage(width=1, height=1)

frame = tk.Frame(bg='gray15', height=750, width=930)
frame.pack()

# log_viewer = tk.Frame(master=window, weight=354.49, height=160.93, bg='white')
# log_viewer.pack(fill=tk.Y, side=tk.RIGHT)

image = Image.open(path_logo)
logo = ImageTk.PhotoImage(image)

# este o carpeala de nedescris cu asezarea butoanelor astora
# nu te uita
logo_panel = tk.Label(frame, image=logo, bd=0)
logo_panel.place(x=305, y=13)


# region Main Buttons

btn_UpdateDB = tk.Button(frame, text="EXTRACT\nNAMES", image=pixel, bd=0, background='gray63', fg='gray15',
                         font=('Montserrat Black', 12), width=153, height=63, compound="c")
btn_UpdateDB.place(x=82, y=208)

btn_UpdatePrices = tk.Button(frame, text="EXTRACT\nPRICES", image=pixel, bd=0, background='gray63', fg='gray15',
                             font=('Montserrat Black', 12), width=153, height=63, compound="c")
btn_UpdatePrices.place(x=82, y=284)

# daca fisierul Skin_names nu exista (si deci functia de pe btn-ul update prices nu are putea functiona
# dezactivez butonul
if not path.exists('Files/Skin_names.xlsx'):
    btn_UpdatePrices['state'] = 'disabled'
    btn_UpdatePrices.unbind("<Button-1>")

btn_UpdateDB.bind("<Button-1>", extract_skins)
btn_UpdatePrices.bind("<Button-1>", extract_prices)

# endregion


# region Log Viewer Window
displayVar = tk.StringVar()
# justify = left (aliniez textul la stanga)
# anchor = 'sw' (ultimul text introdus ramane in josul paginii si oricum redimensionez Label-ul
#               el ramane jos de tot, fara a da resize la fereastra)
displayLab = tk.Label(frame, textvariable=displayVar, height=10, width=55, justify='left', anchor='sw')
displayLab.place(x=248, y=208)
#endregion


# region Select Risk Level.txt

select_risk = tk.Text(frame, font=('Montserrat Black', 25), bd=0, fg='tan2', bg='gray15', width=10, height=2)
select_risk.tag_configure('center', justify='center')
select_risk.insert('1.0', 'SELECT\nRISK LEVEL')
select_risk.tag_add('center', '1.0', 'end')
select_risk.place(x=645, y=205)

# endregion


# region Butoane Risk

btn_risk1 = tk.Button(frame, text="1", image=pixel, relief='solid', bd=0, background='gold', fg='chocolate2',
                      font=('Montserrat Black', 19), width=35, height=35, compound="c")
btn_risk1.place(x=680, y=310)
btn_risk1.bind("<Button-1>", lambda event, risk=1: search_offer(event, risk))

btn_risk2 = tk.Button(frame, text="2", image=pixel, relief='solid', bd=0, background='gold', fg='chocolate2',
                      font=('Montserrat Black', 19), width=35, height=35, compound="c")
btn_risk2.place(x=740, y=310)
btn_risk2.bind("<Button-1>", lambda event, risk=2: search_offer(event, risk))

btn_risk3 = tk.Button(frame, text="3", image=pixel, relief='solid', bd=0, background='gold', fg='chocolate2',
                      font=('Montserrat Black', 19), width=35, height=35, compound="c")
btn_risk3.place(x=800, y=310)
btn_risk3.bind("<Button-1>", lambda event, risk=3: search_offer(event, risk))

# daca fisierul cu preturile nu exista, programul nu poate cauta oferte
if not path.exists('Files/Skin_prices.xlsx'):
    btn_risk1['state'] = 'disabled'
    btn_risk1.unbind("<Button-1>")
    btn_risk2['state'] = 'disabled'
    btn_risk2.unbind("<Button-1>")
    btn_risk3['state'] = 'disabled'
    btn_risk3.unbind("<Button-1>")

# endregion


bg_trade_up = tk.Label(frame, image=pixel, background='gray80', width=930, height=360)
bg_trade_up.place(x=0, y=379)

Cases = []

window.mainloop()
