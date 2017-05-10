import threading
from igra import *
from minimax import *
import time

class Racunalnik():
    def __init__(self, gui, algoritem):
        self.gui = gui
        self.algoritem = algoritem #izbran algoritem, minimax ali alphabeta
        self.mislec = None #vlakno za razmisljanje
        self.je_treba_prekiniti = False

    def igraj(self):
        '''V vzporednem vlaknu sprozi razmislanje o novi potezi'''
        #Sprozimo razmisljanje
        self.mislec = threading.Thread(
            target=lambda: self.algoritem.izracunaj_potezo(
                self.gui.igra.kopija()))

        #Pozenemo vlakno
        self.mislec.start()
        self.zacni_meriti_cas =time.time()

        #Preverjamo na vsake 100ms, ali je mislec ze razmislil
        self.gui.plosca.after(100, self.preveri_potezo)

    def preveri_potezo(self):
        '''Po dolocenem casu preveri, ali je vlakno ze naslo optimalno potezo in
    potezo naredi s primernim zamikom.'''

        #Vsake 100ms preveri, ce je mislec ze koncal
        if self.algoritem.poteza is not None:

            self.pretekli_cas = time.time() - self.zacni_meriti_cas
            if self.pretekli_cas < 1/2:
                #Poskrbi, da racunalnik poteze ne potegne prehitro, saj je
                #takim potezam na plosci tezko slediti
                time.sleep(2/3)
            #Ce smo tacas prekinili igro, poteze ne naredimo
            if not self.je_treba_prekiniti:
                self.gui.naredi_potezo(self.algoritem.poteza)
        else:
            #Ce poteze se ni izracunal, cez cas preveri, ce je ze nared
            self.gui.plosca.after(100, self.preveri_potezo)

    def prekini(self):
        self.je_treba_prekiniti = True
        if self.mislec:
            # Algoritmu sporocimo, naj neha
            self.algoritem.prekini()
            #Pocakamo, da se mislec ustavi
            self.mislec.join()
            self.mislec = None


    def klik(self, p):
        pass
