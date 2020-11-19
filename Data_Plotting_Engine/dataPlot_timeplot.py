# programmed by Edgar Mao for David Stuart lab

# README
# this program is designed to plot the relationship between any designated parameters of data in the format of columns in a text file, and it specializes in plotting given parameters' relationship with time parameter.
# this program supports plotting time parameters that are separated into multiple columns
# user needs to make sure that all of the imported python libraries are installed in order for this program to function normally.


import numpy as np
import math
import matplotlib.pyplot as plt



def getparam():
    #collect required parameters from user
    while True:
        # when using python 3, change the function raw_input() into input()
        raw_param = raw_input('Welcome to dataPlot, please enter your parameters (enter "format" for format hint).')
        if raw_param == 'format':
            print('''
            Format:
                Graphing two or more parameters:
                    data_location independent_variable_name iv_column_number dependent_variable_names dv_column_numbers 
                Example: 
                    D:\Physics\BobLab\particle-detector\datafile.txt temperature 1 magnetic_field,humidity,air_pressure 2,3,4
                
                Graphing one parameter in relationship to time:
                    data_location time time_column_numbers dependent_variable_names dv_column_numbers
                Example:
                    D:\Physics\BobLab\particle-detector\datafile.txt time 1,2 magnetic_field,humidity,air_pressure 3,4,5
            ---------------------------------------------------------------------------------------------------------
            * use only commas to distinguish different dependent variables and their column numbers
           * MAKE SURE each column name has its corresponding column number 
            * DO NOT put comma after the last column number or parameter name
            * use spaces to distinguish each parameter, DO NOT put spaces within parameter names
            * all characters should be UTF-8 encoded
            * make sure the independent variable name is time if you want to plot data in relationship to time
            ''')
        else:
            break
    global dataloc, iv_name, iv_num, dv_name, dv_num
    raw_param_list = raw_param.split(' ')
    dataloc = raw_param_list[0]
    iv_name = raw_param_list[1]
    if iv_name == 'time':
        iv_num_raw = raw_param_list[2].split(',')
        iv_num = [int(i) for i in iv_num_raw]
    else:
        iv_num = int(raw_param_list[2])
    dv_name = raw_param_list[3].split(',')
    dv_num_raw = raw_param_list[4].split(',')
    dv_num = [int(i) for i in dv_num_raw]

def getdata():
    data_file = open(dataloc)
    raw_data = data_file.read()
    data_file_line = open(dataloc)
    first_line = data_file_line.readline()
    # test for how many columns there are
    global line_length
    line_length = first_line.split()
    data = raw_data.split()
    global data_sorted
    data_sorted = {}
    data_set = []
    a = 0
    # Sort out data
    for i in range(len(line_length)):
        if iv_name == 'time':
            for j in range(int(len(data) / len(line_length))):
                if (i+1) in iv_num:
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
    # create if statement for the time option
    if iv_name == 'time':
        global timelist
        timelist = []
        timelist_element = ''
        for i in range(int(len(data) / len(line_length))):
            for c in range(int(len(iv_num))):
                timelist_element = timelist_element + str(data_sorted[iv_num[c]-1][i]) + ':'
            timelist.append(timelist_element)
            timelist_element = ''
    else:
        pass




def graph():
    # start plotting
    plt.figure("x1")
    # create a for loop that plots out all the designated parameters
    b = 0
    for a in range(len(line_length)+1):
        if iv_name == 'time':
            if int(a) in dv_num:
                plt.plot(timelist, data_sorted[a - 1], label=dv_name[b])
                b = b + 1
            else:
                pass
        else:
            if int(a) in dv_num:
                plt.plot(data_sorted[iv_num], data_sorted[a - 1], label=dv_name[b])
                b = b + 1
            else:
                pass
    plt.xticks(np.arange(0, len(data_sorted[0]), step=(len(data_sorted[0])/10)), rotation=90)
    plt.xlabel(iv_name)
    plt.ylabel(dv_name)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plt.grid(True)
    plt.show()


getparam()
getdata()
graph()