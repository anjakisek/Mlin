import logging
from igra import IGRALEC_1, IGRALEC_2, nasprotnik, trojke

#vrednost



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





    def minimax():
        pass
