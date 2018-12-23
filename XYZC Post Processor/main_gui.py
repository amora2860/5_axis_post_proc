from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
import math
from tkinter import messagebox #used for the message box

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
# 2 to to line rotation of the C axis



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
        g_eval(f,data)

        # A message box will appear to indicate that the G-code processing has been completed

        #this is being done wrong it needs to be apart of the main gui but still be brought up
        top = Tk()
        top.geometry("200x200")

        def hello():
            messagebox.showinfo("XYZC Post Processor", "Process Complete")

        B1 = Button(top, text="Ok", command= quit(hello()))
        B1.place(x=35, y=50)

        top.mainloop()



        # if there is an error if the open file an error will be presented
        if fname:
            try:
                fname_file.close()
                f.close()
            except:  # <- naked except is a bad idea
                showerror("Open Source File", "Failed to read file\n'%s'" % fname)
            return

        return data




#I need to have this section broken down into different functions and have several sets of logic gates.

def g_eval(f,data):
    # this is a list of initialized values of the global variables.
    x_1 = 0.0
    y_1 = 0.0
    x_2 = 0.0
    y_2 = 0.0
    i_2 = 0.0
    j_2 = 0.0
    listG2 = []
    listG0 = [0, 0, 0]
    t = 0


    #for loop ensures that each line is read in the g-code file
    for i in data:

        #here is where the for loop should go into a class that will process and evaluate the
        if i[0:2] == "G0":
            f.write(str(i))
            if i[3:4] == "X":
                #set flag
                t = 1
                #seperate line into smaller pieces of values
                listG0 = [str(i[0:2]), str(i[6:11]), str(i[15:21])]

                #saving values into float values for evaluation later on
                x_1 = float(listG0[1])
                y_1 = float(listG0[2])



        # this section of code looks for G2 and should look for G3 which are arc commands and identifies each
        # section of the G-code and pulls out the X ,Y, I, J and turns them into float.
        # At the start of the G-code file is a G20 command which needs to be vetted out.
        if i[0:2] == "G2" or i[0:2] == "G3":

            if i[0:3] != "G20" and i[0:3] != "G21":

                listG2 = [str(i[0:2]), str(i[6:11]), str(i[15:21]), str(i[24:30]), str(i[34:341])]

                x_2 = float(listG2[1])
                y_2 = float(listG2[2])
                i_2 = float(listG2[3])
                j_2 = float(listG2[4])
                origin_x = x_1 + i_2
                origin_y = y_1 + j_2

                #This short section of VEC creates the vectors of each line
                VEC_1x = origin_x - x_1
                VEC_1y = origin_y - y_1
                VEC_2x = origin_x - x_2
                VEC_2y = origin_y - y_2

                #Here is the dot product being solved for
                dot = (VEC_1x * VEC_2x) + (VEC_1y * VEC_2y)

                #the magnetude of both vectors is being evaluated
                mag_1 = math.sqrt((VEC_1x**2) + (VEC_2x**2))
                mag_2 = math.sqrt((VEC_2x**2) + (VEC_2y**2))

                #finally the magnitudes are multiplyed
                mag_mult = mag_1 * mag_2

                #this equation gives the angle in radians between our two lines
                radians = math.acos(dot/mag_mult)

                #if the arc command G3 then the theta value needs to be subtracted
                if i[0:2] == "G3":
                # I am converting the radians into degrees
                    theta = -math.degrees(radians)
                else:
                #I am converting the radians into degrees
                    theta = math.degrees(radians)


                #last step in this process is to add the line "C XXX.XXX" which will be the degrees of rotation of the C axis
                f.write( str(i[:-1]) + "  C " + str("%.3f" % round(theta,3)) +  "\r\n")

            #this section of code takes the end point and makes it the new starting point.
            #the t == 1 flag insures that this part is only entered into if a second point is defined.
            else:
                f.write(str(i))
            if t == 1:
                x_1 = float(listG2[1])
                y_1 = float(listG2[2])



        #here is a catch all of G-codes and line of text that dont meet any other forms of evaluation.
        else:
            if i[0:2] != "G0":
                f.write(str(i))














def main():

    root = Tk()
    ex = MyFrame()

    root.mainloop()
if __name__ == '__main__':
    main()