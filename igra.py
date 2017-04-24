from tkinter import *

#Previdno pri spreminjanju imen igralcev!
IGRALEC_1 = 'modri'
BARVA_1 = 'blue'
IGRALEC_2 = 'rdeci'
BARVA_2 = 'red'


##OSTEVILCENJE POLJ
## 0  -  -  1  -  -  2
## |  3  -  4  -  5  |
## |  -  6  7  8  -  |
## 9 10 11  - 12 13 14
## |  - 15 16 17  -  |
## | 18  - 19  - 20  |
##21  -  - 22  -  - 23

#Faze:
#FAZA_POSTAVI: postavljamo zetone
#FAZA_ODSTRANI : odstranjujemo zetone
#FAZA_PREMAKNI_IZBERI: izbiramo zetone za premik oznacimo s spremenljivko premakni
#FAZA_PREMAKNI: izbiramo mesto za premik

#Z zadnjimi 3 zetoni se igralec lahko premika poljubno po plosci.
#Znotraj vsake faze lahko pridemo do nadaljevanja poteze, kjer odstranimo zeton.

trojke = [(0,1,2), (3,4,5), (6,7,8), (9,10,11),
          (12,13,14), (15,16,17),(18,19,20),(21,22,23),
          (0,9,21),(3,10,18),(6,11,15),(1,4,7),
          (16,19,22),(8,12,17),(5,13,20),(2,14,23)]


def nasprotnik(igralec):
    if igralec == IGRALEC_1:
        return IGRALEC_2
    elif igralec == IGRALEC_2:
        return IGRALEC_1
    else:
        assert False, 'Zgodila se je napaka pri menjavi igralcev'

    

