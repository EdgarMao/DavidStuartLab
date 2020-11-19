# programmed by Edgar Mao for David Stuart lab, I grant anyone full permission to copy, make changes, or rename this prorgam

# README
# this program is designed to plot the relationship between two designated parameters of data in the format of columns in a text file, and it specializes in plotting ONE given parameter's relationship with time parameter
# this program supports plotting time parameters that are separated into multiple columns (time parameters only)
# this program is developed in python 2.7. However, it can also run in python 3 when the function raw_input() in this program is manually changed to input()
# user needs to make sure that all of the imported python libraries are installed in order for this program to function normally.


import numpy as np
import math
import matplotlib.pyplot as plt


def getparam():
    # collect required parameters from user
    while True:
        # change raw_input() to input() when running this program in python 3
        raw_param = raw_input('Welcome to dataPlot, please enter your parameters (enter "format" for format hint).')
        if raw_param == 'format':
            print('''
            Format:
                Graphing two parameters:
                    data_location independent_variable_name iv_column_number dependent_variable_name dv_column_number 
                Example: 
                    D:\Physics\BobLab\particle-detector\datafile.txt temperature 1 magnetic_field 4

                Graphing one parameter in relationship to time:
                    data_location time time_column_numbers dependent_variable_name dv_column_number
                Example:
                    D:\Physics\BobLab\particle-detector\datafile.txt time 1,2,3 magnetic_field 3
            ---------------------------------------------------------------------------------------------------------
            * If the time parameter is separated into more than one column, enter all the column numbers
            * Use ONLY commas to distinguish different time parameters' column numbers
            * DO NOT put comma after the last iv column number
            * Use ONLY spaces to distinguish each parameter
            * All characters should be UTF-8 encoded
            * Make sure the independent variable name is time if you want to plot data in relationship to time
            ''')
        else:
            break
    global dataloc, iv_name, iv_num, dv_name, dv_num
    # organize all the parameters into separate lists
    raw_param_list = raw_param.split(' ')
    dataloc = raw_param_list[0]
    iv_name = raw_param_list[1]
    # option for plotting parameters in relationship to time
    if iv_name == 'time':
        iv_num_raw = raw_param_list[2].split(',')
        iv_num = [int(i) for i in iv_num_raw]
    else:
        iv_num = int(raw_param_list[2])
    dv_name = raw_param_list[3]
    dv_num = int(raw_param_list[4])


def getdata():
    # open designated file
    data_file = open(dataloc)
    raw_data = data_file.read()
    data_file_line = open(dataloc)
    first_line = data_file_line.readline()
    # test for how many columns there are
    global line_length
    line_length = first_line.split()
    data = raw_data.split()
    # Sort out data
    global data_sorted
    data_sorted = {}
    data_set = []
    a = 0
    # organize and append lists of data into a dictionary using a series of for loops
    for i in range(len(line_length)):
        if iv_name == 'time':
            for j in range(int(len(data) / len(line_length))):
                if (i + 1) in iv_num:
                    data_set.append(data[len(line_length) * j + a])
                else:
                    try:
                        data_set.append(float(data[len(line_length) * j + a]))
                    except ValueError:
                        data_set.append(data[len(line_length) * j + a])
            a = a + 1
        else:
            for j in range(int(len(data) / len(line_length))):
                try:
                    data_set.append(float(data[len(line_length) * j + a]))
                except ValueError:
                    data_set.append(data[len(line_length) * j + a])
            a = a + 1
        data_sorted[i] = data_set
        data_set = []
    # if statement for the time option
    if iv_name == 'time':
        # a for loop that joins different time parameters on the same line and collect them into a list
        global timelist
        timelist = []
        timelist_element = ''
        for i in range(int(len(data) / len(line_length))):
            for c in range(int(len(iv_num))):
                timelist_element = timelist_element + str(data_sorted[iv_num[c] - 1][i]) + ':'
            timelist.append(timelist_element)
            timelist_element = ''
    else:
        pass


def graph():
    # start plotting
    plt.figure("x1")
    # if statement for time related plotting option
    if iv_name == 'time':
        plt.plot(timelist, data_sorted[dv_num-1], label=dv_name)
    else:
        plt.plot(data_sorted[iv_num - 1], data_sorted[dv_num - 1], label=dv_name)
    # styling for the graph
    plt.xticks(np.arange(0, len(data_sorted[0]), step=(len(data_sorted[0])/10)), rotation=90)
    plt.xlabel(iv_name)
    plt.ylabel(dv_name)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plt.grid(True)
    plt.show()


getparam()
getdata()
graph()