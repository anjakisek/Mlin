from tkinter import *
velikost_plosce = 400
velikost_polja = 6
class Gui():

    def __init__(self, master):
        #ce se zapre okno
        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))

        self.stevec1 = IntVar(master, value=9)
        
        Label(master, text= "Preostale: {}".format(self.stevec1.get())).grid(row=0, column=0)

        self.stevec2 = IntVar(master, value=9)
        Label(master, text= "Preostale: {}".format(self.stevec2.get())).grid(row=2, column=0)
        
        #igralna plosca
        self.plosca = Canvas(master, width = velikost_plosce, height = velikost_plosce)
        self.plosca.grid(row=1, column=0)

        ##############################################
        #ustvarim 24 pik/polj
        for i in range(0, 3):
            for k in range(0, 2):
                self.plosca.create_oval(velikost_plosce * (1/8 + i * 3/8) - velikost_polja,
                                        velikost_plosce * (1/8 + k * 3/4) - velikost_polja,
                                        velikost_plosce *(1/8 + i * 3/8) + velikost_polja,
                                        velikost_plosce * (1/8 + k * 3/4) + velikost_polja)
        for i in range(0, 3):
            for k in range(0, 2):
                self.plosca.create_oval(velikost_plosce * (1/4 + i/4) - velikost_polja,
                                        velikost_plosce * (1/4 + k/2) - velikost_polja,
                                        velikost_plosce * (1/4 + i/4) + velikost_polja,
                                        velikost_plosce * (1/4 + k/2) + velikost_polja)

        for i in range(0, 3):
            for k in range(0,2):
                self.plosca.create_oval(velikost_plosce * (3/8 + i/8) - velikost_polja,
                                        velikost_plosce * (3/8 + k/4) - velikost_polja,
                                        velikost_plosce * (3/8 + i/8) + velikost_polja,
                                        velikost_plosce * (3/8 + k/4) + velikost_polja)

        for i in range(0, 3):
            for k in range(0,2):
                self.plosca.create_oval(velikost_plosce * (1/8 + i/8 + k/2) - velikost_polja,
                                          velikost_plosce/2 - velikost_polja,
                                          velikost_plosce * (1/8 + i/8 + k/2) + velikost_polja,
                                          velikost_plosce/2 + velikost_polja)
        
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
