from tkinter import *
from igra import *
#dolocimo velikost plosce, polja, ime igralcev ter barvo posameznih zetonov
VELIKOST_PLOSCE = 400
VELIKOST_POLJA = VELIKOST_PLOSCE/25

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
        #Ce uporabnik zapre okno
        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))

        #Glavni menu
        menu = Menu(master)
        master.config(menu=menu)

        #Podmenu
        menu_igra = Menu(menu)
        menu.add_cascade(label="Igra", menu=menu_igra)
        menu_igra.add_command(label="Nova igra",
                              command=self.zacni_igro)

        self.sporocilo = StringVar(
            master,
            value='Dobrodosli! Kliknite na Nova igra, da pricnete z igro.')
        self.sporocevalec = Label(
            master,
            textvariable = self.sporocilo)
        self.sporocevalec.grid(row=0, columnspan = 2)

        #stevec, ki bo prikazoval, koliko zetonov
        #lahko prvi igralec se polozi na plosco
        self.stevec1 = IntVar(master, value=9)
        self.napis1 = Label(
            master,
            text= "Preostali {}: {}".format(
                IGRALEC_1, self.stevec1.get()))
        self.napis1.grid(row=2, column=0)
        
        #stevec, ki bo prikazoval, koliko zetonov
        #lahko drugi igralec se polozi na plosco
        self.stevec2 = IntVar(master, value=9)
        self.napis2 = Label(
            master,
            text= "Preostali {}: {}".format(
                IGRALEC_2, self.stevec2.get()))
        self.napis2.grid(row=2, column=1)

        #String, ki pove, kdo je na potezi
        self.na_vrsti = StringVar(master, value=IGRALEC_1)

        #Seznam vseh krogcev, narisanih na canvas
        self.seznam_krogcev = []

        #Slovar, ki stevilom 1 - 24 doloca pripadajoc objekt POLJE.
        #polja so oznacena od leve proti desni, od zgoraj navzdol
        self.slovar_polj = {}
        
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

        # za vsak krogec, narisan na canvas, ustvarim objekt POLJE in jih shranim
        # v slovar pod zaporedno stevilko med 1 in 24
        for i in range(len(self.seznam_krogcev)):
            polje = Polje(self.plosca, self.seznam_krogcev[i], stevilka_polja=i+1)
            self.slovar_polj[i+1]=polje

        #ob kliku na plosco poklice funkcijo, primerno trenutni fazi igre
        self.plosca.bind("<Button-1>", self.klik)

        #igro zacne vedno prvi igralec
        self.na_vrsti = StringVar(master, value=IGRALEC_1)

        #Polje, iz katerega zelimo premakniti zeton (v fazi 2)
        self.premik_zetona = None

        #Določimo vmesno fazo poteze
        #self.odstranitev_zetona = False

        self.igra = Igra(self)

    def zacni_igro(self):
        self.igra.poteka = True
        self.pripravi_novo_igro()
        self.sporocilo.set('Na vrsti je {} -> postavite zeton'.format(self.na_vrsti.get()))


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
                    index_polja = i+1
                    if self.igra.odstranitev_zetona:
                        print('Klicem odstranitev zetona')
                        self.odstrani_zeton(index_polja)
                    else:
                        self.naredi_potezo(index_polja)
                    break
        

    def naredi_potezo(self, index_polja):
        if self.igra.je_veljavna_poteza(index_polja):
            if self.igra.faza == 1:
                self.postavi_zeton(index_polja)
                if self.stevec1.get() == 0 and self.stevec2.get() == 0:
                    self.igra.spremeni_fazo(2)
            elif self.igra.faza == 2:
                print('Smo v drugi fazi')
                self.premakni_zeton(index_polja)
            else:
                print('Smo v medfazju')

                
            if self.igra.preveri_trojke(index_polja) and self.premik_zetona is None:
                self.igra.odstranitev_zetona = True
                self.sporocilo.set(
                    'Na vrsti je {} -> odstranite zeton'.format(self.na_vrsti.get()))
            elif self.igra.faza == 1:
                self.na_vrsti.set(nasprotnik(self.na_vrsti.get()))
                self.sporocilo.set(
                    'Na vrsti je {} -> postavite zeton'.format(self.na_vrsti.get()))
            elif self.igra.faza == 2:
                if self.premik_zetona is None:
                    self.na_vrsti.set(nasprotnik(self.na_vrsti.get()))
                    self.sporocilo.set(
                        'Na vrsti je {} -> izberite zeton za premik'.format(
                            self.na_vrsti.get()))
                else:
                    self.sporocilo.set(
                        'Na vrsti je {} -> izberite polje, kamor se zelite premakniti'.format(
                            self.na_vrsti.get()))
            
                
            else:
                print('Tezave pri koncu poteze')
                #self.sporocilo.set('Na vrsti je {}'.format(self.na_vrsti.get()))
        else:
            pass
        

    def postavi_zeton(self, index_polja):
        print('Postavljam zeton')
        polje = self.slovar_polj[index_polja]
        polje.spremeni_zasedenost(self.na_vrsti.get())
        self.pobarvaj_polje(polje)
        #popravi ustrezen števec žetonov
        if polje.zasedenost == IGRALEC_1:
            self.stevec1.set(self.stevec1.get()-1)
            self.napis1.config(
                text = "Preostali {}: ".format(IGRALEC_1)+ str(self.stevec1.get()))
        elif polje.zasedenost == IGRALEC_2:
            self.stevec2.set(self.stevec2.get()-1)
            self.napis2.config(
                text = "Preostali {}: ".format(IGRALEC_2)+ str(self.stevec2.get()))
        else:
            print('Napaka pri postavitvi zetona')

    def premakni_zeton(self, index_polja):
        if not self.igra.je_veljavna_poteza(index_polja):
            pass
        else:
            #Ce se nismo izbrali zetona za premik,
            #nastavimo premik na izbrano polje
            if self.premik_zetona == None:
                self.premik_zetona = index_polja
                print('Zgodil se je premik A')
            else:
                polje1 = self.slovar_polj[self.premik_zetona]
                polje1.spremeni_zasedenost()
                self.pobarvaj_polje(polje1)
                polje2 = self.slovar_polj[index_polja]
                polje2.spremeni_zasedenost(self.na_vrsti.get())
                self.pobarvaj_polje(polje2)
                self.premik_zetona = None
                #self.na_vrsti.set(nasprotnik(self.na_vrsti.get()))
                print('Zgodil se je premik B')
        

    def odstrani_zeton(self, index_polja):
        if not self.igra.je_veljavna_poteza(index_polja):
            pass
        else:
            print('Odstranjujem zeton')
            self.slovar_polj[index_polja].spremeni_zasedenost()
            print(self.slovar_polj[index_polja].zasedenost)
            self.pobarvaj_polje(self.slovar_polj[index_polja])
            self.igra.odstranitev_zetona = False
            self.igra.st_zetonov[self.na_vrsti.get()] -= 1
            if self.igra.ali_je_konec():
                self.sporocilo.set(
                    'Igre je konec, zmagal je {}'.format(
                        self.na_vrsti.get()))
            else:
                self.na_vrsti.set(nasprotnik(self.na_vrsti.get()))
                if self.igra.faza == 1:
                    self.sporocilo.set('Na vrsti je {} -> postavite zeton'.format(
                        self.na_vrsti.get()))
                elif self.igra.faza == 2:
                    self.sporocilo.set('Na vrsti je {} -> izberite zeton za premik'.format(
                        self.na_vrsti.get()))
                print('Dokoncal odstranitev')

    
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
        master.destroy()
        
    def pripravi_novo_igro(self):
        for index in self.slovar_polj:
            polje = self.slovar_polj[index]
            polje.spremeni_zasedenost()
            self.pobarvaj_polje(polje)
        self.igra.spremeni_fazo(1)
        self.na_vrsti.set(IGRALEC_1)
        self.stevec1.set(9)
        self.stevec2.set(9)




root = Tk()
root.title("Mlin")
aplikacija = Gui(root)
root.mainloop()
