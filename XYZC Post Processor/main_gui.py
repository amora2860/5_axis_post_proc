import math
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
import calc


# this is a list of all the global variables used.
global listG0
global listG2
global x_1
global y_1
global x_2
global y_2
global i_2
global j_2
global t
global origin_x
global origin_y




#There must be functions added to this file so that there is some organization
#Several things to need be evaluated
# 1 If there needs to be an initial start rotation of the C axis
# 2 line to line rotation of the C axis



class MyFrame(Frame):

    def __init__(self):

        Frame.__init__(self)
        self.master.title("XYZC Post processor")
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





    #when close button is clicked the program is end
    def close_window(self):
        MyFrame.quit(self)

    #This a functiont that allows the selection of a file to be loaded for processing
    def load_file(self):

        #Brings up file browser with only these options for file selection and saves the extension to fname
        fname = askopenfilename(filetypes=(("G-code files", "*.ngc"),
                                           ("All files", "*.*"),
                                           ("Text files", "*.txt")))

        #This opens up fname and makes it readable.
        fname_file = open(fname, 'r')

        #Reads in fname_file and saves it into data as a list of strings
        data = fname_file.readlines()

        # this takes the string and separates it by each "/"
        fname_list = fname.split("/")

        # I need to take fname_list and have its[-1] split to exclude the rest and only have the file name.
        word = fname_list[-1]

        #This finally removed everything and only provides the file name.
        file_name = word[:-4]


        #  this creates a new file and ensures its name is the name of the selected one with _postproc.ngc at the end.
        f = open('{0}.ngc'.format(file_name + "_postproc"), "w")

        #function for evalauting G-code lines and calculations
        calc.g_eval(f,data)

        # A Button will appear to indicate that the G-code processing has been completed
        self.complete = Button(self, text="Process is complete \n (CLICK TO CLOSE) ", command=self.close_window, bg = "red")

        self.complete.place(x=15, y=5)




        # if there is an error if the open file an error will be presented
        if fname:
            try:
                fname_file.close()
                f.close()
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
