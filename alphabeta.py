from igra import *
import random


#Ker ni nekega logicnega zaporedja povezanih polj, sem trojke s skupnimi krajsici
#izpisane shranila tukaj

skupna_krajisca = [(21,9,0,1,2),(0,1,2,14,23),(2,14,23,22,21),(23,22,21,9,0),
                   (18,10,3,4,5),(3,4,5,13,20),(5,13,20,19,18), (20,19,18,10,3),
                   (15,11,6,7,8),(6,7,8,12,17),(8,12,17,16,15),(17,16,15,11,6)]


class AlphaBeta:

    #vrednost
    ZMAGA = 100000
    NESKONCNO = ZMAGA + 1

    def __init__(self, globina):
        self.zacetna_globina = globina
        self.globina = globina
        self.prekinitev = False #ce je treba koncati
        self.igra = None #objekt igre
        self.jaz = None #katerega igralca igramo
        self.poteza = None #na koncu bo to nasa najboljsa poteza

    def prekini(self):
        #Gui bo poklical odpoklic
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

        (poteza, vrednost) = self.alphabeta(
                        self.globina, -AlphaBeta.NESKONCNO,AlphaBeta.NESKONCNO,  True)
        self.jaz = None
        self.igra = None
        if not self.prekinitev:
            # Potezo izvedemo v primeru, da nismo bili prekinjeni
            self.poteza = poteza



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

        #Pogledamo, ce je narejena dvojka s skupnim krajiscem
        for (i,j,k,l,m) in skupna_krajisca:
            if self.igra.plosca[i] is None and self.igra.plosca[m] is None and self.igra.plosca[j] is not None and self.igra.plosca[j] == self.igra.plosca[k] == self.igra.plosca[l]:
                if self.igra.plosca[i] == self.jaz:
                    vrednost += 2000
                elif self.igra.plosca[i] == nasprotnik(self.jaz):
                    vrednost -= 1700

        #Presteje zablokirane zetone
        for i in range(24):
            if self.igra.je_zeton_zablokiran(i):
                #moji zablokirani
                if self.igra.plosca[i] == self.jaz:
                    vrednost -= 40
                #nasprotnikovi zablokirani
                elif self.igra.plosca[i] == nasprotnik(self.jaz):
                    vrednost += 50
        return vrednost


    def alphabeta(self, globina, alpha, beta, maksimiziramo):
        if self.prekinitev:
            return (None, 0)

        #Povem mu, kdaj je prisel do konca
        if not self.igra.poteka:
            if self.igra.na_vrsti == self.jaz:
                return (None, AlphaBeta.ZMAGA)
            elif self.igra.na_vrsti == nasprotnik(self.jaz):
                return (None, -AlphaBeta.ZMAGA)

        elif self.igra.poteka: #zacne iskati poteze
            if globina == 0:
                return (None, self.vrednost_pozicije())
            else:

                #ena stopnja maksimiziranja
                if maksimiziramo:
                    vrednost_najboljse = -AlphaBeta.NESKONCNO
                    najboljsa_poteza = None
                    veljavne = self.igra.veljavne_poteze()
                    random.shuffle(veljavne)
                    
                    for p in veljavne:
                        self.igra.povleci_potezo(p)
                        if self.igra.odstranitev_zetona or self.igra.premik_zetona is not None:
                            #pri dolocenih fazah igre se igralec, ki je na potezi, ne zamenja
                            vrednost_najboljse = max(vrednost_najboljse,
                                                     self.alphabeta(globina-1, alpha, beta,
                                                                    maksimiziramo)[1])
                            alpha = max(alpha, vrednost_najboljse)
                            if beta <= alpha:
                                break

                        else:
                            vrednost_najboljse = max(vrednost_najboljse,
                                                     self.alphabeta(globina-1, alpha, beta,
                                                                    not maksimiziramo)[1])
                            alpha = max(alpha, vrednost_najboljse)
                            if beta <= alpha:
                                break
                        self.igra.razveljavi_potezo()
                        najboljsa_poteza = p



                #Minimiziramo
                else:
                    vrednost_najboljse = AlphaBeta.NESKONCNO
                    najboljsa_poteza = None
                    veljavne = self.igra.veljavne_poteze()
                    random.shuffle(veljavne)

                    for p in veljavne:
                        self.igra.povleci_potezo(p)
                        if self.igra.odstranitev_zetona or self.igra.premik_zetona is not None:
                            #pri dolocenih fazah igre se igralec, ki je na potezi, ne zamenja
                            vrednost_najboljse = min(vrednost_najboljse,
                                                     self.alphabeta(globina-1, alpha, beta,
                                                                    maksimiziramo)[1])
                            alpha = min(alpha, vrednost_najboljse)
                            if beta <= alpha:
                                break

                        else:
                            vrednost_najboljse = min(vrednost_najboljse,
                                                     self.alphabeta(globina-1, alpha, beta,
                                                                    not maksimiziramo)[1])
                            alpha = min(alpha, vrednost_najboljse)
                            if beta <= alpha:
                                break
                        self.igra.razveljavi_potezo()
                        najboljsa_poteza = p

                if najboljsa_poteza == None:
                    assert False
                return (najboljsa_poteza, vrednost_najboljse)
        else:
            assert False, "minimax: nedefinirano stanje igre"
