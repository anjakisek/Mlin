from igra import *
import random
import logging

##OSTEVILCENJE POLJ
## 0  -  -  1  -  -  2
## |  3  -  4  -  5  |
## |  -  6  7  8  -  |
## 9 10 11  - 12 13 14
## |  - 15 16 17  -  |
## | 18  - 19  - 20  |
##21  -  - 22  -  - 23

#Ker ni nekega logicnega zaporedja povezanih polj, sem povezane trojke in posebaj trojke s skupnimi krajsici
#izpisala tukaj
trojke = [(0,1,2), (3,4,5), (6,7,8), (9,10,11),
          (12,13,14), (15,16,17),(18,19,20),(21,22,23),
          (0,9,21),(3,10,18),(6,11,15),(1,4,7),
          (16,19,22),(8,12,17),(5,13,20),(2,14,23)]

#Ker ni nekega logicnega zaporedja povezanih polj, sem povezane trojke in posebaj trojke s skupnimi krajsici
#izpisane shranila tukaj
povezane_trojke = [(2, 1, 0, 9, 21),(0, 2, 1, 4, 7),(0, 1, 2, 14, 23),
                   (3, 4, 5, 10, 18),(3, 4, 5, 1, 7),(3, 4, 5, 13, 20),
                   (6, 7, 8, 11, 15),(6, 7, 8, 1, 4),(6, 7, 8, 12, 17),
                   (9, 10, 11, 0, 21),(9, 10, 11, 3, 18),(9, 10, 6, 11, 15),
                   (12, 13, 14, 8, 17),(12, 14, 5, 13, 20),(12, 13, 14, 2, 23),
                   (15, 16, 17, 6, 11),(15, 17, 16, 19, 22),(15, 16, 8, 12, 17),
                   (18, 19, 20, 3, 10),(18, 19, 20, 16, 22),(18, 19, 20, 5, 13),
                   (21, 22, 23, 0, 9),(21, 22, 23, 16, 19),(21, 22, 23, 2, 14)]

skupna_krajisca = [(21,9,0,1,2),(0,1,2,14,23),(2,14,23,22,21),(23,22,21,9,0),
                   (18,10,3,4,5),(3,4,5,13,20),(5,13,20,19,18), (20,19,18,10,3),
                   (15,11,6,7,8),(6,7,8,12,17),(8,12,17,16,15),(17,16,15,11,6)]

