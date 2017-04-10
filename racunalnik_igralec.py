import threading
from igra import *
from minimax import *

class Racunalnik():
    def __init__(self, gui, algoritem):
        self.gui = gui
        self.algoritem = algoritem
        self.mislec = None #vlakno za razmisljanje

    def igraj(self):
        #sprozimo razmisljanje
        print(self.gui.igra)
        print(self.gui.igra.kopija())
        self.mislec = threading.Thread(
            target=lambda: self.algoritem.izracunaj_potezo(self.gui.igra.kopija()))

        #pozenemo vlakno
        self.mislec.start()

        #preverjamo na vsake 100ms, ali je mislec ze razmislil
        self.gui.plosca.after(100, self.preveri_potezo)

    def preveri_potezo(self):
        #vsake 100ms preveri, ce je mislec ze koncal
        if self.algoritem.poteza is not None:
            self.gui.naredi_potezo(self.algoritem.poteza)
            self.mislec = None
        else:
            self.gui.plosca.after(100, self.preveri_potezo)

    def prekini(self):
        if self.mislec:
            logging.debug ("Prekinjamo {0}".format(self.mislec))
            # Algoritmu sporocimo, naj neha
            self.algoritem.prekini()
            #Pocakamo, da se mislec ustavi
            self.mislec.join()
            self.mislec = None
    

    def klik(self, p):
        pass
    
