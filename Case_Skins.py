# cele cu S in fata au StatTrak (valoreaza mai mult)
# pentru fiecare calitate stim pretul
class Skin:
    def __init__(self):
        self.name = ""
        self.weapon = ""
        self.prices = []
        self.rarity = ""
        self.cheapest_skin = []


# fiecare cutie cu skin-uri + link-ul cu date despre skin-urile din ea
class Case:
    def __init__(self):
        self.name = ""
        self.link = ""
        self.Skins = []
        self.byRarity = []