class Minimax:
    def __init__(self, globina):
        self.zacetna_globina = globina
        self.globina = globina
        self.prekinitev = False #ce je treba koncati
        self.igra = None #objekt igre
        self.jaz = None #katerega igralca igramo
        self.poteza = None #na koncu bo to nasa najboljsa poteza

    def prekini(self):
        #Gui bo poklical odpoklic minimaxa
        self.prekinitev = True

    def izracunaj_potezo(self, igra):
        '''Poisce najboljso potezo in jo vrne kot indeks polja, na katerega
    se bo igralo.'''

        #poklicali jo bomo iz vzporednega vlakna
        self.igra = igra
        self.prekinitev = False
        self.jaz = self.igra.na_vrsti
        self.poteza = None # tu bomo zapisali najboljso potezo

        #Po dolecenem stevilu potez se globina poveca.
        st_veljavnih_potez = len(self.igra.veljavne_poteze())
        if st_veljavnih_potez < 8:
            self.globina = self.zacetna_globina + 2
        elif st_veljavnih_potez < 15:
            self.globina = self.zacetna_globina + 1
        else:
            self.globina = self.zacetna_globina

        (poteza, vrednost) = self.minimax(self.globina, True)
        self.jaz = None
        self.igra = None
        if not self.prekinitev:
            # Potezo izvedemo v primeru, da nismo bili prekinjeni
            self.poteza = poteza

    #vrednost
    ZMAGA = 100000
    NESKONCNO = ZMAGA + 1

    def vrednost_pozicije(self):
        '''Oceni vrednost trenutne pozicije.'''
        vrednost = 0
        #Trojke so nam vsec, skoraj trojke tudi
        for trojka in trojke:
            seznam_zasedenosti = [
                self.igra.plosca[x] for x in trojka]
            if seznam_zasedenosti.count(self.jaz) == 3:
                vrednost += 240
            elif seznam_zasedenosti.count(self.jaz) == 2 and (
                seznam_zasedenosti.count(None) == 1):
                vrednost += 200

            #Bolj nam je vazno postaviti svojo trojko, kot blokirati nasprotnikovo
            elif seznam_zasedenosti.count(nasprotnik(self.jaz)) == 3:
                vrednost -= 210
            elif seznam_zasedenosti.count(nasprotnik(self.jaz)) == 2 and (
                seznam_zasedenosti.count(None) == 1):
                vrednost -= 170

        #Polja v srednjem kvadratu so stratesko boljsa:
        for i in (4,10,13,19):
            if self.igra.plosca[i] == self.jaz:
                vrednost += 5
            elif self.igra.plosca[i] == nasprotnik(self.jaz):
                vrednost -= 5

        #Zelimo, da se igra cimprej konca:
        vrednost += 200 - 2 * self.igra.st_potez

        #Dobro je imeti cimvec svojih zetonov in cim manj nasprotnikovih:
        vrednost += self.igra.st_zetonov[self.jaz] * 400
        vrednost -= self.igra.st_zetonov[nasprotnik(self.jaz)] * 380

        #pogledamo, ce je narejena dvojka s skupnim krajiscem
        for (i,j,k,l,m) in skupna_krajisca:
            if self.igra.plosca[i] is None and self.igra.plosca[m] is None and self.igra.plosca[j] is not None and self.igra.plosca[j] == self.igra.plosca[k] == self.igra.plosca[l]:
                if self.igra.plosca[i] == self.jaz:
                    vrednost += 2000
                #nasprotnikovi zablokirani
                elif self.igra.plosca[i] == nasprotnik(self.jaz):
                    vrednost -= 1700

        #presteje zablokirane zetone
        for i in range(24):
            if self.igra.je_zeton_zablokiran(i):
                #moji zablokirani
                if self.igra.plosca[i] == self.jaz:
                    vrednost -= 40
                #nasprotnikovi zablokirani
                elif self.igra.plosca[i] == nasprotnik(self.jaz):
                    vrednost += 50
        return vrednost


    def poskusna_cenilka(self):
        vrednost = 0
        #razlika med stevilom tvojih in njegovih strojk
        vrednost += 800 * (self.igra.st_zetonov[self.jaz] - self.igra.st_zetonov[nasprotnik(self.jaz)])

        #presteje zablokirane zetone
        for i in range(24):
            if self.igra.je_zeton_zablokiran(i):
                #moji zablokirani
                if self.igra.plosca[i] == self.jaz:
                    vrednost -= 40
                #nasprotnikovi zablokirani
                elif self.igra.plosca[i] == nasprotnik(self.jaz):
                    vrednost += 50

        #gremo po vseh poljih, prestejemo trojke in dvojke ( [zasedeno, zasedeno, None] ).
        moje_trojke = 0
        njegove_trojke = 0
        moje_dvojke = 0
        njegove_dvojke = 0
        for polje in range(24):
            for (i,j,k) in [t for t in trojke if polje in t]:
                if (self.igra.plosca[i] != None and self.igra.plosca[i] == self.igra.plosca[j] == self.igra.plosca[k]):
                    if self.igra.plosca[i] == self.jaz:
                        #morebitno trojko bi steli trikrat
                        moje_trojke += 1/3
                    elif self.igra.plosca[i] == nasprotnik(self.jaz):
                        #morebitno trojko bi steli trikrat
                        njegove_trojke += 1/3
                elif ((self.igra.plosca[i] == self.igra.plosca[j] and self.igra.plosca[k] is None) or (self.igra.plosca[k] == self.igra.plosca[j] and self.igra.plosca[j] is None)):
                    if self.igra.plosca[i] == self.jaz:
                        #morebitno trojko bi steli trikrat
                        moje_dvojke += 1/3
                    elif self.igra.plosca[i] == nasprotnik(self.jaz):
                        #morebitno trojko bi steli trikrat
                        njegove_dvojke += 1/3
        vrednost += 200 * (moje_trojke - njegove_trojke) + 100 * (moje_dvojke - njegove_dvojke)

        #pogledamo dvojne trojke
        for polje in range(24):
            for (i,j,k,l,m) in [t for t in povezane_trojke if polje in t]:
                if (self.igra.plosca[i] != None and self.igra.plosca[i] == self.igra.plosca[j] == self.igra.plosca[k] == self.igra.plosca[l] == self.igra.plosca[m]):
                    if self.igra.plosca[i] == self.jaz:
                        vrednost += 200
                    elif self.igra.plosca[i] == nasprotnik(self.jaz):
                        vrednost -= 170

        #pogledamo, ce je narejena dvojka s skupnim krajiscem
        for (i,j,k,l,m) in skupna_krajisca:
            if self.igra.plosca[i] is None and self.igra.plosca[m] is None and self.igra.plosca[j] is not None and self.igra.plosca[j] == self.igra.plosca[k] == self.igra.plosca[l]:
                if self.igra.plosca[i] == self.jaz:
                    vrednost += 2000
                elif self.igra.plosca[i] == nasprotnik(self.jaz):
                    vrednost -= 1700

        
        #Polja v srednjem kvadratu so stratesko boljsa:
        for i in (4,10,13,19):
            if self.igra.plosca[i] == self.jaz:
                vrednost += 10
            elif self.igra.plosca[i] == nasprotnik(self.jaz):
                vrednost -= 10

        #Zelimo, da se igra cimprej konca:
        vrednost += 200 - 2 * self.igra.st_potez

        return vrednost

                

        


    def minimax(self, globina, maksimiziramo):
        '''Preveri poteze do dolocene globine, vrne najbolje ocenjeno potezo in njeno vrednost.'''
        if self.prekinitev:
            return (None, 0)

        #Povem mu, kdaj je prisel do konca
        if not self.igra.poteka:
            if self.igra.na_vrsti == self.jaz:
                return (None, Minimax.ZMAGA)
            elif self.igra.na_vrsti == nasprotnik(self.jaz):
                return (None, -Minimax.ZMAGA)

        elif self.igra.poteka: #zacne iskati poteze
            if globina == 0:
                return (None, self.vrednost_pozicije())
            else:

                #ena stopnja minimaxa
                if maksimiziramo:
                    najboljsa_poteza = None
                    vrednost_najboljse = -Minimax.NESKONCNO 
                    veljavne = self.igra.veljavne_poteze()
                    random.shuffle(veljavne)
                    for p in veljavne:
                        self.igra.povleci_potezo(p)
                        if self.igra.ali_odstranjujemo_zeton or self.igra.premik_zetona is not None:
                            #pri dolocenih fazah igre se igralec, ki je na potezi, ne zamenja
                            vrednost = self.minimax(globina-1, maksimiziramo)[1]
                        else:
                            vrednost = self.minimax(globina-1, not maksimiziramo)[1]
                        self.igra.razveljavi_potezo()
                        if vrednost > vrednost_najboljse:
                            vrednost_najboljse = vrednost
                            najboljsa_poteza = p


                #Minimiziramo
                else:
                    najboljsa_poteza = None
                    vrednost_najboljse = Minimax.NESKONCNO
                    veljavne = self.igra.veljavne_poteze()
                    random.shuffle(veljavne)

                    
                    for p in veljavne:
                        self.igra.povleci_potezo(p)
                        if self.igra.ali_odstranjujemo_zeton or self.igra.premik_zetona is not None:
                            #pri dolocenih fazah igre se igralec, ki je na potezi, ne zamenja
                            vrednost = self.minimax(globina-1, maksimiziramo)[1]
                        else:
                            vrednost = self.minimax(globina-1, not maksimiziramo)[1]
                        self.igra.razveljavi_potezo()
                        if vrednost < vrednost_najboljse:
                            vrednost_najboljse = vrednost
                            najboljsa_poteza = p

                if najboljsa_poteza == None:
                    logging.debug("alphabeta nima poteze v poziciji: {}".format(self.igra.plosca))
                    assert False
                return (najboljsa_poteza, vrednost_najboljse)
        else:
            assert False, "minimax: nedefinirano stanje igre"
