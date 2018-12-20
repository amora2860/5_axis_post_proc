from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
import math

#There must be functions added to this file so that there is some organization

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

        # this takes the string and seperates it by each "/"
        fname_list = fname.split("/")

        # I need to take fname_list and have its[-1] split to exclude the rest and only have the file name.
        word = fname_list[-1]

        #This finally removed everything and only provides the file name.
        file_name = word[:-4]


        #  this creates a new file and ensures its name is
        f = open('{0}.txt'.format(file_name + "_postproc"), "w")

        self.canvas.create_text(100, 0, text=data, anchor=N)
        #This line will call for the calc.py file and have it run the loaded G-code file and
        #calc.run(data)


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
        n = 0 # this is a flag for G0 to ensure that it the starting point is captured
        t = 0

        for i in data:

            list2 = i

            #here is where the for loop should go into a class that will process and evaluate the
            #string and look at the next ones.
            if n == 0:
                if list2[0:2] == "G0":
                    if list2[3:4] == "X":
                        print("This is the beginning start point.")
                        t = 1
                        listG0 = [str(list2[0:2]), str(list2[6:11]), str(list2[15:21])]
                        print("X1 " + str(listG0[1]) + " Y1 " + str(listG0[2]))
                        x_1 = float(listG0[1])
                        y_1 = float(listG0[2])
                        n = 1
                        f.write( str(i) + "\r\n")

            # this section of code looks for G2 which is the arc command and identifies each
            # section of the G-code and pulls out the X ,Y, I, J and turns them into float.
            # At the start of the G-code file is a G20 command which needs to be vetted out.
            if list2[0:2] == "G2":

                if list2[0:3] != "G20":

                    listG2 = [str(list2[0:2]), str(list2[6:11]), str(list2[15:21]), str(list2[23:30]), str(list2[32:39])]

                    x_2 = float(listG2[1])
                    y_2 = float(listG2[2])
                    i_2 = float(listG2[3])
                    j_2 = float(listG2[4])
                    origin_x = x_1 + i_2
                    origin_y = y_1 + j_2

                    #this section of printing is purely for testing purposes and should be removed with final release
                    print("The start point of the arc is (X " + str(x_1) + " Y " + str(y_1) + ")")
                    print("The end point is (X " + str(x_2) + " Y " + str(y_2) + ")")
                    print("The center of the arc is X " + str(origin_x) + " Y " + str(origin_y))
                    print("x_1 " + str(x_1))
                    print("y_1 " + str(y_1))
                    print("origin x " + str(origin_x))
                    print("origin y " + str(origin_y))

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
                    print("VEC_1x " + str(VEC_1x))
                    print("VEC_1y " + str(VEC_1y))
                    print("VEC_2x " + str(VEC_2x))
                    print("VEC_2y " + str(VEC_2y))
                    print("dot " + str(dot))
                    print("mag_1 " + str(mag_1) + " mag_2 " + str(mag_2) + " mag_multi " + str(mag_mult))
                    print("The radians are " + str(radians))
                    print("The angle is " + str(theta))

                    #last step in this process is to add the line "C XXX.XXX" which will be the degrees of rotation of the C axis
                    f.write( str(i) + "  C " + str(theta) +  "\r\n")

                #this section of code takes the second point and pushes to be the new starting point.
                #the t == 1 flag insures that this part is only entered into if a second point is defined.
                if t == 1 :
                    x_1 = float(listG2[1])
                    y_1 = float(listG2[2])
                    print(" This is the new starting point. " + "(X " + str(x_1) + " Y " +str(y_1)+ ")")


            #here is where the line for writing each line of code to a new folder and adding the C rotation
            f.write(str(i) + "\r\n")








        # setting up a canvas to house the text for the text file
        self.canvas2 = Canvas(self, width=500, height=200, background='white')
        self.canvas2.grid(row=2, column=3)

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