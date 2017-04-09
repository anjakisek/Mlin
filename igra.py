from tkinter import *

#Previdno pri spreminjanju imen igralcev!
IGRALEC_1 = 'modri'
BARVA_1 = 'blue'
IGRALEC_2 = 'rdeci'
BARVA_2 = 'red'


##OSTEVILCENJE POLJ
## 1  -  -  2  -  -  3
## |  4  -  5  -  6  |
## |  -  7  8  9  -  |
##10 11 12  - 13 14 15
## |  - 16 17 18  -  |
## | 19  - 20  - 21  |
##22  -  - 23  -  - 24

#Faze:
#1: postavljamo zetone
#2: premikamo zetone
#Z zadnjimi 3 zetoni se igralec lahko premika poljubno po plosci.
#Znotraj vsake faze lahko pridemo do nadaljevanja poteze, kjer odstranimo zeton.


trojke = [(1,2,3), (4,5,6), (7,8,9), (10,11,12),
          (13,14,15), (16,17,18),(19,20,21),(22,23,24),
          (1,10,22),(4,11,19),(7,12,16),(2,5,8),
          (17,20,23),(9,13,18),(6,14,21),(3,15,24)]


def nasprotnik(igralec):
    if igralec == IGRALEC_1:
        return IGRALEC_2
    elif igralec == IGRALEC_2:
        return IGRALEC_1
    else:
        assert False, 'Zgodila se je napaka pri menjavi igralcev'

    

class Polje():
    def __init__(self, canvas, id_krogca):
        self.canvas = canvas
        self.id_krogca = id_krogca
        #self.stevilka_polja = stevilka_polja
        self.zasedenost = None
        


    def spremeni_zasedenost(self, igralec=None):
        #spremenimo zasedenost polja: ce na vrsti ni noben igralec, vrne None, sicer pa pripadajoco
        #barvo igralca, ki je na vrsti
        if igralec != IGRALEC_1 and igralec != IGRALEC_2:
            self.zasedenost = None
        else:
            self.zasedenost = igralec


