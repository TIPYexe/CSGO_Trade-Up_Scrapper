import xlsxwriter


# stat_prices = ii spun functiei daca are de salvat si preturi, sau nu
def to_xlsx(Cases, file_name, stat_prices):
    # Generez fisierul Excel
    wb = xlsxwriter.Workbook(file_name)

    # region Sheet Cases

    # Generez sheet pentru Cutii
    sheet_cases = wb.add_worksheet('Cases')

    # Adaug numele coloanelor: Case Name, Link
    sheet_cases.write(0, 0, 'Case Name')
    sheet_cases.write(0, 1, 'Link')

    # Adaug datele in coloane
    for index, case in enumerate(Cases):

        sheet_cases.write(index + 1, 0, case.name)

        if stat_prices == False:
            sheet_cases.write(index + 1, 1, case.link)
    # endregion

    # Generez sheet pentru fiecare Cutie in care salvez toate skin-urile din ea
    for case in Cases:
        # sheet_SingleCase
        sheet_scase = wb.add_worksheet(case.name.replace(':', ''))

        # adaug numele coloanelor
        sheet_scase.write(0, 0, 'Skin')
        sheet_scase.write(0, 1, 'Weapon')
        sheet_scase.write(0, 2, 'Rarity')

        if stat_prices == True:
            # Fara ST
            sheet_scase.write(0, 3, 'FN')
            sheet_scase.write(0, 4, 'MW')
            sheet_scase.write(0, 5, 'FT')
            sheet_scase.write(0, 6, 'WW')
            sheet_scase.write(0, 7, 'BS')

            # Cu ST
            sheet_scase.write(0, 8, 'SFN')
            sheet_scase.write(0, 9, 'SMW')
            sheet_scase.write(0, 10, 'SFT')
            sheet_scase.write(0, 11, 'SWW')
            sheet_scase.write(0, 12, 'SBS')

        # adaug numele si datele despre skin-uri
        for index, skin in enumerate(case.Skins):
            sheet_scase.write(index + 1, 0, skin.name)
            sheet_scase.write(index + 1, 1, skin.weapon)
            sheet_scase.write(index + 1, 2, skin.rarity)

            if stat_prices == True:
                # adaug preturile pt fiecare calitate a armei
                for i in range(0, 10):
                    if skin.prices[i] != -1:
                        sheet_scase.write(index + 1, i + 3, skin.prices[i])

    # Salvez Fisierul
    wb.close()
