import threading
from igra import *
from minimax import *
import time

class Racunalnik():
    def __init__(self, gui, algoritem):
        self.gui = gui
        self.algoritem = algoritem
        self.mislec = None #vlakno za razmisljanje

    def igraj(self):
        '''V vzporednem vlaknu sprozi razmislanje o novi potezi'''
        #sprozimo razmisljanje
        self.mislec = threading.Thread(
            target=lambda: self.algoritem.izracunaj_potezo(
                self.gui.igra.kopija()))

        #pozenemo vlakno
        self.mislec.start()
        self.zacni_meriti_cas =time.time()

        #preverjamo na vsake 100ms, ali je mislec ze razmislil
        self.gui.plosca.after(100, self.preveri_potezo)

    def preveri_potezo(self):
        '''Po dolocenem casu preveri, ali je vlakno ze naslo optimalno potezo in
    potezo naredi s primernim zamikom.'''

        #vsake 100ms preveri, ce je mislec ze koncal
        if self.algoritem.poteza is not None:

            self.pretekli_cas = time.time() - self.zacni_meriti_cas
            if self.pretekli_cas < 1/2:
                time.sleep(2/3)
            # XXX potezo naredimo samo, če nismo bili prekinjeni
            self.gui.naredi_potezo(self.algoritem.poteza)
        else:
            self.gui.plosca.after(100, self.preveri_potezo)

    def prekini(self):
        if self.mislec:
            # Algoritmu sporocimo, naj neha
            self.algoritem.prekini()
            #Pocakamo, da se mislec ustavi
            self.mislec.join()
            self.mislec = None


    def klik(self, p):
        pass
