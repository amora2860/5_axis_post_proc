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
global VEC_0x
global VEC_0y
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
global C_arc
global theta
global G_code

# this is a list of initialized values of the global variables.
x_0 = 0.0
y_0 = 1.0

C = 0.0
theta = 0.0

flag_1 = 0
flag_2 = 0


def G2_G3_values(i):
    global x_2
    global y_2
    global i_2
    global j_2

    words = i.split()
    x_2 = float(words[2])
    y_2 = float(words[4])
    i_2 = float(words[6])
    j_2 = float(words[8])

def G0_G1_values(i):
    global x_2
    global y_2
    words = i.split()
    x_2 = float(words[2])
    y_2 = float(words[4])

def origin_xy(x_1, y_1, i_2, y_2):
    global origin_x
    global origin_y
    origin_x = x_1 + i_2
    origin_y = y_1 + y_2

def vectors_G2_G3(x_1, y_1, x_2, y_2, origin_x, origin_y):
    global VEC_1x
    global VEC_1y
    global VEC_2x
    global VEC_2y
    VEC_1x = origin_x - x_1
    VEC_1y = origin_y - y_1
    VEC_2x = origin_x - x_2
    VEC_2y = origin_y - y_2

def vectors_G0_G1(x_0, y_0,x_1, y_1, x_2, y_2):
    global VEC_1x
    global VEC_1y
    global VEC_2x
    global VEC_2y
    VEC_1x = x_0 - x_1
    VEC_1y = y_0 - y_1
    VEC_2x = x_2 - x_1
    VEC_2y = y_2 - y_1


def dot(VEC_1x, VEC_2x, VEC_1y, VEC_2y):
    global  dotprod
    dotprod = (VEC_1x * VEC_2x) + (VEC_1y * VEC_2y)


def magnitude(VEC_1x,VEC_1y, VEC_2x, VEC_2y):
    global mag_1
    global mag_2
    mag_1 = math.sqrt((VEC_1x**2) + (VEC_1y**2))
    mag_2 = math.sqrt((VEC_2x**2) + (VEC_2y**2))


def multi_mag(mag_1, mag_2):
    global mag_mult
    mag_mult = mag_1 * mag_2

# this equation gives the angle in radians between our two lines
def rads(dotprod, mag_mult):
    global radians
    radians = math.acos(dotprod / mag_mult)

#THIS NEEDS TO EVALUATE THE SIDE REGARDLESS OF WHETHER THE LINE IS GOING DOWN OR UP IN THE Y AXIS.
#THIS CAN FLIP THE SIDE IT IS ON
def line_eval_G0_G1(x_1, y_1, x_2, y_2):
    global cord

    # what coordinate system is each line in
    if x_1 == x_2:
        cord = "none_0"

    elif y_1 == y_2:
        cord = "none_90"

    elif x_2 > x_1:
        cord = "right_side"

    elif x_2 < x_1:
        cord = "left_side"

#this needs to be oriented towards evaluating the center point
def line_eval_G2_G3(x_1, y_1, origin_x, origin_y):
    global C
    global cord

    if x_1 == origin_x:
        cord = "none_0"

    if y_1 == origin_y:
        cord = "none_90"

    if x_2 > x_1:
        cord = "right_side"

    if x_2 < x_1:
        cord = "left_side"


# This function gets the smallest angle between two vectors.
# Then dending on if it is the right side or left relative to the C axis which facing (0,1) or at 0 deg is the origin.

def cord_angle_calc(dotprod, mag_mult):
    global C
    global cord
    if cord == "none_0":
        C = 0

    if cord == "none_90":
        C = 90

    if cord == "right_side":
        rads(dotprod, mag_mult)
        theta = math.degrees(radians)

        C = theta

    if cord == "left_side":
        rads(dotprod, mag_mult)
        theta = math.degrees(radians)
        C = 360 - theta

#this gives the orientation of C to every point that is evaluated
def C_line(x_1, y_1):
    global  x_0
    global  y_0

    x_0 = x_1
    y_0 = y_1 + 1