class Igra():
    def __init__(self, gui):
        self.gui = gui
        self.st_zetonov = {IGRALEC_1: 9, IGRALEC_2: 9}
        self.faza = 1
        self.zgodovina = []
        self.odstranitev_zetona = False
        self.poteka = False
        self.slovar_polj = {}
        self.na_vrsti = IGRALEC_1

    def shrani_trenutno_stanje(self):
        '''Shrani nabor s st. zetonov, fazo, odstranitev_zetona,
        ali poteka, kdo je navrsti in slovarjem polj'''
        trenutni_slovar_polj = {}
        for indeks in self.slovar_polj:
            polje = Polje(self.slovar_polj[indeks].canvas,
                          self.slovar_polj[indeks].id_krogca)
            polje.zasedenost = self.slovar_polj[indeks].zasedenost
            trenutni_slovar_polj[indeks] = polje
        self.zgodovina.append((self.st_zetonov, self.faza, self.odstranitev_zetona,
                               self.poteka, self.na_vrsti, trenutni_slovar_polj))
        

    def kopija(self):
        '''Napravi kopijo trenutne igre tako, da ustvari nove objekte Polja '''
        kopija = Igra()
        #kopija.gui = self.gui
        kopija.st_zetonov = self.st_zetonov
        kopija.faza = self.faza
        kopija.odstranitev_zetona = self.odstranitev_zetona
        kopija.poteka = self.poteka
        kopija.na_vrsti = self.na_vrsti

        kopija.slovar_polj = {}
        for indeks in self.slovar_polj:
            polje = Polje(self.slovar_polj[indeks].canvas,
                          self.slovar_polj[indeks].id_krogca)
            polje.zasedenost = self.slovar_polj[indeks].zasedenost
            kopija.slovar_polj[indeks] = polje
            

    def razveljavi(self):
        (self.st_zetonov, self.faza, self.odstranitev_zetona,
         self.poteka, self.na_vrsti, self.slovar_polj) = self.zgodovina.pop()


    def veljavne_poteze(self, index_polja):
        '''Naredi seznam z indeksi vseh polj, na katere lahko igramo.'''
        poteze = []
        for indeks in slovar_polj:
            if je_veljavna_poteza(indeks):
                poteze.append(indeks)



    def je_veljavna_poteza(self, index_polja):
        #ob pregledu aktivnega polja, na katerega zelimo igrati, vrne True,
        #ce je poteza veljavna, ter False sicer.
        print('Preverjam veljavnost poteze')
        aktivno_polje = self.slovar_polj[index_polja]

        
        ################################
        #### Odstranjevanje zetona #####
        ################################
        if self.odstranitev_zetona:
            #ce v potezi tece faza odstranitve, pogleda, ce je polje,
            #ki ga je treba odstraniti, nasprotnikovo
            
            if aktivno_polje.zasedenost == nasprotnik(self.na_vrsti):
                #Ce zeton, ki ga zelimo odstraniti ni v trojki, je poteza
                #veljavna:
                
                if not self.preveri_trojke(index_polja):
                    return True
                
                #Ce zeton, ki ga zelimo odstraniti, je v trojki, bo poteza
                #veljavna le, ce je vsak nasprotnikov zeton v trojki
                else:
                    #TODO?
                    #Za hitrejse delovanje, bi lahko shranjevali najdene trojke,
                    #polj v ze-najdenih trojkah potem ni treba preverjati
                    for index in self.slovar_polj:
                        polje = self.slovar_polj[index]
                        if polje.zasedenost == nasprotnik(self.na_vrsti):
                            if not self.preveri_trojke(index):
                                print('Izbrati morate zeton, ki ni v trojki')
                                return False
                    return True
                                
            else:
                print('Niste kliknili na nasprotnikov zeton')
                return False
            
        #########################################
        ##Preverjanje pri postavljanju zetonov ##
        #########################################
        if self.faza == 1:
        #ce smo v fazi dodajanja zetonov, lahko dodamo zeton na prazno polje
            if aktivno_polje.zasedenost == None:
                return True
            else:
                print('Polje je ze zasedeno')
                return False



        ########################################
        ######### Premikanje zetonov ###########
        ########################################
        elif self.faza  == 2:

            #Ce izbiramo zeton za premik, moramo izbrati svojega
            if self.gui.premik_zetona == None:
                if aktivno_polje.zasedenost == self.na_vrsti:
                    return True
                else:
                    print('Niste kliknili na svoj zeton')
                    return False

               
            else:
                if aktivno_polje.zasedenost is not None:
                    self.gui.premik_zetona = None
                    return False

                #Ce so na plosci samo se 3 zetoni, lahko z njimi poljubno skacemo
                ####TODO: zakaj mora biti tu nasprotnik?
                if self.st_zetonov[nasprotnik(self.na_vrsti)] == 3:
                    print(self.na_vrsti)
                    if aktivno_polje.zasedenost is None:
                        return True
                    else:
                        return False

                #Zeton smemo premakniti le na povezana polja 
                else:
                    je_v_trojkah = []
                    for trojka in trojke:
                        if self.gui.premik_zetona in trojka:
                            je_v_trojkah.append(trojka)
                            if len(je_v_trojkah) == 2:
                                break
                    for trojka in je_v_trojkah:
                        a = trojka.index(self.gui.premik_zetona)
                        if index_polja in trojka:
                            b = trojka.index(index_polja)
                            if abs(b-a) == 1:
                                return True                   
                    print('Niste izbrali veljavnega polja')
                    self.gui.premik_zetona = None
                    return False
                
        else:
            print('Faze ne delajo prav')




    def preveri_trojke(self, index_polja):
        je_v_trojkah = []
        for trojka in trojke:
            if index_polja in trojka:
                je_v_trojkah.append(trojka)
                if len(je_v_trojkah) == 2:
                    break
        for trojka in je_v_trojkah:
            zasedenost = None
            koncaj = None #kontroliramo, ali se mora zanka prekiniti ali ne
            for index in trojka:
                #okupiranost = kdo je po potezi na polju
                #zasedenost = kaksne barve zbiramo v trojki
                okupiranost = self.slovar_polj[index].zasedenost
                if koncaj is None:
                    if okupiranost == None:
                        koncaj = True
                        break
                        #eno polje v trojki je prazno - trojke ni
                    elif zasedenost == None:
                        #nastavimo barvo trojke, ki jo iščemo
                        zasedenost = okupiranost
                    elif zasedenost != okupiranost:
                        #v trojki je kakšna drugačna barva kot prej
                        koncaj = True
                        break
                else:
                    pass
            if koncaj is None:
                print('Nasel sem trojko')
                return True
        #Če ni našel nobene trojke:
        print('Nisem nasel trojke')
        return False

    def spremeni_fazo(self, stevilka_faze):
        self.faza = stevilka_faze


    def ali_je_konec(self):
        for igralec in self.st_zetonov:
            if self.st_zetonov[igralec] <= 2:
                self.poteka = False
                return True
        else:
            return False




                