class Igra():
    def __init__(self):
        #Plosca je predstavljena s seznamom s 24 elementi. Niz na dolocenem mestu
        # pomeni zasedenost mesta s tistim igralcem
        self.plosca = [None]* 24

        #Stevilo zetonov, ki jih ima igralec se na voljo za igro
        self.st_zetonov = {IGRALEC_1: 9, IGRALEC_2: 9}

        #Ali smo v fazi odstranjevanja?
        self.odstranitev_zetona = False

        #Iz stevca vemo, v kateri fazi smo
        self.stevec1 = 9
        self.stevec2 = 9

        #Izvemo, ali moramo koncati
        self.poteka = False
        
        #Polje, iz katerega zelimo premakniti zeton (v fazi FAZA_PREMAKNI)
        self.premik_zetona = None
        
        self.na_vrsti = IGRALEC_1

        self.st_potez = 0
        
        self.zgodovina = []


    def shrani_trenutno_stanje(self):
        '''Shrani nabor, ki vsebuje trenutne vrednosti atributov objekta Igra
            na konec seznama self.zgodovina.'''
        novi_st_zetonov = {}
        for igralec in self.st_zetonov:
            novi_st_zetonov[igralec] = self.st_zetonov[igralec]
        self.zgodovina.append((self.plosca[:], novi_st_zetonov,
                               self.odstranitev_zetona,
                               self.stevec1, self.stevec2,
                               self.poteka, self.premik_zetona,
                               self.na_vrsti, self.st_potez))
        

    def kopija(self):
        '''Napravi kopijo trenutne igre tako, da skopira trenutne atribute
            igre, nato vrne kopijo igre.'''
        kopija = Igra()
        kopija.plosca = self.plosca[:]
        
        kopija.st_zetonov = {}
        for igralec in self.st_zetonov:
            kopija.st_zetonov[igralec] = self.st_zetonov[igralec]
            
        kopija.stevec1 = self.stevec1
        kopija.stevec2 = self.stevec2
        kopija.odstranitev_zetona = self.odstranitev_zetona
        kopija.poteka = self.poteka
        kopija.premik_zetona = self.premik_zetona
        kopija.na_vrsti = self.na_vrsti
        kopija.st_potez = self.st_potez
        return kopija
            

    def razveljavi_potezo(self):
        '''Igri posreduje atribute zadnjega elementa v seznamu zgodovine,
           ta element odstrani.'''
        if self.zgodovina == []:
            pass
        else:
            (self.plosca, self.st_zetonov, self.odstranitev_zetona,
             self.stevec1, self.stevec2,
             self.poteka, self.premik_zetona,
             self.na_vrsti, self.st_potez) = self.zgodovina.pop()
            

    def povleci_potezo(self, index_polja):
        '''Ce je poteza veljavna, jo povlece in vrne True, sicer vrne False'''
        #Ce poteza ni veljavna, le ponastavi izbrani zeton za premik na None
        if not self.je_veljavna_poteza(index_polja):
            self.premik_zetona = None
            return False
        
        else:
            self.shrani_trenutno_stanje()
            self.st_potez += 1
            #FAZA_ODSTRANI
            if self.odstranitev_zetona:
                self.plosca[index_polja] = None
                self.odstranitev_zetona = False
                self.st_zetonov[nasprotnik(self.na_vrsti)] -= 1
                if not self.ali_je_konec():
                    self.na_vrsti = nasprotnik(self.na_vrsti)
                    return True
                else:
                    return True
            
            #FAZA_POSTAVI
            elif self.stevec1 > 0 or self.stevec2 > 0:
                self.plosca[index_polja] = self.na_vrsti
                if self.na_vrsti == IGRALEC_1:
                    self.stevec1 -= 1
                elif self.na_vrsti == IGRALEC_2:
                    self.stevec2 -= 1

                #Preveri se trojke in morebiti zamenja, kdo je na potezi
                if self.preveri_trojke(index_polja):
                    self.odstranitev_zetona = True
                    return True
                else:
                    self.na_vrsti = nasprotnik(self.na_vrsti)
                    return True

            #FAZA_PREMAKNI_ZETON
            elif self.stevec1 == 0 and self.stevec2 == 0:
                
                #FAZA_PREMAKNI_IZBERI
                if self.premik_zetona is None:
                    self.premik_zetona = index_polja
                    return True
                    
                #FAZA_PREMAKNI_POSTAVI
                else:
                    self.plosca[index_polja] = self.na_vrsti
                    self.plosca[self.premik_zetona] = None
                    self.premik_zetona = None
                    #Preveri se trojke in morebiti zamenja, kdo je na potezi
                    if self.preveri_trojke(index_polja):
                        self.odstranitev_zetona = True
                        return True
                    else:
                        self.na_vrsti = nasprotnik(self.na_vrsti)
                        if self.zablokiran():
                            self.na_vrsti = nasprotnik(self.na_vrsti)
                            self.poteka = False
                        return True

            else:
                assert False, 'neveljavna faza!'




    def veljavne_poteze(self):
        '''Naredi seznam z indeksi vseh polj, na katere lahko igramo.'''
        poteze = []
        for indeks in range(len(self.plosca)):
            if self.je_veljavna_poteza(indeks):
                poteze.append(indeks)
        return poteze



    def je_veljavna_poteza(self, index_polja):
        '''ob pregledu aktivnega polja, na katerega zelimo igrati, vrne True,
        ce je poteza veljavna, ter False sicer.'''

        
        ################################
        #### Odstranjevanje zetona #####
        ################################
        if self.odstranitev_zetona:
            #Ce v potezi tece faza odstranitve, pogleda, ce je polje,
            # ki ga je treba odstraniti, nasprotnikovo
            
            if self.plosca[index_polja] == nasprotnik(self.na_vrsti):
                #Ce zeton, ki ga zelimo odstraniti ni v trojki, je poteza
                #veljavna:
                if not self.preveri_trojke(index_polja):
                    return True
                
                #Ce zeton, ki ga zelimo odstraniti, je v trojki, bo poteza
                #veljavna le, ce je vsak nasprotnikov zeton v trojki
                else:
                    for index in range(0, 24):
                        if self.plosca[index] == nasprotnik(self.na_vrsti):
                            if not self.preveri_trojke(index):
                                return False
                    return True
                                
            else:
                return False
            
        #########################################
        ##Preverjanje pri FAZA_POSTAVITE##
        #########################################
        
        if self.stevec1 > 0 or self.stevec2 > 0:
        #Ce smo v fazi dodajanja zetonov, lahko dodamo zeton na prazno polje
            if self.plosca[index_polja] == None:
                return True
            else:
                return False



        ########################################
        # Premikanje zetonov - FAZA_PREMIKANJE #
        ########################################
        elif self.stevec1 == 0 and self.stevec2 == 0:
            #Ce izbiramo zeton za premik, moramo izbrati svojega
            if self.premik_zetona == None:
                if self.plosca[index_polja] == self.na_vrsti:
                    return True
                else:
                    return False

               
            else:
                if self.plosca[index_polja] is not None:
                    return False

                #Ce so na plosci samo se 3 zetoni,
                #lahko z njimi poljubno skacemo
                if self.st_zetonov[self.na_vrsti] == 3:
                    if self.plosca[index_polja] is None:
                        return True
                    else:
                        return False

                #Zeton smemo premakniti le na povezana polja 
                else:
                    if index_polja in self.povezana_polja(self.premik_zetona):
                                return True                   
                    return False
                
        else:
            print('Faze ne delajo prav')


    def povezana_polja(self, index_polja):
        '''Vrne seznam polj, ki so z danim povezana.'''
        je_v_trojkah = []
        for trojka in trojke:
            if index_polja in trojka:
                je_v_trojkah.append(trojka)
                if len(je_v_trojkah) == 2:
                    break
        povezana_polja = []
        for trojka in je_v_trojkah:
            a = trojka.index(index_polja)
            for polje in trojka:
                b = trojka.index(polje)
                if abs(b-a) == 1:
                    povezana_polja.append(trojka[b])
        return povezana_polja
                    


    def preveri_trojke(self, index_polja):
        '''Preveri, ali je bila formirana trojka.'''
        
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
                okupiranost = self.plosca[index]
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
                return True
            
        #Če ni našel nobene trojke:
        return False


    def zablokiran(self):
        for i in range(24):
            if self.plosca[i] == self.na_vrsti:
                for polje in self.povezana_polja(i):
                    if self.plosca[polje] == None:
                        return False
        return True
        
            

    
    def ali_je_konec(self):
        '''Vrne True, ce je igre konec in False sicer. Pri tem nastavi
        self.poteka na pravilno vrednost.'''
        for igralec in self.st_zetonov:
            if self.st_zetonov[igralec] <= 2:
                self.poteka = False
                return True
        
        else:
            return False




                
