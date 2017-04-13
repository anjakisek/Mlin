from tkinter import *
from igra import *
from racunalnik_igralec import *
from clovek import *
from minimax import *



#dolocimo velikost plosce in polja
VELIKOST_PLOSCE = 400
VELIKOST_POLJA = VELIKOST_PLOSCE/25
globina = 3

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
        self.igralec_1 = None 
        self.igralec_2 = None


        #Ce uporabnik zapre okno
        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))

        #Zacasno premaknjen naprej, da bo obstajala ze prej, kot pa rabimo
        #slovar polj
        self.igra = Igra()

        #Glavni menu
        menu = Menu(master)
        master.config(menu=menu)

        #Podmenu: Igra
        menu_igra = Menu(menu)
        menu.add_cascade(label="Igra", menu=menu_igra)
        menu_igra.add_command(label="Clovek vs. Clovek",
                              command=lambda: self.zacni_igro(
                                  Clovek(self),
                                Clovek(self)))
        menu_igra.add_command(label="Clovek vs. Racunalnik",
                              command=lambda: self.zacni_igro(
                                  Clovek(self),
                                        Racunalnik(self, Minimax(globina))))
        menu_igra.add_command(label="Racunalnik vs. Clovek",
                              command=lambda: self.zacni_igro(
                                  Racunalnik(self, Minimax(globina)),
                                                Clovek(self)))
        menu_igra.add_command(label="Racunalnik vs. Racunalnik",
                              command=lambda: self.zacni_igro(
                                  Racunalnik(self, Minimax(globina)),
                                        Racunalnik(self, Minimax(globina))))
        #Podmenu: Moznosti
        menu_moznosti = Menu(menu)
        menu.add_cascade(label="Moznosti", menu=menu_moznosti)
        menu_moznosti.add_command(label="Razveljavi",
                                  command=self.razveljavi)


        #Napis nad igralno plosco
        self.sporocilo = StringVar(
            master,
            value='Dobrodosli! Izberite tipe igralcev, da pricnete z igro.')
        self.sporocevalec = Label(
            master,
            textvariable = self.sporocilo)
        self.sporocevalec.grid(row=0, columnspan = 2)

        #Stevec, ki bo prikazoval, koliko zetonov
        #lahko prvi igralec se polozi na plosco
        #self.stevec1 = IntVar(master, value=9)
        self.napis1 = Label(
            master,
            text= "Preostali {}: {}".format(
                IGRALEC_1, self.igra.stevec1))
        self.napis1.grid(row=2, column=0)
        
        #Stevec, ki bo prikazoval, koliko zetonov
        #lahko drugi igralec se polozi na plosco
        self.stevec2 = IntVar(master, value=9)
        self.napis2 = Label(
            master,
            text= "Preostali {}: {}".format(
                IGRALEC_2, self.igra.stevec2))
        self.napis2.grid(row=2, column=1)



        self.seznam_krogcev = []


        
        #Igralna plosca
        self.plosca = Canvas(
            master, width = VELIKOST_PLOSCE, height = VELIKOST_PLOSCE,
            bg = 'white')
        self.plosca.grid(row=1, column=0, columnspan=2)



        ##############################################
        ##############################################
        #povezem polja med seboj
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
        
        #ustvarim 24 pik/polj in njihove id shranim v seznam krogcev v pravilnem
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

    

        #ob kliku na plosco poklice funkcijo, primerno trenutni fazi igre
        self.plosca.bind("<Button-1>", self.klik)

    


        


    def zacni_igro(self, igralec1, igralec2):
        self.prekini_igralce()
        self.igralec_1 = igralec1
        self.igralec_2 = igralec2
        self.igra.poteka = True
        self.pripravi_novo_igro()
        self.sporocilo.set('Na vrsti je {} - postavite žeton'.format(self.igra.na_vrsti))
        self.igralec_1.igraj()


    def klik(self, event):
        if not self.igra.poteka:
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
        if self.igra.povleci_potezo(index_polja):
            self.osvezi_plosco()
            if not self.igra.poteka:
                self.sporocilo.set(
                    'Igre je konec, zmagal je {}'.format(
                     self.igra.na_vrsti))
            elif self.igra.odstranitev_zetona:
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

            else:
                print('Obstaja faza, ki je gui zdaj ni znal sprocesirati')

            if self.igra.na_vrsti == IGRALEC_1:
                self.igralec_1.igraj()
            elif self.igra.na_vrsti == IGRALEC_2:
                self.igralec_2.igraj()
            else:
                print('Naprej ne more igrati nihce')
                

        else:
            if self.igra.stevec1 == 0 and self.igra.stevec2 == 0:
                self.sporocilo.set('Na vrsti je {} - izberite žeton za premik'
                                   .format(self.igra.na_vrsti))

    def osvezi_plosco(self):
        self.napis1.config(text = "Preostali {}: "
                           .format(IGRALEC_1)+ str(self.igra.stevec1))
        self.napis2.config(text = "Preostali {}: "
                           .format(IGRALEC_2)+ str(self.igra.stevec2))
        for polje in range(0, 24):
            if self.igra.plosca[polje] == IGRALEC_1:
                barva = BARVA_1
            elif self.igra.plosca[polje] == IGRALEC_2:
                barva = BARVA_2
            else:
                barva = 'white'
            self.plosca.itemconfigure(self.seznam_krogcev[polje], fill=barva)
        
            

        
    def zapri_okno(self, master):
        self.prekini_igralce()
        master.destroy()

    def prekini_igralce(self):
        #TODO
        pass

    #Poskusno vpeljana razveljavitev:
    def razveljavi(self):
        self.igra.razveljavi_potezo()
        self.osvezi_plosco()
    
        
    def pripravi_novo_igro(self):
        self.igra.plosca = [None] * 24
        self.igra.zgodovina = []
        self.igra.na_vrsti = IGRALEC_1
        self.igra.odstranitev_zetona = False
        self.igra.premik_zetona = None
        self.igra.stevec1 = 9
        self.napis1.config(
                text = "Preostali {}: ".format(IGRALEC_1)+ str(self.igra.stevec1))
        self.igra.stevec2 = 9
        self.napis2.config(
                text = "Preostali {}: ".format(IGRALEC_2)+ str(self.igra.stevec2))
        self.igra.st_zetonov[IGRALEC_1] = 9
        self.igra.st_zetonov[IGRALEC_2] = 9
        self.osvezi_plosco()




root = Tk()
root.title("Mlin")
aplikacija = Gui(root)
root.mainloop()
