import logging
##from igra import IGRALEC_1, IGRALEC_2, nasprotnik, trojke
from igra import *

#vrednost
ZMAGA = 10000
NESKONCNO = ZMAGA + 1


class Minimax:
    def __init__(self, globina):
        self.globina = globina
        self.prekinitev = False #ce je treba koncati
        self.igra = None #objekt igre
        self.na_potezi = None #cigavo potezo izbiramo
        self.poteza = None #na koncu bo to nasa najboljsa poteza

    def prekini(self):
        #Gui bo poklical odpoklic minimaxa
        self.prekinitev = True

    def izracunaj_potezo(self, igra):
        #potezo bo treba vracati kot indeks polja, na katerega se bo igralo

        
        #poklicali jo bomo iz vzporednega vlakna
        self.igra = igra
        self.prekinitev = False
        self.na_potezi = self.igra.na_vrsti
        self.poteza = None # tu bomo zapisali najboljso potezo
        
        (poteza, vrednost) = self.minimax(self.globina, True)
        self.na_potezi = None
        self.igra = None
        if not self.prekinitev:
            # Potezo izvedemo v primeru, da nismo bili prekinjeni
            logging.debug("minimax: poteza {0}, vrednost {1}".format(poteza, vrednost))
            self.poteza = poteza

    def vrednost_pozicije(self):
        #Predlagam, da za cenilko: ne glede na fazo vec zetonov
        #prinese vec pik. Potem prestejeva trojke. Morda se kaj
        vrednost = 0
        for trojka in trojke:
            seznam_zasedenosti = [
                self.igra.slovar_polj[x].zasedenost for x in trojka]
            if seznam_zasedenosti.count(self.na_potezi) == 3:
                vrednost += 240
            elif seznam_zasedenosti.count(self.na_potezi) == 2 and (
                seznam_zasedenosti.count(None) == 1):
                vrednost += 200
            elif seznam_zasedenosti.count(nasprotnik(self.na_potezi)) == 3:
                vrednost -= 210
            elif seznam_zasedenosti.count(nasprotnik(self.na_potezi)) == 2 and (
                seznam_zasedenosti.count(None) == 1):
                vrednost -= 170
            #Dodatne vredne pozicije: ...
        return vrednost
                
               



    def minimax():
        pass
