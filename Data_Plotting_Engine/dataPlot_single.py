# programmed by Edgar Mao for David Stuart lab -- I grant anyone permission to copy, change, rename any part of this program.

# this program is designed to graph one acceleration parameter in a local data file in relationship to time, please reference the example data format this program is tailored for.
# user needs to make sure that all of the imported python libraries are installed in order for this program to function normally.

import numpy as np
import math
import matplotlib.pyplot as plt
import time
import datetime
from datetime import datetime, timedelta

# list of global variables
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

# a function that obtains all required user parameters
def getuserinput():
    print('Welcome to accelerometer data plotting program, please enter your parameters.')
    dataloc = input('Enter location of data file: ')
    start_time = input('Start time (ex. 2019:06:30:22:37:46): ')
    end_time = input('End time (ex. 2019:11:30:22:37:00): ')
    sensor_name = input('Axes Name (avaliable axes: x,y,z -- choose one): ')
    return start_time, end_time, dataloc, sensor_name


# a function that collects data from desginated file and sort then into lists of data for different parameters
def getdata():
    data_file = open(f'{dataloc}', 'r')
    raw_data = data_file.read()
    dataset = raw_data.split()
    data.extend(dataset)
    # Sort raw data into different parameters
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


# a function that plots the desginated parameter in relationship to time  (with minor styling)
def graph():
    # Get data from user's time parameters;
    xfinal = x[raw_time.index(start_time):(raw_time.index(end_time)+1)]
    yfinal = y[raw_time.index(start_time):(raw_time.index(end_time)+1)]
    zfinal = z[raw_time.index(start_time):(raw_time.index(end_time)+1)]
    time_stamp_final = time_stamp_utc[raw_time.index(start_time):(raw_time.index(end_time)+1)]
    #start plotting
    plt.figure("x1")
    plt.title("Accerelation on the " + sensor_name + " axis as a function of time")
    if sensor_name == 'x':
        plt.plot(time_stamp_final, xfinal, label="x")
    elif sensor_name == 'y':
        plt.plot(time_stamp_final, yfinal, label="y")
    elif sensor_name == 'z':
        plt.plot(time_stamp_final, zfinal, label="z")
    else:
        print('Invalid parameter.')
    plt.xticks(rotation=45)
    plt.xlabel('utc time')
    plt.ylabel("Acceleration (m/s^2)")
    plt.grid(True)
    plt.show()


start_time, end_time, dataloc, sensor_name = getuserinput()
getdata()
graph()