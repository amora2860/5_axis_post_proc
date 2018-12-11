from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from tkinter import Scrollbar as tkScrollBar
import io
#from calc import calc
import configparser

global flag


class MyFrame(Frame):

    def __init__(self):

        Frame.__init__(self)
        self.master.title("C Axis Post processor")
        self.master.rowconfigure(500, weight=1)
        self.master.columnconfigure(500, weight=1)
        self.grid(sticky=W+E+N+S)


        #browse button needed to find text file and hopefully with an event it will show the files contents in
        # the canvas
        self.button = Button(self, text="Browse", command = self.load_file, width=20)
        self.button.grid(row=1, column=0, sticky=N)

        #this is a program close button
        self.close_button = Button(self, text="Close", command=self.close_window, width=20)
        self.close_button.grid(row=2, column=0, sticky=N)

        #setting up a canvas to house the text for the text file
        self.canvas = Canvas(self, width=500, height=200, background='white')
        self.canvas.grid(row=1,column=3)


    #when close button is clicked the program is end
    def close_window(self):
        MyFrame.quit(self)

    #This a functiont that
    def load_file(self):

        fname = askopenfilename(filetypes=(("Text files", "*.txt"),
                                           ("All files", "*.*")))
        fname_file = open(fname, 'r')
        data = fname_file.readlines()
        self.canvas.create_text(100, 0, text=data, anchor=N)
        #This line will call for the calc.py file and have it run the loaded G-code file and
        #calc.run(data)

        #this section is nice in that it takes each line of the G-code file and stores
        #it into a dictionary which has a list that is labeled per each line.
        dct = {}
        n = 0
        for i in data:
            dct['list_%s' % n] = [data[n]]
            n = n + 1







            #skip the first 14 lines of the text file
            #if the first three characters are equal to G02 or Go3 then and arc is taking place
            # G02 is a clockwise arc
            #G03 is a counterclockwise arc
            # X and Y is the ending position.
            # I and J is the distance from start point to the center point
            #G2 X  3.354 Y  3.354 I  0.354 J  0.354
            #we know the start point from the previous line

        # setting up a canvas to house the text for the text file
        self.canvas2 = Canvas(self, width=500, height=200, background='white')
        self.canvas2.grid(row=2, column=3)

        # how to have this file added to the canvas after it is selected.
        if fname:
            try:
                fname_file.close()
            except:  # <- naked except is a bad idea
                showerror("Open Source File", "Failed to read file\n'%s'" % fname)
            return

        return data



def main():

    root = Tk()
    ex = MyFrame()

    root.mainloop()
if __name__ == '__main__':
    main()