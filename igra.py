from tkinter import *

IGRALEC_1 = 'igralec1'
BARVA_1 = 'blue'
IGRALEC_2 = 'igralec2'
BARVA_2 = 'red'

##OSTEVILCENJE POLJ
## 1  -  -  2  -  -  3
## |  4  -  5  -  6  |
## |  -  7  8  9  -  |
##10 11 12  - 13 14 15
## |  - 16 17 18  -  |
## | 19  - 20  - 21  |
##22  -  - 23  -  - 24

class Polje():
    def __init__(self, canvas, id_krogca, stevilka_polja):#master?
        self.canvas = canvas #/plosca
        self.id_krogca = id_krogca
        self.stevilka_polja = stevilka_polja
        self.zasedenost = None


    def spremeni_zasedenost(self, igralec=None):
        #spremenimo zasedenost polja: ce na vrsti ni noben igralec, vrne None, sicer pa pripadajoco
        #barvo igralca, ki je na vrsti
        if igralec != IGRALEC_1 and igralec != IGRALEC_2:
            self.zasedenost = None
        else:
            self.zasedenost = igralec

class Igra():
    def __init__(self, seznam_polj):
        self.st_zetonov = {IGRALEC_1: 9, IGRALEC_2: 9}
        self.seznam_polj = seznam_polj
        self.na_potezi = IGRALEC_1
        self.zgodovina = []
        
