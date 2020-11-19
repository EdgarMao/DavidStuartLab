# programmed by Edgar Mao for David Stuart lab

# this program is designed to graph one acceleration parameter in a local data file in relationship to time, please reference the example data format this program is tailored for.
# user needs to make sure that all of the imported python libraries are installed in order for this program to function normally.

# make the prorgam compatible for python 2.7
# make two separate programs for historgram and parameters


import numpy as np
import math
import matplotlib.pyplot as plt
import time
import datetime
from datetime import datetime, timedelta

# list of variables
start_time = ()
end_time = ()
time = []
day = []
month = []
year = []
x = []
y = []
z = []
temp = []
data = []
time_stamp_utc = []
raw_time = []
raw_data = []
dataloc = []

def getdatalist():
    #collect required parameters from user
    print('Welcome to accelerometer data plotting program, please enter your parameters.')
    dataloc = input('Enter location of data file: ')
    start_time = input('Start time (ex. 2019:06:30:22:37:46): ')
    end_time = input('End time (ex. 2019:11:30:22:37:00): ')
    sensor_name = input('Axes Names (avaliable axes: x,y,z): ')
    sensor_name_list = sensor_name.split(',')
    # create a desirable time format;
    temp_start_time = datetime.strptime(start_time, '%Y:%m:%d:%H:%M:%S')
    temp_end_time = datetime.strptime(end_time, '%Y:%m:%d:%H:%M:%S')
    temp_time = temp_start_time
    return start_time, end_time, dataloc, sensor_name_list



def getdata(site):
    # This for loop is for potential updates on reliably plotting data from multiple files
    for i in range(int(len(site))):
        data_file = open(f'{dataloc}', 'r')
        raw_data = data_file.read()
        dataset = raw_data.split()
        data.extend(dataset)
    # Sort out data
    for i in range(int(len(data) / 7)):
        day.append(data[7 * i])
        month.append(data[7 * i + 1])
        year.append(data[7 * i + 2])
        time.append(data[7 * i + 3])
        raw_time.append('{}:{}:{}:{}'.format(year[i], month[i], day[i], time[i]))
        time_stamp_utc.append(datetime.strptime(raw_time[i], '%Y:%m:%d:%H:%M:%S'))
        x.append(float(data[7 * i + 4]))
        y.append(float(data[7 * i + 5]))
        z.append(float(data[7 * i + 6]))
    return time_stamp_utc, x, y, z


def graph():
    # Get data from designated time;
    xfinal = x[raw_time.index(start_time):(raw_time.index(end_time)+1)]
    yfinal = y[raw_time.index(start_time):(raw_time.index(end_time)+1)]
    zfinal = z[raw_time.index(start_time):(raw_time.index(end_time)+1)]
    time_stamp_final = time_stamp_utc[raw_time.index(start_time):(raw_time.index(end_time)+1)]
    #start plotting
    plt.figure("x1")
    # create a for loop that plots out all the designated parameters
    plt.title("Acceleration" + ' as a Function of Time')
    for i in range(len(sensor_name_list)):
        temp_sensor_name = str(sensor_name_list[i])
        if sensor_name_list[i] == 'x':
            plt.plot(time_stamp_final, xfinal, label="x")
        elif sensor_name_list[i] == 'y':
            plt.plot(time_stamp_final, yfinal, label="y")
        elif sensor_name_list[i] == 'z':
            plt.plot(time_stamp_final, zfinal, label="z")
        else:
            print('Invalid parameter.')
    plt.xticks(rotation=45)
    plt.xlabel('utc time')
    plt.ylabel("Acceleration (m/s^2)")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plt.grid(True)
    plt.show()


start_time, end_time, dataloc, sensor_name_list = getdatalist()
getdata(dataloc)
graph()
