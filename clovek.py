import logging

class Clovek():
    def __init__(self, gui):
        self.gui = gui

    def igraj(self):
        pass

    def prekini(self):
        pass

    def klik(self, p):
        logging.debug("Clovek dela potezo {}".format(p))
        self.gui.naredi_potezo(p)