# this function finds what cordinate that point 1 and point 2 are in.
def arc_cords_p1(x_1, y_1, origin_x, origin_y):
    global cord_p1

    # is point #1 on the left side of the origin
    if x_1 < origin_x:
        # x_1 is either cord 3 or 4

        #checking whether point #1 is in cord 4
        if y_1 < origin_y:
            # point #1 is in cord 4
            cord_p1 = "4"
        elif y_1 > origin_y:
            # point #1 is in cord 3
            cord_p1 = "3"
        elif y_1 == origin_y:
            cord_p1 = "3&4"
    # is point #1 on the right side of the origin
    elif x_1 > origin_x:
        # x_1 is either cord 1 or 2

        # checking whether point #1 is in cord 1
        if y_1 < origin_y:
        # point #1 is in cord 1
            cord_p1 = "1"
        elif y_1 > origin_y:
        # point #1 is in cord 2
            cord_p1 = "2"
        elif y_1 == origin_y:
            cord_p1 = "1&2"
    #special senario where x_1 or y_1 is equal to the origin
    # is point #1 equal to the origin_x
    elif x_1 == origin_x:
        #the point is between (2 and  3) or ( 1 and 4)
        if y_1 < origin_y:
            # point 1 is on (1 and 4) line
            cord_p1 = "1&4"
        else:
            # point 1 is on (2 and 3) line
            cord_p1 = "2&3"
    return cord_p1

# this function finds what cordinate that point 1 and point 2 are in.
def arc_cords_p2(x_2, y_2, origin_x, origin_y):
    global cord_p2

 # is point #2 on the left side of the origin
    if x_2 < origin_x:
        # x_2 is either cord 3 or 4

        #checking whether point #2 is in cord 4
        if y_2 < origin_y:
            # point #2 is in cord 4
            cord_p2 = "4"
        elif y_2 > origin_y:
            # point #2 is in cord 3
            cord_p2 = "3"
        elif y_2 == origin_y:
            cord_p2 = "3&4"
    # is point #2 on the right side of the origin
    elif x_2 > origin_x:
        # x_2 is either cord 1 or 2

        # checking whether point #2 is in cord 1
        if y_2 < origin_y:
        # point #2 is in cord 1
            cord_p2 = "1"
        elif y_2 > origin_y:
        # point #2 is in cord 2
            cord_p2 = "2"
        elif y_2 == origin_y:
            cord_p2 = "1&2"
    #special senario where x_2 or y_2 is equal to the origin
    # is point #2 equal to the origin_x
    elif x_2 == origin_x:
        #the point is between (2 and  3) or ( 1 and 4)
        if y_2 < origin_y:
            # point 2 is on (1 and 4) line
            cord_p2 = "1&4"
        else:
            # point 2 is on (2 and 3) line
            cord_p2 = "2&3"
    return cord_p2

def eval1_theta():
    print("eval1_theta")

def eval2_theta():
    print("eval2_theta")

