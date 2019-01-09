import math

#I need to have this section broken down into different functions and have several sets of logic gates.

global x_1
global y_1
global x_2
global y_2
global i_2
global j_2
global t
global origin_x
global origin_y
global VEC_1x
global VEC_1y
global VEC_2x
global VEC_2y
global dotprod
global mag_1
global mag_2
global radians
global mag_mult
global words

def G2_G3_values(i):
    global x_2
    global y_2
    global i_2
    global j_2

    x_2 = float(words[2])
    y_2 = float(words[4])
    i_2 = float(words[6])
    j_2 = float(words[8])

def origin_xy(x_1, y_1, i_2, y_2):
    global origin_x
    global origin_y
    origin_x = x_1 + i_2
    origin_y = y_1 + y_2


def vectors(x_1, y_1, x_2, y_2, origin_x, origin_y):
    global VEC_1x
    global VEC_1y
    global VEC_2x
    global VEC_2y
    VEC_1x = origin_x - x_1
    VEC_1y = origin_y - y_1
    VEC_2x = origin_x - x_2
    VEC_2y = origin_y - y_2


def dot(VEC_1x, VEC_2x, VEC_1y, VEC_2y):
    global  dotprod
    dotprod = (VEC_1x * VEC_2x) + (VEC_1y * VEC_2y)


def magnitude(VEC_1x,VEC_1y, VEC_2x, VEC_2y):
    global mag_1
    global mag_2
    mag_1 = math.sqrt((VEC_1x**2) + (VEC_2x**2))
    mag_2 = math.sqrt((VEC_2x**2) + (VEC_2y**2))


def multi_mag(mag_1, mag_2):
    global mag_mult
    mag_mult = mag_1 * mag_2


def rads(dotprod, mag_mult):
    global radians
    radians = math.acos(dotprod / mag_mult)


def g_eval(f,data):
    # this is a list of initialized values of the global variables.
    '''x_1 = 0.0
    y_1 = 0.0
    x_2 = 0.0
    y_2 = 0.0
    i_2 = 0.0
    j_2 = 0.0
    t = 0
    origin_x = 0.0
    origin_y = 0.0
    VEC_1x = 0.0
    VEC_1y = 0.0
    VEC_2x = 0.0
    VEC_2y = 0.0
    mag_1 = 0.0
    mag_2 = 0.0
    dotprod = 0.0
    mag_mult = 0.0'''

    flag = 0
    #for loop ensures that each line is read in the g-code file
    for i in data:
        global words
        words = i.split()

        # this is a logic gate that will pass each line until that start of true G-code
        if flag != 1:
            if i =="\n":
                f.write(str(i))
            else:
                if words[0] == "(*" and words[1] == "SHAPE":
                    f.write(str(i))
                    flag = 1
                else:
                    f.write(str(i))
        else:
            #here is where the for loop should go into a class that will process and evaluate the
            if words[0] == "G0":
                f.write(str(i))
                if words[1] == "X":

                    #saving values into float values for evaluation later on
                    x_1 = words[2]
                    y_1 = words[4]



            # this section of code looks for G2 and should look for G3 which are arc commands and identifies each
            # section of the G-code and pulls out the X ,Y, I, J and turns them into float.
            # At the start of the G-code file is a G20 command which needs to be vetted out.
            if words[0] == "G2" or words[0] == "G3":

                #This is a catch incase G20 or G21 is in the G-code lines
                if words[0] != "G20" and words[0] != "G21":

                    #this evaluates the string of i and Identifies x,y,i,j and returns them.
                    G2_G3_values(i)

                    #this function identifies the starting point of the arc
                    origin_xy(x_1,y_1,i_2,y_2)

                    #vectors are created from each line
                    vectors(x_1, y_1, x_2, y_2, origin_x, origin_y)

                    #Here is the dot product being solved
                    dot(VEC_1x, VEC_2x, VEC_1y, VEC_2y)

                    #the magnetude of both vectors is being evaluated
                    magnitude(VEC_1x,VEC_1y, VEC_2x, VEC_2y)

                    # finally the magnitudes are multiplyed
                    multi_mag(mag_1,mag_2)

                    #this equation gives the angle in radians between our two lines
                    rads(dotprod, mag_mult)

    # this should be a function
                    #if the arc command G3 then the theta value needs to be subtracted
                    if words[0] == "G3":

                    # I am converting the radians into degrees
                        theta = -math.degrees(radians)
                    else:
                    #I am converting the radians into degrees
                        theta = math.degrees(radians)

    #this should be its own function
                    #last step in this process is to add the line "C XXX.XXX" which will be the degrees of rotation of the C axis
                    f.write( str(i[:-1]) + "  C " + str("%.3f" % round(theta,3)) +  "\r\n")

                #this section of code takes the end point and makes it the new starting point.
                #the t == 1 flag insures that this part is only entered into if a second point is defined.
                else:
                    f.write(str(i))
                x_1 = float(words[2])
                y_1 = float(words[4])


    #this catch all should go away with the use of a flag from earlier in the process
            #here is a catch all of G-codes and line of text that dont meet any other forms of evaluation.
            else:
                f.write(str(i))
