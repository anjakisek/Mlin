from tkinter import *
velikost_plosce = 400
velikost_polja = 6
class Gui():

    def __init__(self, master):
        #ce se zapre okno
        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))

        #igralna plosca
        self.plosca = Canvas(master, width = velikost_plosce, height = velikost_plosce)
        self.plosca.pack()

        ##############################################
        #ustvarim 24 pik/polj
        polje1 = self.plosca.create_oval(velikost_plosce/8 - velikost_polja,
                                         velikost_plosce/8 - velikost_polja,
                                         velikost_plosce/8 + velikost_polja,
                                         velikost_plosce/8 + velikost_polja)
        polje2 = self.plosca.create_oval(velikost_plosce/2 - velikost_polja,
                                         velikost_plosce/8 - velikost_polja,
                                         velikost_plosce/2 + velikost_polja,
                                         velikost_plosce/8 + velikost_polja)
        polje3 = self.plosca.create_oval(7 * velikost_plosce/8 - velikost_polja,
                                             velikost_plosce/8 - velikost_polja,
                                         7 * velikost_plosce/8 + velikost_polja,
                                             velikost_plosce/8 + velikost_polja)
        polje4 = self.plosca.create_oval(velikost_plosce/4 - velikost_polja,
                                         velikost_plosce/4 - velikost_polja,
                                         velikost_plosce/4 + velikost_polja,
                                         velikost_plosce/4 + velikost_polja)
        polje5 = self.plosca.create_oval(velikost_plosce/2 - velikost_polja,
                                         velikost_plosce/4 - velikost_polja,
                                         velikost_plosce/2 + velikost_polja,
                                         velikost_plosce/4 + velikost_polja)
        polje6 = self.plosca.create_oval(3 * velikost_plosce/4 - velikost_polja,
                                             velikost_plosce/4 - velikost_polja,
                                         3 * velikost_plosce/4 + velikost_polja,
                                             velikost_plosce/4 + velikost_polja)
        polje7 = self.plosca.create_oval(3 * velikost_plosce/8 - velikost_polja,
                                         3 * velikost_plosce/8 - velikost_polja,
                                         3 * velikost_plosce/8 + velikost_polja,
                                         3 * velikost_plosce/8 + velikost_polja)
        polje8 = self.plosca.create_oval(    velikost_plosce/2 - velikost_polja,
                                         3 * velikost_plosce/8 - velikost_polja,
                                             velikost_plosce/2 + velikost_polja,
                                         3 * velikost_plosce/8 + velikost_polja)
        polje9 = self.plosca.create_oval(5 * velikost_plosce/8 - velikost_polja,
                                        3 * velikost_plosce/8 - velikost_polja,
                                        5 * velikost_plosce/8 + velikost_polja,
                                        3 * velikost_plosce/8 + velikost_polja)
        polje10 = self.plosca.create_oval(velikost_plosce/8 - velikost_polja,
                                          velikost_plosce/2 - velikost_polja,
                                          velikost_plosce/8 + velikost_polja,
                                          velikost_plosce/2 + velikost_polja)
        polje11 = self.plosca.create_oval(velikost_plosce/4 - velikost_polja,
                                          velikost_plosce/2 - velikost_polja,
                                          velikost_plosce/4 + velikost_polja,
                                          velikost_plosce/2 + velikost_polja)
        polje12 = self.plosca.create_oval(3 * velikost_plosce/8 - velikost_polja,
                                              velikost_plosce/2 - velikost_polja,
                                          3 * velikost_plosce/8 + velikost_polja,
                                              velikost_plosce/2 + velikost_polja)
        polje13 = self.plosca.create_oval(5 * velikost_plosce/8 - velikost_polja,
                                              velikost_plosce/2 - velikost_polja,
                                          5 * velikost_plosce/8 + velikost_polja,
                                              velikost_plosce/2 + velikost_polja)
        polje14 = self.plosca.create_oval(3 * velikost_plosce/4 - velikost_polja,
                                              velikost_plosce/2 - velikost_polja,
                                          3 * velikost_plosce/4 + velikost_polja,
                                              velikost_plosce/2 + velikost_polja)
        polje15 = self.plosca.create_oval(7 * velikost_plosce/8 - velikost_polja,
                                              velikost_plosce/2 - velikost_polja,
                                          7 * velikost_plosce/8 + velikost_polja,
                                              velikost_plosce/2 + velikost_polja)
        polje16 = self.plosca.create_oval(3 * velikost_plosce/8 - velikost_polja,
                                          5 * velikost_plosce/8 - velikost_polja,
                                          3 * velikost_plosce/8 + velikost_polja,
                                          5 * velikost_plosce/8 + velikost_polja)
        polje17 = self.plosca.create_oval(    velikost_plosce/2 - velikost_polja,
                                          5 * velikost_plosce/8 - velikost_polja,
                                              velikost_plosce/2 + velikost_polja,
                                          5 * velikost_plosce/8 + velikost_polja)
        polje18 = self.plosca.create_oval(5 * velikost_plosce/8 - velikost_polja,
                                          5 * velikost_plosce/8 - velikost_polja,
                                          5 * velikost_plosce/8 + velikost_polja,
                                          5 * velikost_plosce/8 + velikost_polja)
        polje19 = self.plosca.create_oval(velikost_plosce/4 - velikost_polja,
                                         3 * velikost_plosce/4 - velikost_polja,
                                         velikost_plosce/4 + velikost_polja,
                                         3 * velikost_plosce/4 + velikost_polja)
        
        polje20 = self.plosca.create_oval(velikost_plosce/2 - velikost_polja,
                                         3 * velikost_plosce/4 - velikost_polja,
                                         velikost_plosce/2 + velikost_polja,
                                         3 * velikost_plosce/4 + velikost_polja)
        
        polje21 = self.plosca.create_oval(3 * velikost_plosce/4 - velikost_polja,
                                          3 * velikost_plosce/4 - velikost_polja,
                                          3 * velikost_plosce/4 + velikost_polja,
                                          3 * velikost_plosce/4 + velikost_polja)
        
        polje22 = self.plosca.create_oval(velikost_plosce/8 - velikost_polja,
                                          7 *velikost_plosce/8 - velikost_polja,
                                          velikost_plosce/8 + velikost_polja,
                                          7 * velikost_plosce/8 + velikost_polja)
        
        polje23 = self.plosca.create_oval(velikost_plosce/2 - velikost_polja,
                                          7 * velikost_plosce/8 - velikost_polja,
                                          velikost_plosce/2 + velikost_polja,
                                          7 *velikost_plosce/8 + velikost_polja)
        
        polje24 = self.plosca.create_oval(7 * velikost_plosce/8 - velikost_polja,
                                          7 *velikost_plosce/8 - velikost_polja,
                                          7 * velikost_plosce/8 + velikost_polja,
                                          7 * velikost_plosce/8 + velikost_polja)

        self.plosca.create_rectangle(velikost_plosce/8,
                                     velikost_plosce/8,
                                 7 * velikost_plosce/8,
                                 7 * velikost_plosce/8)

        self.plosca.create_rectangle(velikost_plosce/4,
                                     velikost_plosce/4,
                                 3 * velikost_plosce/4,
                                 3 * velikost_plosce/4)
        
        self.plosca.create_rectangle(3 * velikost_plosce/8,
                                     3 * velikost_plosce/8,
                                     5 * velikost_plosce/8,
                                     5 * velikost_plosce/8)

        self.plosca.create_line(velikost_plosce/2, velikost_plosce/8,velikost_plosce/2,
                                3 * velikost_plosce/8)

        self.plosca.create_line(velikost_plosce/2, 5 * velikost_plosce/8,velikost_plosce/2,
                                7 * velikost_plosce/8)

        self.plosca.create_line(velikost_plosce/8, velikost_plosce/2,3 * velikost_plosce/8,
                                velikost_plosce/2)

        self.plosca.create_line(5 * velikost_plosce/8, velikost_plosce/2,7 * velikost_plosce/8,
                                velikost_plosce/2)
        
                                         
        




    def zapri_okno(self, master):
        self.prekini_igralce()
        master.destroy()
        
    def prekini_igralce(self):
        #TODO
        pass





root = Tk()
root.title("Mlin")
aplikacija = Gui(root)
root.mainloop()
