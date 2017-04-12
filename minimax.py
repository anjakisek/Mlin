import logging
from igra import *




class Minimax:
    def __init__(self, globina):
        self.globina = globina
        self.prekinitev = False #ce je treba koncati
        self.igra = None #objekt igre
        self.jaz = None #katerega igralca igramo
        self.poteza = None #na koncu bo to nasa najboljsa poteza

    def prekini(self):
        #Gui bo poklical odpoklic minimaxa
        self.prekinitev = True

    def izracunaj_potezo(self, igra):
        #potezo bo treba vracati kot indeks polja, na katerega se bo igralo

        
        #poklicali jo bomo iz vzporednega vlakna
        self.igra = igra
        self.prekinitev = False
        self.jaz = self.igra.na_vrsti
        self.poteza = None # tu bomo zapisali najboljso potezo
        
        (poteza, vrednost) = self.minimax(self.globina, True)
        self.jaz = None
        self.igra = None
        if not self.prekinitev:
            # Potezo izvedemo v primeru, da nismo bili prekinjeni
            logging.debug("minimax: poteza {0}, vrednost {1}".format(poteza, vrednost))
            self.poteza = poteza

    #vrednost
    ZMAGA = 10000
    NESKONCNO = ZMAGA + 1
    
    def vrednost_pozicije(self):
        #Zaenkrat se zelo slaba cenilka
        #Iz nekega razloga je ta slovar vcasih prazen ???
        print(self.igra.slovar_polj)
        vrednost = 0
        for trojka in trojke:
            seznam_zasedenosti = [
                self.igra.slovar_polj[x].zasedenost for x in trojka]
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
        vrednost += self.igra.st_zetonov[self.jaz] * 40
        vrednost -= self.igra.st_zetonov[nasprotnik(self.jaz)] * 35
        print('Vrednost je: ', vrednost)
        return vrednost
                
               

    def minimax(self, globina, maksimiziramo):
        if self.prekinitev:
            print('Prekinjajo me')
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
                    print('Veljavne poteze:', self.igra.veljavne_poteze(),
                          self.igra.zgodovina[-1])
                    for p in self.igra.veljavne_poteze():
                        #self.igra.povleci_potezo(p)
                        self.igra.gui.naredi_potezo(p, False)
                        if self.igra.odstranitev_zetona or self.igra.premik_zetona is not None:
                            vrednost = self.minimax(globina-1, maksimiziramo)[1]
                        else:
                            vrednost = self.minimax(globina-1, not maksimiziramo)[1]
                        self.igra.razveljavi()
                        if vrednost > vrednost_najboljse:
                            vrednost_najboljse = vrednost
                            najboljsa_poteza = p
                            print('Vrednost najboljse: ', vrednost_najboljse)
                else:
                    najboljsa_poteza = None
                    vrednost_najboljse = Minimax.NESKONCNO
                    print('Veljavne poteze:', self.igra.veljavne_poteze())
                    for p in self.igra.veljavne_poteze():
                        #self.igra.povleci_potezo(p)
                        self.igra.gui.naredi_potezo(p, False)
                        if self.igra.odstranitev_zetona or self.igra.premik_zetona is not None:
                            vrednost = self.minimax(globina-1, maksimiziramo)[1]
                        else:
                            vrednost = self.minimax(globina-1, not maksimiziramo)[1]
                        self.igra.razveljavi()
                        if vrednost < vrednost_najboljse:
                            vrednost_najboljse = vrednost
                            najboljsa_poteza = p
                            
                assert (najboljsa_poteza is not None), "minimax: izracunana poteza je None"
                return (najboljsa_poteza, vrednost_najboljse)
        else:
            assert False, "minimax: nedefinirano stanje igre"
                            
        


















    
