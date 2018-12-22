from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
import math

#There must be functions added to this file so that there is some organization

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




#I need to have this section broken down into different functions and have several sets of logic gates.


        #this is a list of all the global variables used.
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

        #this is a list of initialized values of the global variables.
        x_1 = 0.0
        y_1 = 0.0
        x_2 = 0.0
        y_2 = 0.0
        i_2 = 0.0
        j_2 = 0.0
        listG2 = []
        listG0 = [0,0,0]
        t = 0

        #for loop ensures that each line is read in the g-code file
        for i in data:

            #list2 will be evaluated
            list2 = i

            #here is where the for loop should go into a class that will process and evaluate the
            if list2[0:2] == "G0":
                f.write(str(i))
                if list2[3:4] == "X":
                    print("This is the beginning start point.")
                    t = 1
                    listG0 = [str(list2[0:2]), str(list2[6:11]), str(list2[15:21])]
                    print("X1 " + str(listG0[1]) + " Y1 " + str(listG0[2]))
                    x_1 = float(listG0[1])
                    y_1 = float(listG0[2])



            # this section of code looks for G2 and should look for G3 which are arc commands and identifies each
            # section of the G-code and pulls out the X ,Y, I, J and turns them into float.
            # At the start of the G-code file is a G20 command which needs to be vetted out.
            if list2[0:2] == "G2":

                if list2[0:3] != "G20" and list2[0:3] != "G21":

                    listG2 = [str(list2[0:2]), str(list2[6:11]), str(list2[15:21]), str(list2[24:30]), str(list2[34:341])]

                    x_2 = float(listG2[1])
                    y_2 = float(listG2[2])
                    i_2 = float(listG2[3])
                    j_2 = float(listG2[4])
                    origin_x = x_1 + i_2
                    origin_y = y_1 + j_2

                    #this section of printing is purely for testing purposes and should be removed with final release
                    #print("The start point of the arc is (X " + str(x_1) + " Y " + str(y_1) + ")")
                    #print("The end point is (X " + str(x_2) + " Y " + str(y_2) + ")")
                    #print("The center of the arc is X " + str(origin_x) + " Y " + str(origin_y))
                    #print("x_1 " + str(x_1))
                    #print("y_1 " + str(y_1))
                    #print("origin x " + str(origin_x))
                    #print("origin y " + str(origin_y))

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

                    #I am converting the radians into degrees
                    theta = math.degrees(radians)

                    ##this section of printing is purely for testing purposes and should be removed with final release
                    #print("VEC_1x " + str(VEC_1x))
                    #print("VEC_1y " + str(VEC_1y))
                    #print("VEC_2x " + str(VEC_2x))
                    #print("VEC_2y " + str(VEC_2y))
                    #print("dot " + str(dot))
                    #print("mag_1 " + str(mag_1) + " mag_2 " + str(mag_2) + " mag_multi " + str(mag_mult))
                    #print("The radians are " + str(radians))
                    #print("The angle is " + str(theta))


                    #last step in this process is to add the line "C XXX.XXX" which will be the degrees of rotation of the C axis
                    f.write( str(list2[:-1]) + "  C " + str("%.3f" % round(theta,3)) +  "\r\n")

                #this section of code takes the second point and pushes to be the new starting point.
                #the t == 1 flag insures that this part is only entered into if a second point is defined.
                else:
                    f.write(str(i))
                if t == 1:
                    x_1 = float(listG2[1])
                    y_1 = float(listG2[2])
                    print(" This is the new starting point. " + "(X " + str(x_1) + " Y " +str(y_1)+ ")")


            #here is where the line for writing each line of code to a new folder and adding the C rotation
            else:
                print(i)
                if list2[0:2] != "G0":
                    f.write(str(i))










        # how to have this file added to the canvas after it is selected.
        if fname:
            try:
                fname_file.close()
                #f.close()
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