# this function is meant to evaluate how the vector angle should be altered.
def arc_comp (cord_p1, cord_p2):
    global theta
    global G_code

    if cord_p1 == "1":
        if cord_p2 == "1":
            #this theta will have to tell if point_1 is to the right or left of point 2
            eval2_theta()

        elif cord_p2 == "2" or cord_p2 == "1&2" or cord_p2 == "2&3":
            if G_code == "G2":
                C = 360 - theta

            elif G_code == "G3":
                C = theta

        elif cord_p2 == "3":
            eval1_theta()

        elif cord_p2 == "4" or cord_p2 == "3&4" or cord_p2 == "4&1":
            if G_code == "G3":
                C = 360 - theta

            elif G_code == "G2":
                C = theta


    if cord_p1 == "2":
        if cord_p2 == "1" or cord_p2 == "1&2" or cord_p2 == "4&1":
            # this theta will have to tell if point_1 is to the right or left of point 2
            if G_code == "G2":
                C = theta

            elif G_code == "G3":
                C = 360 - theta

        elif cord_p2 == "2":
            eval2_theta()

        elif cord_p2 == "3" or cord_p2 == "2&3" or cord_p2 == "3&4":
            if G_code == "G2":
                C = 360 - theta

            elif G_code == "G3":
                C = theta
                
        elif cord_p2 == "4":
            eval1_theta()

    if cord_p1 == "3":
        if cord_p2 == "1":
            # this theta will have to tell if point_1 is to the right or left of point 2
            eval1_theta()
        
        elif cord_p2 == "2" or cord_p2 == "1&2" or cord_p2 == "2&3":
            if G_code == "G2":
                C = theta
            elif G_code == "G3":
                C = 360 - theta

        elif cord_p2 == "3":
            eval2_theta()

        elif cord_p2 == "4" or cord_p2 == "3&4" or cord_p2 == "4&1":
            if G_code == "G2":
                C = 360 - theta
                
            elif G_code == "G3":
                C = theta

    if cord_p1 == "4":
        if cord_p2 == "1" or cord_p2 == "1&2" or cord_p2 == "2&3" or cord_p2 == "4&1":

            if G_code == "G2":
                C = 360 - theta

            elif G_code == "G3":
                C = theta

        elif cord_p2 == "2":
            eval1_theta()

        elif cord_p2 == "3" or cord_p2 == "3&4":
            if G_code == "G2":
                C = theta
            elif G_code == "G3":
                C = 360 - theta

        elif cord_p2 == "4":
            eval2_theta()

    if cord_p1 == "1&2":
        if cord_p2 == "1" or cord_p2 == "4" or cord_p2 == "2&3" or cord_p2 == "4&1":

            if G_code == "G2":
                C = theta

            elif G_code == "G3":
                C = 360 - theta

        elif cord_p2 == "2" or cord_p2 == "3":
            if G_code == "G2":
                C = 360 - theta

            elif G_code == "G3":
                C = theta

        elif cord_p2 == "3&4":
            C = theta

    if cord_p1 == "2&3":
        if cord_p2 == "1" or cord_p2 == "2" or cord_p2 == "1&2":

            if G_code == "G2":
                C = theta

            elif G_code == "G3":
                C = 360 - theta


        elif cord_p2 == "3" or cord_p2 == "4" or cord_p2 == "3&4":
            if G_code == "G2":
                C = 360 - theta

            elif G_code == "G3":
                C = theta

        elif cord_p2 == "4&1":
            C = theta

    if cord_p1 == "3&4":
        if cord_p2 == "1" or cord_p2 == "4" or cord_p2 == "4&1":
            if G_code == "G2":
                C = 360 - theta

            elif G_code == "G3":
                C = theta

        elif cord_p2 == "2" or cord_p2 == "3" or cord_p2 == "2&3":
            if G_code == "G2":
                C = theta

            elif G_code == "G3":
                C = 360 - theta

        elif cord_p2 == "1&2":
            C = theta

    if cord_p1 == "4&1":
        if cord_p2 == "1" or cord_p2 == "2":
            if G_code == "G2":
                C = 360 - theta

            elif G_code == "G3":
                C = theta

        elif cord_p2 == "3" or cord_p2 == "4" or cord_p2 == "1&2" or cord_p2 == "3&4":
            if G_code == "G2":
                C = theta

            elif G_code == "G3":
                C = 360 - theta

        elif cord_p2 == "2&3":
            C = theta



#this function is to only be used if G0/G1 is going to another G0/G1
def C_G0_G1_eval(i,x_1,y_1):

    G0_G1_values(i)

    C_line(x_1,y_1)

    vectors_G0_G1(x_0, y_0, x_1, y_1, x_2, y_2)

    # Here is the dot product being solved
    dot(VEC_1x, VEC_2x, VEC_1y, VEC_2y)

    # the magnetude of both vectors is being evaluated
    magnitude(VEC_1x, VEC_1y, VEC_2x, VEC_2y)

    # finally the magnitudes are multiplied
    multi_mag(mag_1, mag_2)

    #there needs to be an evaluation as to which quadrent the second point resides in.
    line_eval_G0_G1(x_1, y_1, x_2, y_2)

    cord_angle_calc(dotprod,mag_mult)

    return C


#this function is to only be used if G0/G1 is going to another G0/G1
def C_G2_G3_eval(i):
    global C
    global last_G_code
    global x_0
    global y_0

    G2_G3_values(i)

    origin_xy(x_1, y_1, i_2, y_2)

    vectors_G2_G3(x_1, y_1, x_2, y_2, origin_x, origin_y)

    # the arc rotation should be calulated for each of the arcs.
    dot(VEC_1x, VEC_2x, VEC_1y, VEC_2y)

    # the magnitude of both vectors is being evaluated
    magnitude(VEC_1x, VEC_1y, VEC_2x, VEC_2y)

    # finally the magnitudes are multiplied
    multi_mag(mag_1, mag_2)

    rads(dotprod, mag_mult)

    theta = math.degrees(radians)

    #evaluation of starting angle


    #Evaluation of total rotation
    # finds corcinate that point #1 is in
    arc_cords_p1(x_1, y_1, origin_x, origin_y)
    # finds the cordinate that point #2 is in
    arc_cords_p2(x_2, y_2, origin_x, origin_y)

    # finds the degrees of rotation of the shortest angle between point #1 and #2
    #arc_angle(x_1, y_1, origin_x, origin_y, x_2, y_2)

    #based on comparison between coordinates of point #1 and #2 then degrees of rotation is evaluated
    # so correct one is selected
    arc_comp(cord_p1, cord_p2)

