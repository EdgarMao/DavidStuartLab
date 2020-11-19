# programmed by Edgar Mao for David Stuart lab

# this program is designed to plot the relationship between any designated data parameters in the format of columns in a text file
# user needs to make sure that all of the imported python libraries are installed in order for this program to function normally.


import numpy as np
import math
import matplotlib.pyplot as plt




def getparam():
    #collect required parameters from user
    while True:
        raw_param = raw_input('Welcome to dataPlot, please enter your parameters (enter "format" for format hint).')
        if raw_param == 'format':
            print('''
            Format: 
            data_location independent_variable_name iv_column_number dependent_variable_names dv_column_numbers
            Example: 
            D:\Physics\BobLab\particle-detector\datafile.txt temperature 1 magnetic_field,humidity,air_pressure 2,3,4 
            ---------------------------------------------------------------------------------------------------------
            * use only commas to distinguish different dependent variables and their column numbers
            * use spaces to distinguish each parameter, do not put spaces within parameter names
            * all characters should be UTF-8 encoded
            ''')
        else:
            break
    global dataloc, iv_name, iv_num, dv_name, dv_num
    raw_param_list = raw_param.split(' ')
    dataloc = raw_param_list[0]
    iv_name = raw_param_list[1]
    iv_num = int(raw_param_list[2])
    dv_name = raw_param_list[3].split(',')
    dv_num_raw = raw_param_list[4].split(',')
    dv_num = [int(i) for i in dv_num_raw]


def getdata():
    data_file = open(dataloc)
    first_line = data_file.readline()
    raw_data = data_file.read()
    #test for how many columns there are
    global line_length
    line_length = first_line.split()
    data = raw_data.split()
    global data_sorted
    data_sorted = {}
    data_set = []
    a = 0
    # Sort out data
    # check the math for creating the sequence
    for i in range(len(line_length)):
        for j in range(int(len(data) / len(line_length))):
            try:
                data_set.append(float(data[len(line_length) * (j - 1) + a]))
            except ValueError:
                data_set.append(data[len(line_length) * (j - 1) + a])
        a = a + 1
        data_sorted[i] = data_set
        data_set = []


def graph():
    # start plotting
    plt.figure("x1")
    # create a for loop that plots out all the designated parameters
    b = 0
    for a in range(len(line_length)+1):
        if int(a) in dv_num:
            plt.plot(data_sorted[iv_num-1], data_sorted[a-1], label=dv_name[b-1])
            b = b + 1
        else:
            pass
    plt.xticks(rotation=45)
    plt.xlabel(iv_name)
    plt.ylabel(dv_name)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plt.grid(True)
    plt.show()


getparam()
getdata()
graph()