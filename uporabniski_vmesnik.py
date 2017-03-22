from tkinter import *
velikost_plosce = 400
velikost_polja = velikost_plosce/25
IGRALEC_1 = 'igralec1'
BARVA_1 = 'blue'
IGRALEC_2 = 'igralec2'
BARVA_2 = 'red'

def sredisce(krogec):
    (x1, y1, x2, y2) = krogec
    return ((x1 + x2) / 2, (y1 + y2) /2)
class Gui():

    def __init__(self, master):
        #ce se zapre okno
        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))

        self.stevec1 = IntVar(master, value=9)
        
        Label(master, text= "Preostale: {}".format(self.stevec1.get())).grid(row=0, column=0)

        self.stevec2 = IntVar(master, value=9)
        Label(master, text= "Preostale: {}".format(self.stevec2.get())).grid(row=2, column=0)

        self.na_vrsti = StringVar(master, value=IGRALEC_1)
        self.seznam_krogcev = []
        self.slovar_polj = {}
        
        #igralna plosca
        self.plosca = Canvas(master, width = velikost_plosce, height = velikost_plosce)
        self.plosca.grid(row=1, column=0)

        ##############################################
        #ustvarim 24 pik/polj
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

        for i in range(len(self.seznam_krogcev)):
            polje = Polje(self.plosca, self.seznam_krogcev[i], stevilka_polja=i+1)
            self.slovar_polj[i+1]=polje
                
        ###povezem polja med seboj
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

        self.plosca.bind("<Button-1>", self.postavi_zeton)

        self.na_vrsti = StringVar(master, value='igralec1')


    def postavi_zeton(self, event):
        (a,b) = (event.x, event.y)
        for i in range(len(self.seznam_krogcev)):
            id_krogca = self.seznam_krogcev[i]
            x, y = sredisce(self.plosca.coords(id_krogca))
            razdalja = ((a-x)**2 + (b-y)**2)**0.5
            if razdalja <= velikost_polja:#neki ne dela
                print('Ha')
                polje = self.slovar_polj[i+1]
                print(polje)
                polje.spremeni_zasedenost(self.na_vrsti.get())

    def pobarvaj_polje(self, polje):#mogoče neki ne dela
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

class Polje():#vse je vprašljivo

    def __init__(self, canvas, id_krogca, stevilka_polja):#master?
        self.canvas = canvas #/plosca
        self.id_krogca = id_krogca
        self.stevilka_polja = stevilka_polja
        self.zasedenost = None

    def spremeni_zasedenost(self, igralec=None):
        if igralec != IGRALEC_1 and igralec != IGRALEC_2:
            self.zasedenost = None
        else:
            self.zasedenost = igralec




root = Tk()
root.title("Mlin")
aplikacija = Gui(root)
root.mainloop()
