from tkinter import *
from igra import *
from racunalnik_igralec import *
from clovek import *
from minimax import *
from alphabeta import *
import logging

# Odkomentiraj za debug:
logging.basicConfig(level=logging.DEBUG)

#Dolocimo velikost plosce in polja ter globino
VELIKOST_PLOSCE = 400
VELIKOST_POLJA = VELIKOST_PLOSCE/25
GLOBINA = 2

##OSTEVILCENJE POLJ
## 0  -  -  1  -  -  2
## |  3  -  4  -  5  |
## |  -  6  7  8  -  |
## 9 10 11  - 12 13 14
## |  - 15 16 17  -  |
## | 18  - 19  - 20  |
##21  -  - 22  -  - 23

def sredisce(krogec):
    (x1, y1, x2, y2) = krogec
    return ((x1 + x2) / 2, (y1 + y2) /2)



##############################################################
##############################################################
################### UPORABNISKI VMESNIK ######################
##############################################################
##############################################################

class Gui():

    def __init__(self, master):
        
        #Kasneje nastavi igralce glede na uporabnikovo izbiro
        self.igralec_1 = None
        self.igralec_2 = None


        #Ce uporabnik zapre okno
        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))


        self.igra = None # Igre še nismo začeli igrati

        #Privzeti algoritem je minimax
        self.algoritem = Minimax(GLOBINA)

        #Glavni menu
        menu = Menu(master)
        master.config(menu=menu)

        #Podmenu: Igra
        #Uporabnik lahko izbere, kaksni tipi igralcev bodo igro igrali
        menu_igra = Menu(menu)
        menu.add_cascade(label="Igra", menu=menu_igra)
        menu_igra.add_command(label="Clovek vs. Clovek",
                              command=lambda: self.zacni_igro(
                                  Clovek(self),
                                Clovek(self)))
        menu_igra.add_command(label="Clovek vs. Racunalnik",
                              command=lambda: self.zacni_igro(
                                  Clovek(self),
                                        Racunalnik(self, self.algoritem)))
        menu_igra.add_command(label="Racunalnik vs. Clovek",
                              command=lambda: self.zacni_igro(
                                  Racunalnik(self, self.algoritem),
                                                Clovek(self)))
        menu_igra.add_command(label="Racunalnik vs. Racunalnik",
                              command=lambda: self.zacni_igro(
                                  Racunalnik(self, self.algoritem),
                                        Racunalnik(self, self.algoritem)))
        #Podmenu: Tezavnost
        #Tezavnost se nastavlja z izbiro algoritma, lazji je minimax, tezji
        #pa minimax z alpha beta rezi in povecano globino
        menu_tezavnost = Menu(menu)
        menu.add_cascade(label="Tezavnost", menu=menu_tezavnost)
        menu_tezavnost.add_radiobutton(label="Zacetnik",
                                  variable=self.algoritem,
                                       value=(Minimax(GLOBINA)))
        menu_tezavnost.add_radiobutton(label="Mojster",
                                  variable=self.algoritem,
                                   value=(AlphaBeta(GLOBINA+4)))

        #Podmenu: Moznosti
        #Uporabnik lahko razveljavi potezo
        menu_moznosti = Menu(menu)
        menu.add_cascade(label="Moznosti", menu=menu_moznosti)
        menu_moznosti.add_command(label="Razveljavi",
                                  command=self.razveljavi)



        #Napis nad igralno plosco
        self.sporocilo = StringVar(
            master,
            value='Dobrodošli! Izberite tipe igralcev, da pričnete z igro.')
        self.sporocevalec = Label(
            master,
            textvariable = self.sporocilo)
        self.sporocevalec.grid(row=0, columnspan = 2, sticky=E+W)

        #Stevec, ki bo prikazoval, koliko zetonov lahko
        # prvi igralec se polozi na plosco
        self.napis1 = Label(
            master,
            text= "")
        self.napis1.grid(row=2, column=0)

        #Stevec, ki bo prikazoval, koliko zetonov lahko
        # drugi igralec se polozi na plosco
        self.napis2 = Label(
            master,
            text= "")
        self.napis2.grid(row=2, column=1)


        #Seznam krogcev hrani id naslove krogcev na canvasu. Urejeni bodo v
        #enakem vrstnem redu, kot so ostevilcena pripadajoca polja na plosci
        self.seznam_krogcev = []


        #Igralna plosca
        self.plosca = Canvas(
            master, width = VELIKOST_PLOSCE, height = VELIKOST_PLOSCE,
            bg = 'white')
        self.plosca.grid(row=1, column=0, columnspan=2)



        ##############################################
        ##############################################
        #Povezem polja med seboj
        for i in range(0, 3):
            self.plosca.create_rectangle(VELIKOST_PLOSCE * (1/8 + i/8),
                                         VELIKOST_PLOSCE * (1/8 + i/8),
                                         VELIKOST_PLOSCE * (7/8 - i/8) ,
                                         VELIKOST_PLOSCE * (7/8 - i/8))

        self.plosca.create_line(VELIKOST_PLOSCE/2, VELIKOST_PLOSCE/8,VELIKOST_PLOSCE/2,
                                3 * VELIKOST_PLOSCE/8)
        self.plosca.create_line(VELIKOST_PLOSCE/2, 5 * VELIKOST_PLOSCE/8,VELIKOST_PLOSCE/2,
                                7 * VELIKOST_PLOSCE/8)
        self.plosca.create_line(VELIKOST_PLOSCE/8, VELIKOST_PLOSCE/2,3 * VELIKOST_PLOSCE/8,
                                VELIKOST_PLOSCE/2)
        self.plosca.create_line(5 * VELIKOST_PLOSCE/8, VELIKOST_PLOSCE/2,7 * VELIKOST_PLOSCE/8,
                                VELIKOST_PLOSCE/2)

        #Ustvarim 24 pik/polj in njihove id shranim v seznam krogcev v pravilnem
        # vrstnem redu
        for k in range(0, 2): #krogci 10-15
            for i in range(0, 3):
                id_krogca = self.plosca.create_oval(VELIKOST_PLOSCE * (1/8 + i/8 + k/2) - VELIKOST_POLJA,
                                          VELIKOST_PLOSCE/2 - VELIKOST_POLJA,
                                          VELIKOST_PLOSCE * (1/8 + i/8 + k/2) + VELIKOST_POLJA,
                                          VELIKOST_PLOSCE/2 + VELIKOST_POLJA,
                                                    fill = 'white')
                self.seznam_krogcev.append(id_krogca)

        for k in range(0, 2):#krogci 7-9, 16-18
            seznam=[]
            for i in range(0, 3):
                id_krogca = self.plosca.create_oval(VELIKOST_PLOSCE * (3/8 + i/8) - VELIKOST_POLJA,
                                        VELIKOST_PLOSCE * (3/8 + k/4) - VELIKOST_POLJA,
                                        VELIKOST_PLOSCE * (3/8 + i/8) + VELIKOST_POLJA,
                                        VELIKOST_PLOSCE * (3/8 + k/4) + VELIKOST_POLJA,
                                                    fill = 'white')
                seznam.append(id_krogca)
            if k == 0:
                self.seznam_krogcev = seznam + self.seznam_krogcev
            else:
                self.seznam_krogcev = self.seznam_krogcev + seznam

        for k in range(0, 2):#krogci 4-6, 19-21
            seznam = []
            for i in range(0, 3):
                id_krogca = self.plosca.create_oval(VELIKOST_PLOSCE * (1/4 + i/4) - VELIKOST_POLJA,
                                        VELIKOST_PLOSCE * (1/4 + k/2) - VELIKOST_POLJA,
                                        VELIKOST_PLOSCE * (1/4 + i/4) + VELIKOST_POLJA,
                                        VELIKOST_PLOSCE * (1/4 + k/2) + VELIKOST_POLJA,
                                                    fill = 'white')
                seznam.append(id_krogca)
            if k == 0:
                self.seznam_krogcev = seznam + self.seznam_krogcev
            else:
                self.seznam_krogcev = self.seznam_krogcev + seznam

        for k in range(0, 2):#krogci 1-3, 22-24
            seznam = []
            for i in range(0, 3):
                id_krogca = self.plosca.create_oval(
                    VELIKOST_PLOSCE * (1/8 + i * 3/8) - VELIKOST_POLJA,
                    VELIKOST_PLOSCE * (1/8 + k * 3/4) - VELIKOST_POLJA,
                    VELIKOST_PLOSCE *(1/8 + i * 3/8) + VELIKOST_POLJA,
                    VELIKOST_PLOSCE * (1/8 + k * 3/4) + VELIKOST_POLJA,
                    fill = 'white')
                seznam.append(id_krogca)
            if k == 0:
                self.seznam_krogcev = seznam + self.seznam_krogcev
            else:
                self.seznam_krogcev = self.seznam_krogcev + seznam

        #################################
        #################################


        #Ob kliku na plosco poklice funkcijo, primerno trenutni fazi igre
        self.plosca.bind("<Button-1>", self.klik)





    def zacni_igro(self, igralec1, igralec2):
        '''Pripravi novo igro, nastavi tipe igralcev in pozene prvega igralca v tek'''
        self.prekini_igralce()
        self.igralec_1 = igralec1
        self.igralec_2 = igralec2
        self.pripravi_novo_igro()
        self.sporocilo.set('Na vrsti je {} - postavite žeton'.format(self.igra.na_vrsti))
        self.igralec_1.igraj()


    def klik(self, event):
        '''Ob kliku ugotovi, kam smo kliknili, in poklice odziv na klik glede na trenutnega igralca'''
        if (self.igra is None) or (not self.igra.poteka):
            pass
        else:
            (a,b) = (event.x, event.y)
            for i in range(len(self.seznam_krogcev)):
                id_krogca = self.seznam_krogcev[i]
                x, y = sredisce(self.plosca.coords(id_krogca))
                razdalja = ((a-x)**2 + (b-y)**2)**0.5
                #Ce smo kliknili znotraj krogca, bomo naredili ustrezno potezo.
                if razdalja <= VELIKOST_POLJA:
                    index_polja = i

                    if self.igra.na_vrsti == IGRALEC_1:
                        self.igralec_1.klik(index_polja)
                    elif self.igra.na_vrsti == IGRALEC_2:
                        self.igralec_2.klik(index_polja)


    def naredi_potezo(self, index_polja):
        '''Naroci igri, da potezo izvede, nato izrise trenutno plosco in pozene igro naprej'''
        if self.igra.povleci_potezo(index_polja):
            self.osvezi_plosco()

            #pozene naslednjega igralca v igro
            if self.igra.na_vrsti == IGRALEC_1:
                self.igralec_1.igraj()
            elif self.igra.na_vrsti == IGRALEC_2:
                self.igralec_2.igraj()
            else:
                pass
        #Ce poteza ni bila veljavna in ni naredil nic, samo ponastavi napis nad plosco
        else:
            if self.igra.stevec1 == 0 and self.igra.stevec2 == 0:
                self.sporocilo.set('Na vrsti je {} - izberite žeton za premik'
                                   .format(self.igra.na_vrsti))



    def osvezi_plosco(self):
        '''Prebarva polja in osvezi napise nad plosco'''
        self.napis1.config(text = "Preostali {}: "
                           .format(IGRALEC_1)+ str(self.igra.stevec1))
        self.napis2.config(text = "Preostali {}: "
                           .format(IGRALEC_2)+ str(self.igra.stevec2))

        #Barvanje polj
        for polje in range(0, 24):
            if self.igra.plosca[polje] == IGRALEC_1:
                barva = BARVA_1
            elif self.igra.plosca[polje] == IGRALEC_2:
                barva = BARVA_2
            else:
                barva = 'white'
            self.plosca.itemconfigure(self.seznam_krogcev[polje], fill=barva, width = 1)

        #Spremeni napis glede na fazo igre
        if not self.igra.poteka:
                self.sporocilo.set(
                    'Igre je konec, zmagal je {}'.format(
                     self.igra.na_vrsti))
        elif self.igra.ali_odstranjujemo_zeton:
                self.sporocilo.set('Na vrsti je {} - odstranite žeton'
                                   .format(self.igra.na_vrsti))
        elif self.igra.stevec1 > 0 or self.igra.stevec2 > 0:
                self.sporocilo.set('Na vrsti je {} - postavite žeton'
                                   .format(self.igra.na_vrsti))
        elif self.igra.stevec1 == 0 and self.igra.stevec2 == 0 and self.igra.premik_zetona is None:
                self.sporocilo.set('Na vrsti je {} - izberite žeton za premik'
                                   .format(self.igra.na_vrsti))
        elif self.igra.stevec1 == 0 and self.igra.stevec2 == 0 and self.igra.premik_zetona is not None:
                self.sporocilo.set('Na vrsti je {} - premaknite žeton'
                                   .format(self.igra.na_vrsti))
                #Odebeli krogec, ki ga premikamo
                self.plosca.itemconfigure(self.seznam_krogcev[self.igra.premik_zetona], width=3)

        else:
             pass


    def zapri_okno(self, master):
        '''Prekine igralce in ubije program.'''
        self.prekini_igralce()
        master.destroy()

    def prekini_igralce(self):
        if self.igralec_1 is not None:
            self.igralec_1.prekini()
        if self.igralec_2 is not None:
            self.igralec_2.prekini()

    def razveljavi(self):
        self.igra.razveljavi_potezo()
        self.osvezi_plosco()


    def pripravi_novo_igro(self):
        '''Pobrise trenutno plosco, izrise prazno in ustvari nov objekt Igra.'''
        self.igra = Igra()
        self.napis1.config(
                text = "Preostali {}: ".format(IGRALEC_1)+ str(self.igra.stevec1))
        self.napis2.config(
                text = "Preostali {}: ".format(IGRALEC_2)+ str(self.igra.stevec2))
        self.osvezi_plosco()




root = Tk()
root.title("Mlin")
aplikacija = Gui(root)
root.mainloop()
