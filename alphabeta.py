from igra import *
import random


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
        #potezo bo treba vracati kot indeks polja, na katerega se bo igralo

        
        #poklicali jo bomo iz vzporednega vlakna
        self.igra = igra
        self.prekinitev = False
        self.jaz = self.igra.na_vrsti
        self.poteza = None # tu bomo zapisali najboljso potezo

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
        #Zaenkrat se zelo slaba cenilka
        #Iz nekega razloga je ta slovar vcasih prazen ???
        vrednost = 0
        for trojka in trojke:
            seznam_zasedenosti = [
                self.igra.plosca[x] for x in trojka]
            if seznam_zasedenosti.count(self.jaz) == 3:
                vrednost += 240
            elif seznam_zasedenosti.count(self.jaz) == 2 and (
                seznam_zasedenosti.count(None) == 1):
                vrednost += 200
            elif seznam_zasedenosti.count(nasprotnik(self.jaz)) == 3:
                vrednost -= 210
            elif seznam_zasedenosti.count(nasprotnik(self.jaz)) == 2 and (
                seznam_zasedenosti.count(None) == 1):
                vrednost -= 170
        for i in (3,4,5,10,13,18,19,20):
            if self.igra.plosca[i] == self.jaz:
                vrednost += 5
            elif self.igra.plosca[i] == nasprotnik(self.jaz):
                vrednost -= 5
        vrednost += 200 - 2 * self.igra.st_potez
        vrednost += self.igra.st_zetonov[self.jaz] * 400
        vrednost -= self.igra.st_zetonov[nasprotnik(self.jaz)] * 400
        return vrednost
                
               

    def alphabeta(self, globina, alpha, beta, maksimiziramo):
        if self.prekinitev:
            print('Prekinjajo me')
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

                #ena stopnja 
                if maksimiziramo:
                    vrednost_najboljse = -AlphaBeta.NESKONCNO
                    najboljsa_poteza = None
                    veljavne = self.igra.veljavne_poteze()
                    random.shuffle(veljavne)
                    for p in veljavne:
                        self.igra.povleci_potezo(p)
                        if self.igra.odstranitev_zetona or self.igra.premik_zetona is not None:
                            #globina-1?
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
                            #globina-1?
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


                            
                #assert (najboljsa_poteza is not None), "minimax: izracunana poteza je None"
                return (najboljsa_poteza, vrednost_najboljse)
        else:
            assert False, "minimax: nedefinirano stanje igre"
