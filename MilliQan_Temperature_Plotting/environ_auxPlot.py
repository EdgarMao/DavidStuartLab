#programmed by Edgar Mao for David Stuart lab

#Key questions that are yet to be answered : does T increases with HV , What is T(HV()
#Hands on stuff: set up an experiment that losely analyzes the temperature and the gain (the gain is not only effected by the high voltage but also a lot of other factors -- including temperature in a scilicon PMT) of PMT
#temperature in relationship to time  --> temperature as a function of high voltage, temperature settle time in relationship to HV

import numpy as np
import math
import matplotlib.pyplot as plt
import requests
import time
import datetime
from datetime import datetime, timedelta


#list of variables
start_time = ()
end_time = ()
yname = ["temperature"]
epoch_time = []
time_stamp_utc = []
temp1 = []
temp2 = []
temp3 = []
temp4 = []
humi1 = []
humi2 = []
humi3 = []
humi4 = []
pressure = []
temp = []
URL = []
data = []
sensor_name_list = []

'''
problems with the data set:
- random datas have unknown symbols in them
- the group of data recorded in January 2019 were labeled 2018
'''

def getdatalist():
    print('Welcome to environment sensor data plotting program, please enter your parameters.')
    start_time = input('Start time (ex. 2019:06:30:22:37:46): ')
    end_time = input('End time (ex. 2019:11:30:22:37:00): ')
    sensor_name = input('Sensor Names (avaliable sensors:temp1, temp2, temp3, temp4, humi1, humi2, humi3, humi4, pressure, temp -- separate them by commas without spaces): ')
    sensor_name_list = sensor_name.split(',')
    #create a desirable time format
    temp_start_time = datetime.strptime(start_time, '%Y:%m:%d:%H:%M:%S')
    temp_end_time = datetime.strptime(end_time, '%Y:%m:%d:%H:%M:%S')
    time_diff = (temp_end_time - temp_start_time) // timedelta(days=1)
    temp_time = temp_start_time
    for i in range(time_diff):
        year = datetime.strftime(temp_time, '%Y')
        month = datetime.strftime(temp_time, '%m')
        day = datetime.strftime(temp_time, '%d')
        temp_time_num = (year, month, day)
        # ***important: needs to only output valid files
        response = requests.get(f'http://cms2.physics.ucsb.edu/milliqan/EnvironSensorData/environ_aux_{temp_time_num[0]}{temp_time_num[1]}{temp_time_num[2]}.txt')
        if response.status_code == 200:
            URL.append(f'http://cms2.physics.ucsb.edu/milliqan/EnvironSensorData/environ_aux_{temp_time_num[0]}{temp_time_num[1]}{temp_time_num[2]}.txt')
        else:
            pass
        temp_time = temp_time +  timedelta(days=1)
    URL_sorted = list(dict.fromkeys(URL))
    return start_time, end_time, URL_sorted, sensor_name_list



#enable user to choose what time to plot

def getdata(site):
    for i in range(int(len(site))):
        r = requests.get(site[i])
        tempo = r.text[88:]
        dataset = tempo.split()
        data.extend(dataset)
    try:
        data.remove("\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
    except ValueError:
        pass
    try:
        data.remove("\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
    except ValueError:
        pass
    try:
        data.remove("\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
    except ValueError:
        pass
    #Sort out data
    for i in range(int(len(data) / 12)):
        epoch_time.append(float(data[12 * i]))
        time_stamp_utc.append(datetime.strptime(data[12 * i + 1], '%Y:%m:%d:%H:%M:%S'))
        temp1.append(float(data[12 * i + 2]))
        temp2.append(float(data[12 * i + 3]))
        temp3.append(float(data[12 * i + 4]))
        temp4.append(float(data[12 * i + 5]))
        humi1.append(float(data[12 * i + 6]))
        humi2.append(float(data[12 * i + 7]))
        humi3.append(float(data[12 * i + 8]))
        humi4.append(float(data[12 * i + 9]))
        pressure.append(float(data[12 * i + 10]))
        temp.append(float(data[12 * i + 11]))
    #Get data from designated time
    return epoch_time, time_stamp_utc, temp1, temp2, temp3, temp4, humi1, humi2, humi3, humi4, pressure, temp;



def graph():
    plt.figure("x1")
    #create a for loop that plots out all the designated parameters
    plt.title("temperatures" + ' as a function of time')
    for i in range(len(sensor_name_list)):
        temp_sensor_name = str(sensor_name_list[i])
        if sensor_name_list[i] == 'temp1':
            plt.plot(time_stamp_utc, temp1, label="temp1")
        elif sensor_name_list[i] == 'temp2':
            plt.plot(time_stamp_utc, temp2, label="temp2")
        elif sensor_name_list[i] == 'temp3':
            plt.plot(time_stamp_utc, temp3, label="temp3")
        elif sensor_name_list[i] == 'temp4':
            plt.plot(time_stamp_utc, temp4, label="temp4")
        elif sensor_name_list[i] == 'humi1':
            plt.plot(time_stamp_utc, humi1, label="humi1")
        elif sensor_name_list[i] == 'humi2':
            plt.plot(time_stamp_utc, humi2, label="humi2")
        elif sensor_name_list[i] == 'humi3':
            plt.plot(time_stamp_utc, humi3, label="humi3")
        elif sensor_name_list[i] == 'humi4':
            plt.plot(time_stamp_utc, humi4, label="humi4")
        elif sensor_name_list[i] == 'pressure':
            plt.plot(time_stamp_utc, pressure, label="pressure")
        elif sensor_name_list[i] == 'temp':
            plt.plot(time_stamp_utc, temp, label="temp")
        else:
            print('Invalid parameter.')
    plt.xticks(rotation=45)
    plt.xlabel('utc time')
    plt.ylabel("temperature (\u00b0" + "C)")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plt.grid(True)
    plt.show()


start_time, end_time, URL_sorted, sensor_name_list = getdatalist()
getdata(URL_sorted)
graph()
