from tkinter import *

#Previdno pri spreminjanju imen igralcev!
IGRALEC_1 = 'modri'
BARVA_1 = 'blue'
IGRALEC_2 = 'rdeči'
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
#FAZA_ODSTRANI: odstranjujemo zetone
#FAZA_PREMAKNI_IZBERI: izbiramo zetone za premik, izbrani zeton oznacimo s spremenljivko premakni
#FAZA_PREMAKNI_POSTAVI: izbiramo mesto za premik

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

        #Slovar s stevilom zetonov, ki jih ima igralec se na voljo za igro
        self.st_zetonov = {IGRALEC_1: 9, IGRALEC_2: 9}

        #Ali smo v fazi odstranjevanja? Predstavljeno z Boolovo vrednostjo.
        self.ali_odstranjujemo_zeton = False

        #Stevec steje, koliko zetonov se lahko polozimo na plosco
        self.stevec1 = 9
        self.stevec2 = 9

        # Ali igra trenutno poteka (na zacetku seveda poteka)
        self.poteka = True

        #Polje, iz katerega zelimo premakniti zeton (nastavimo v FAZA_PREMAKNI_IZBERI)
        self.premik_zetona = None

        self.na_vrsti = IGRALEC_1

        self.st_potez = 0

        self.zgodovina = []


    def shrani_trenutno_stanje(self):
        '''Shrani nabor, ki vsebuje trenutne vrednosti atributov objekta Igra,
            na konec seznama self.zgodovina.'''
        novi_st_zetonov = {}
        for igralec in self.st_zetonov:
            novi_st_zetonov[igralec] = self.st_zetonov[igralec]
        self.zgodovina.append((self.plosca[:], novi_st_zetonov,
                               self.ali_odstranjujemo_zeton,
                               self.stevec1, self.stevec2,
                               self.poteka, self.premik_zetona,
                               self.na_vrsti, self.st_potez))


    def kopija(self):
        '''Napravi kopijo trenutne igre tako, da skopira trenutne atribute
            igre, nato vrne kopijo igre kot objekt.'''
        kopija = Igra()
        kopija.plosca = self.plosca[:]

        kopija.st_zetonov = {}
        for igralec in self.st_zetonov:
            kopija.st_zetonov[igralec] = self.st_zetonov[igralec]

        kopija.stevec1 = self.stevec1
        kopija.stevec2 = self.stevec2
        kopija.ali_odstranjujemo_zeton = self.ali_odstranjujemo_zeton
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
            (self.plosca, self.st_zetonov, self.ali_odstranjujemo_zeton,
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
            #Odstranimo zeton, ponastavimo atribut ali_odstranjujemo_zeton,
            # preverimo, ce je igre konec.
            if self.ali_odstranjujemo_zeton:
                self.plosca[index_polja] = None
                self.ali_odstranjujemo_zeton = False
                self.st_zetonov[nasprotnik(self.na_vrsti)] -= 1
                if not self.ali_je_konec():
                    self.na_vrsti = nasprotnik(self.na_vrsti)
                    return True
                else:
                    return True

            #FAZA_POSTAVI
            #Postavimo zeton na plosco, preverimo, ce smo s tem napravili trojko. Pri zadnjih
            # postavljenih zetonih preverimo, ce so nasprotnikovi zetoni zablokirani.
            elif self.stevec1 > 0 or self.stevec2 > 0:
                self.plosca[index_polja] = self.na_vrsti
                if self.na_vrsti == IGRALEC_1:
                    self.stevec1 -= 1
                elif self.na_vrsti == IGRALEC_2:
                    self.stevec2 -= 1

                #Preveri se trojke in morebiti zamenja, kdo je na potezi
                if self.je_v_trojki(index_polja):
                    self.ali_odstranjujemo_zeton = True
                    return True
                else:
                    #Preveri, ali so nasprotnikovi zetoni zablokiran_igraleci
                    if self.stevec1 == 0:
                        if not self.ali_je_konec():
                            self.na_vrsti = nasprotnik(self.na_vrsti)
                            return True
                    else:
                        self.na_vrsti = nasprotnik(self.na_vrsti)
                        return True

            #FAZA_PREMAKNI_IZBERI ali FAZA_PREMAKNI
            elif self.stevec1 == 0 and self.stevec2 == 0:

                #FAZA_PREMAKNI_IZBERI
                #V atribut premik shrani izbrani zeton
                if self.premik_zetona is None:
                    self.premik_zetona = index_polja
                    return True

                #FAZA_PREMAKNI
                #Izbrani zeton premakne na izbrano mesto. Preveri trojke ter ali je nasprotnik
                # zablokiran_igralec.
                else:
                    self.plosca[index_polja] = self.na_vrsti
                    self.plosca[self.premik_zetona] = None
                    self.premik_zetona = None
                    #Preveri se trojke in morebiti zamenja, kdo je na potezi
                    if self.je_v_trojki(index_polja):
                        self.ali_odstranjujemo_zeton = True
                        return True
                    else:
                        if not self.ali_je_konec():
                            self.na_vrsti = nasprotnik(self.na_vrsti)
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
        '''Ob pregledu aktivnega polja, na katerega zelimo igrati, vrne True,
        ce je poteza veljavna, ter False sicer.'''


        ###########################
        #####  FAZA_ODSTRANI  #####
        ###########################
        if self.ali_odstranjujemo_zeton:
            #Ce v potezi tece faza odstranitve, pogleda, ce je polje,
            # ki ga je treba odstraniti, nasprotnikovo

            if self.plosca[index_polja] == nasprotnik(self.na_vrsti):
                #Ce zeton, ki ga zelimo odstraniti, ni v trojki, je poteza
                #veljavna:
                if not self.je_v_trojki(index_polja):
                    return True

                #Ce zeton, ki ga zelimo odstraniti, je v trojki, bo poteza
                #veljavna le, ce je vsak nasprotnikov zeton v trojki
                else:
                    for index in range(0, 24):
                        if self.plosca[index] == nasprotnik(self.na_vrsti):
                            if not self.je_v_trojki(index):
                                return False
                    return True

            else:
                return False

        ##########################
        #####  FAZA_POSTAVI  #####
        ##########################

        if self.stevec1 > 0 or self.stevec2 > 0:
        #Zeton lahko dodamo na prazno polje
            if self.plosca[index_polja] == None:
                return True
            else:
                return False



        ################################
        ##### FAZA_PREMAKNI_IZBERI #####
        ################################
        elif self.stevec1 == 0 and self.stevec2 == 0:
            #Izbrati moramo svoj zeton
            if self.premik_zetona == None:
                if self.plosca[index_polja] == self.na_vrsti:
                    #Ce je v fazi skakanja
                    if self.st_zetonov[self.na_vrsti] == 3:
                        return True
                    elif not self.je_zeton_zablokiran(index_polja):
                        return True
                else:
                    return False

        ##################################
        #####  FAZA_PREMAKNI_POSTAVI  #####
        ##################################
                
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


    def povezana_polja(self, polje):
        '''Vrne seznam polj, ki so z danim povezana.'''
        povezana_polja = []
        #Pregledamo vse trojke, ki vsebujejo polje
        for (i,j,k) in [t for t in trojke if polje in t]:
            #Ce je polje na sredini trojke, je povezan s stranskima
            if polje == i or polje == k:
                povezana_polja.append(j)
            #Ce je polje pri strani, je povezan le s sredinskim
            elif polje == j:
                povezana_polja.extend((i,k))
                
        return povezana_polja



    def je_v_trojki(self, polje):
        '''Preveri, ali je dano polje v trojki. Vrni True, če je, sicer False.'''

        # Gremo po trojkah, ki vsebujejo polje
        for (i,j,k) in [t for t in trojke if polje in t]:
            if (self.plosca[i] != None and self.plosca[i] == self.plosca[j] == self.plosca[k]):
                # nasli smo neprazno trojko
                return True
        return False


    def zablokiran_igralec(self):
        '''Vrne True, ce nasprotnik igralca, ki je na potezi, nima mozne veljavne poteze,
        in False sicer.'''
        for i in range(24):
            if self.plosca[i] == nasprotnik(self.na_vrsti):
                for polje in self.povezana_polja(i):
                    if self.plosca[polje] == None:
                        return False
        return True

    def je_zeton_zablokiran(self, polje):
        '''Vrne True, ce se zeton na danem polju ne more premakniti nikamor, in False sicer.'''
        for t in self.povezana_polja(polje):
            if self.plosca[t] == None:
                return False
        return True




    def ali_je_konec(self):
        '''Vrne True, ce je igre konec zaradi premalo zetonov ali zablokiranosti igralca,
        in False sicer. Pri tem nastavi self.poteka na pravilno vrednost.'''
        for igralec in self.st_zetonov:
            if self.st_zetonov[igralec] <= 2:
                self.poteka = False
                return True
            elif self.zablokiran_igralec():
                self.poteka = False
                return True
        
        return False
