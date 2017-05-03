# Mlin
Igrica [Mlin](https://en.wikipedia.org/wiki/Nine_Men%27s_Morris).

# Načrt dela:
- 20.3. - 26. 3.: Postavitev repozitorija, uporabniški vmesnik
- 27.3. - 2.4.: uporabniški vmesnik in prva faza igre
- 3.3. - 9.4.: druga faza in igrica 1 na 1, začetek dela na računalniku kot igralcu
- 10.4. - 16.4.: računalnik proti računalniku, odprava napak
- 16.4. - : odprava napak, testiranje

# Struktura igre:
Igra je razdeljena v več datotek:
- uporabniski_vmesnik.py
	Glavni program, ki izriše igralno ploščo in skrbi, da se narejena poteza izriše na zaslonu. V menijski vrstici so naslednja okenca:
	- _Igra_ : uporabnik lahko izbere tipe igralcev (kombinacije igralca-človeka in računalniškega igralca)
	- _Težavnost_: v kolikor uporabnik izbere računalniškega igralca, lahko izbira med težjo in lažjo zahtevnostjo igre. Privzeta tezavnost je lazja, ki uporablja algoritem minimax, za težjo zahtevnost pa uporablja minimax z alphabeta rezanjem in povečano globino iskanja.
	- _Moznosti_: uporabnik lahko razveljavi svojo potezo.

- igra.py
	V uporabniškem vmesniku je seznam, kjer so v seznamu _seznam_krogcev_ shranjeni id posameznih krogcev na plošči, Igra pa uporablja seznam _plosca_, kjer vsak element ponazarja zasedenost določenega polja. Seznamoma so skupni indeksi, torej: četrti element v seznamu predstavja četrto polje.
	Igra je razdeljena v 4 faze: postavljanje žetonov, odstranjevanje žetonov, izbiranje žetona za premik in izbiranje polja, kamor bomo žeton premaknili. Tako poteza, kjer izberemo žeton, ga premaknemo na drugo polje in zaradi morebitne trojke odstranimo še nasprotnikov žeton, šteje za tri poteze, čeprav smo na vrsti le enkrat. Znotraj faze premikanja tudi velja, da če ima igralec na razpolago le še tri žetone, se lahko premakne na poljubno mesto, ne le na povezana polja.

- clovek.py

- racunalniski_igralec.py
	Zažene vzporedno vlakno, ki s pomočjo izbranega algoritma izračuna optimalno potezo, nato pa poskrbi, da se poteza izvede.

- minimax.py
	Algoritem za izračun najboljše poteze s pomočjo minimiziranja in maksimiziranja izračunanih potez.

- alphabeta.py
	Nadgrajeni algoritem minimax z alfa beta rezi in povečano globino.



