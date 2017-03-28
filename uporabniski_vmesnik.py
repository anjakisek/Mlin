from tkinter import *
from igra import *
#dolocimo velikost plosce, polja, ime igralcev ter barvo posameznih zetonov
velikost_plosce = 400
velikost_polja = velikost_plosce/25
#Igralci in barve testno prestavljeni v igra.py
##IGRALEC_1 = 'igralec1'
##BARVA_1 = 'blue'
##IGRALEC_2 = 'igralec2'
##BARVA_2 = 'red'

##OSTEVILCENJE POLJ
## 1  -  -  2  -  -  3
## |  4  -  5  -  6  |
## |  -  7  8  9  -  |
##10 11 12  - 13 14 15
## |  - 16 17 18  -  |
## | 19  - 20  - 21  |
##22  -  - 23  -  - 24

def sredisce(krogec):
    (x1, y1, x2, y2) = krogec
    return ((x1 + x2) / 2, (y1 + y2) /2)

class Gui():

    def __init__(self, master):
        #ce se zapre okno
        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))

        #stevec, ki se bo prikazoval, koliko zetonov
        #lahko prvi igralec se polozi na plosco
        self.stevec1 = IntVar(master, value=9)
        Label(#TODO: popravi label, da se text spreminja s stevcem 1
            master,
            text= "Preostale: {}".format(self.stevec1.get())).grid(row=0, column=0)
        
        #stevec, ki se bo prikazoval, koliko zetonov
        #lahko drugi igralec se polozi na plosco
        self.stevec2 = IntVar(master, value=9)
        Label(#TODO: popravi label, da se text spreminja s stevcem 2
            master,
            text= "Preostale: {}".format(self.stevec2.get())).grid(row=2, column=0)

        #string, ki pove, kdo je na potezi
        self.na_vrsti = StringVar(master, value=IGRALEC_1)

        #seznam vseh krogcev, narisanih na canvas
        self.seznam_krogcev = []

        #slovar, ki stevilom 1 - 24 doloca pripadajoc objekt POLJE.
        #polja so oznacena od leve proti desni, od zgoraj navzdol
        self.slovar_polj = {}
        
        #igralna plosca
        self.plosca = Canvas(master, width = velikost_plosce, height = velikost_plosce)
        self.plosca.grid(row=1, column=0)

        ##############################################
        #ustvarim 24 pik/polj in njihove id shranim v seznam krogcev v pravilnem
        # vrstnem redu
        for k in range(0, 2): #krogci 10-15
            for i in range(0, 3):
                id_krogca = self.plosca.create_oval(velikost_plosce * (1/8 + i/8 + k/2) - velikost_polja,
                                          velikost_plosce/2 - velikost_polja,
                                          velikost_plosce * (1/8 + i/8 + k/2) + velikost_polja,
                                          velikost_plosce/2 + velikost_polja)
                self.seznam_krogcev.append(id_krogca)

        for k in range(0, 2):#krogci 7-9, 16-18
            seznam=[]
            for i in range(0, 3):
                id_krogca = self.plosca.create_oval(velikost_plosce * (3/8 + i/8) - velikost_polja,
                                        velikost_plosce * (3/8 + k/4) - velikost_polja,
                                        velikost_plosce * (3/8 + i/8) + velikost_polja,
                                        velikost_plosce * (3/8 + k/4) + velikost_polja)
                seznam.append(id_krogca)
            if k == 0:
                self.seznam_krogcev = seznam + self.seznam_krogcev
            else:
                self.seznam_krogcev = self.seznam_krogcev + seznam

        for k in range(0, 2):#krogci 4-6, 19-21
            seznam = []
            for i in range(0, 3):
                id_krogca = self.plosca.create_oval(velikost_plosce * (1/4 + i/4) - velikost_polja,
                                        velikost_plosce * (1/4 + k/2) - velikost_polja,
                                        velikost_plosce * (1/4 + i/4) + velikost_polja,
                                        velikost_plosce * (1/4 + k/2) + velikost_polja)
                seznam.append(id_krogca)
            if k == 0:
                self.seznam_krogcev = seznam + self.seznam_krogcev
            else:
                self.seznam_krogcev = self.seznam_krogcev + seznam

        for k in range(0, 2):#krogci 1-3, 22-24
            seznam = []
            for i in range(0, 3):
                id_krogca = self.plosca.create_oval(
                    velikost_plosce * (1/8 + i * 3/8) - velikost_polja,
                    velikost_plosce * (1/8 + k * 3/4) - velikost_polja,
                    velikost_plosce *(1/8 + i * 3/8) + velikost_polja,
                    velikost_plosce * (1/8 + k * 3/4) + velikost_polja)
                seznam.append(id_krogca)
            if k == 0:
                self.seznam_krogcev = seznam + self.seznam_krogcev
            else:
                self.seznam_krogcev = self.seznam_krogcev + seznam
                
        #povezem polja med seboj
        for i in range(0, 3):
            self.plosca.create_rectangle(velikost_plosce * (1/8 + i/8),
                                         velikost_plosce * (1/8 + i/8),
                                         velikost_plosce * (7/8 - i/8) ,
                                         velikost_plosce * (7/8 - i/8))

        self.plosca.create_line(velikost_plosce/2, velikost_plosce/8,velikost_plosce/2,
                                3 * velikost_plosce/8)
        self.plosca.create_line(velikost_plosce/2, 5 * velikost_plosce/8,velikost_plosce/2,
                                7 * velikost_plosce/8)
        self.plosca.create_line(velikost_plosce/8, velikost_plosce/2,3 * velikost_plosce/8,
                                velikost_plosce/2)
        self.plosca.create_line(5 * velikost_plosce/8, velikost_plosce/2,7 * velikost_plosce/8,
                                velikost_plosce/2)
        
                                         
        #################################
        #################################

        # za vsak krogec, narisan na canvas, ustvarim objekt POLJE in jih shranim
        # v slovar podzaporedno stevilko med 1 in 24
        for i in range(len(self.seznam_krogcev)):
            polje = Polje(self.plosca, self.seznam_krogcev[i], stevilka_polja=i+1)
            self.slovar_polj[i+1]=polje

        #ob kliku na plosco poklice funkcijo postavi zeton
        self.plosca.bind("<Button-1>", self.klik)

        #igro zacne vedno prvi igralec
        self.na_vrsti = StringVar(master, value='igralec1')

    def klik(self, event):
        self.postavi_zeton(event)

    def postavi_zeton(self, event):
        (a,b) = (event.x, event.y)
        for i in range(len(self.seznam_krogcev)):
            id_krogca = self.seznam_krogcev[i]
            x, y = sredisce(self.plosca.coords(id_krogca))
            razdalja = ((a-x)**2 + (b-y)**2)**0.5
            #ce smo kliknili znotraj krogca, bomo na polju oznacili, da je
            #zaseden s trenutnim igralcem. Na koncu pobarvamo polje na pravilno barvo
            if razdalja <= velikost_polja:
                polje = self.slovar_polj[i+1]
                polje.spremeni_zasedenost(self.na_vrsti.get())
                self.pobarvaj_polje(polje)
                #popravi ustrezen števec žetonov
                if polje.zasedenost == IGRALEC_1:
                    self.stevec1.set(self.stevec1.get()-1)
                elif polje.zasedenost == IGRALEC_2:
                    self.stevec2.set(self.stevec2.get()-1)
                else:
                    pass

    
    def pobarvaj_polje(self, polje):
        #pobravamo krogec glede na to, kateri igralec je zasedel polje
        if polje.zasedenost == IGRALEC_1:
            barva = BARVA_1
        elif polje.zasedenost == IGRALEC_2:
            barva = BARVA_2
        else:#samo None je lahko
            barva = 'white'
        self.plosca.itemconfigure(polje.id_krogca, fill=barva)
        

        
    def zapri_okno(self, master):
        self.prekini_igralce()
        master.destroy()
        
    def prekini_igralce(self):
        #TODO
        pass

#Class Polje testno prestavljeno v igra.py
##class Polje():
##
##    def __init__(self, canvas, id_krogca, stevilka_polja):#master?
##        self.canvas = canvas #/plosca
##        self.id_krogca = id_krogca
##        self.stevilka_polja = stevilka_polja
##        self.zasedenost = None
##
##
##    def spremeni_zasedenost(self, igralec=None):
##        #spremenimo zasedenost polja: ce na vrsti ni noben igralec, vrne None, sicer pa pripadajoco
##        #barvo igralca, ki je na vrsti
##        if igralec != IGRALEC_1 and igralec != IGRALEC_2:
##            self.zasedenost = None
##        else:
##            self.zasedenost = igralec




root = Tk()
root.title("Mlin")
aplikacija = Gui(root)
root.mainloop()