def g_eval(f,data):
    global flag_1
    global flag_2
    global x_1
    global y_1
    #for loop ensures that each line is read in the g-code file
    for i in data:
        global words
        words = i.split()

        # this is a logic gate that will pass each line until (* SHAPE Nr: 0 *) is reached.
        #(* SHAPE Nr: 0 *) is the universal start of the G-code. Everything before it is not important.
        if flag_1 != 1:
            #I found there are blank lines before (* SHAPE Nr: 0 *) comes up.
            if i =="\n":
                f.write(str(i))
            else:
                #this ensures that any lines are printed if they are before (* SHAPE.
                if words[0] == "(*" and words[1] == "SHAPE":
                    f.write(str(i))
                    #this flad ensures that after (*SHAPE Nr: 0 *) G-code is evaluated.
                    flag_1 = 1
                    #this flag allows for the first point to be logged as X_1 and Y_1
                    flag_2 = 1
                else:
                    f.write(str(i))
        else:
            # this logic checks to see if the line read is a rapid movement. It will print and store the numbers X & Y.
            if words[0] == "G0" or words[0] == "G1":

                if words[1] == "X":
                    # This flag checks the first G0 or G1 movement and does not move C
                    if flag_2 == 1:

                    #saving values into float values for evaluation later on
                        x_1 = float(words[2])
                        y_1 = float(words[4])

                        f.write(str(i))

                        flag_2 = 0

                    #placing values onto the second point
                    else:


                        #evaluation of where C axis should point
                        C_G0_G1_eval(i,x_1,y_1)

                        #this raises the Z axis so the cut material will not be ruined
                        f.write("G1" + " Z " + str(1.125) + "\r\n")

                        #Have C axis rotate before moving to next point.
                        f.write("G1" + " C " + str("%.3f" % round(C, 3)) + "\r\n")

                        #this lowers the Z axis back down so it can cut
                        f.write("G1" + " Z " + str(-1.125) + "\r\n")

                        #write line for point.
                        f.write(str(i))


                        #these two lines of code moves point 2 to point 1.

                        x_1 = x_2
                        y_1 = y_2

                #if the G-code line is G0 or G1 and the coordinate start with anything other than X then print it.
                else:
                    f.write(str(i))
            # this section of code looks for G2 and should look for G3 which are arc commands and identifies each
            # section of the G-code and pulls out the X ,Y, I, J and turns them into float.
            # At the start of the G-code file is a G20 command which needs to be vetted out.
            elif words[0] == "G2" or words[0] == "G3":

                #This is a catch incase G20 or G21 is in the G-code lines
                if words[0] != "G20" and words[0] != "G21":

                    C_G2_G3_eval(i)

                    # this raises the Z axis so the cut material will not be ruined
                    f.write("G1" + " Z " + str(1.125) + "\r\n")

                    # Have C axis rotate before moving to next point.
                    f.write("G1" + " C " + str("%.3f" % round(C, 3)) + "\r\n")

                    # this lowers the Z axis back down so it can cut
                    f.write("G1" + " Z " + str(-1.125) + "\r\n")


                    #last step in this process is to add the line "C XXX.XXX" which will be the degrees of rotation of the C axis
                    f.write( str(i[:-1]) + "  C " + str("%.3f" % round(C_arc,3)) +  "\r\n")




                #this section of code takes the end point and makes it the new starting point.
                #the t == 1 flag insures that this part is only entered into if a second point is defined.
                else:
                    f.write(str(i))
                x_1 = float(words[2])
                y_1 = float(words[4])



            #Here is a catch all of that writes any G-codes that do not meet any evaluation criteria
            #for G0 & G1 and also G2 & G3
            else:
                f.write(str(i))
