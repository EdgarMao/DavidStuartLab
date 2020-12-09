# programmed by Edgar Mao for David Stuart Lab

# decide whether to use python2.7 or 3.6/7
# ***IMPORTANT currently using python 3.7

import matplotlib
import numpy as np
import math
import matplotlib.pyplot as plt
import requests
import urllib.request
import time
import datetime
from datetime import datetime, timedelta
from html.parser import HTMLParser
import re
import sys

# temporal solution to recursion depth exceeded
sys.setrecursionlimit(10**6)


# obtain high-voltage values with runtime

def getHV():
    global HV_num, run_num
    rawhtml = urllib.request.urlopen("http://cms2.physics.ucsb.edu/milliqanValidationPlots/")
    htmltxt = []
    raw_HV_data = []
    # the limit of this computer is about 130
    graph_range = 100
    htmltxt_line = str(rawhtml.readline())
    # enter the desired run number to move the cursor for readline to the spot
    while '<TD><A HREF="Run2630/index.html">' not in htmltxt_line:
        htmltxt_line = str(rawhtml.readline())
    # This loop is able to find all the stuff around TD, now get only the high voltage out.
    for i in range(graph_range):
        if "TD" in str(htmltxt_line):
            htmltxt.append(htmltxt_line)
            htmltxt_line = str(rawhtml.readline())
            while "TD" not in htmltxt_line:
                htmltxt.append(htmltxt_line)
                htmltxt_line = str(rawhtml.readline())
        else:
            htmltxt_line = str(rawhtml.readline())
    # get every 5th TD (with an exception condition)
    TD_count = 0
    for i in range(len(htmltxt)):
        # identify the start of every HV data
        if "TD" in htmltxt[i]:
            TD_count += 1
        else:
            pass
        if TD_count % 5 == 0:
            # This condition parses out the label rows
            if "evts" in htmltxt[i]:
                TD_count -= 1
            else:
                raw_HV_data.append(htmltxt[i])
        else:
            pass
    HV_data = []
    temp_HV = []
    for i in range(len(raw_HV_data)):
        if "TD" in raw_HV_data[i]:
            temp_HV.append(raw_HV_data[i])
            a = 1
            while "TD" not in raw_HV_data[i+a] and i+a < (len(raw_HV_data)-1):
                temp_HV.append(raw_HV_data[i+a])
                a += 1
            HV_data.append(''.join(temp_HV))
            temp_HV = []
    # group each HV data together and clean up the extra characters
    str_num = ["0","1","2","3","4","5","6","7","8","9"]
    HV_num = []
    for i in range(len(HV_data)):
        single_HV = [j for i in HV_data[i] for j in i]
        single_HV_num_avg = []
        for a in range(len(single_HV)):
            single_HV_num = []
            b = 1
            # revise this condition, some empty strings are getting mixed in
            while (single_HV[a] == "=" and single_HV[a+1] != "N") or (single_HV[a-3]+single_HV[a-2]+single_HV[a-1]+single_HV[a] == "<TD>" and (single_HV[a+1] in str_num)):
                if single_HV[a+b] in str_num:
                    single_HV_num.extend(single_HV[a+b])
                    b += 1
                else:
                    #print(single_HV_num)
                    single_HV_num_avg.append(float(''.join(single_HV_num)))
                    break
            #print(single_HV_num_avg)
        # making an average (consider if this is a valid idea or not)
        # IMPORTANT consider switching to groups of data of single sensors
        HV_num_avg = 0
        for i in range(len(single_HV_num_avg)):
            HV_num_avg = HV_num_avg + single_HV_num_avg[i]
        HV_num.append(HV_num_avg/len(single_HV_num_avg))
    print(HV_num)
    print(len(HV_num))
    # get the run numbers using the same method
    raw_run_num = []
    for i in range(len(htmltxt)):
        # identify the start of every HV data
        if '<TD><A HREF="Run' in htmltxt[i]:
            raw_run_num.append(htmltxt[i])
        else:
            pass
    run_num = []
    for i in range(len(raw_run_num)-1):
        raw_single_run_num = [j for i in raw_run_num[i] for j in i]
        single_run_num = []
        for a in range(len(raw_single_run_num)):
            if raw_single_run_num[a] in str_num:
                single_run_num.extend(raw_single_run_num[a])
            # Check this break condition if things don't work out
            elif raw_single_run_num[a] == '/':
                break
            else:
                pass
        run_num.append(int(''.join(single_run_num)))
    run_num = list(dict.fromkeys(run_num))
    print(run_num)
    print(len(run_num))
    return HV_num, run_num




# figure out how to associate high voltage with temperature using time
# consider the usage of average temperature and average HV


epoch_time = []
time_stamp_utc = []
time_stamp_HV = []
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
temp_data = []
HV_setting = []

# use dictionary to align temperature with HV
# find out what data structure would help to produce a histogram
def gettemp():
    # open the validation page of the last run and find the date, that will be the start date (first run is end date)
    HV_startdate = []
    raw_HV_startdate = []
    HV_enddate = []
    raw_HV_enddate = []
    for i in range(len(run_num)):
        # need to deal with bad runs
        response = requests.get(
            f"http://cms2.physics.ucsb.edu/milliqanValidationPlots/Run{str(run_num[i])}/index.html")
        if response.status_code == 200:
            rawhtml = urllib.request.urlopen(f"http://cms2.physics.ucsb.edu/milliqanValidationPlots/Run{str(run_num[i])}/index.html")
            rawhtml_line = str(rawhtml.readline())
        else:
            pass
        while "Summary:" not in rawhtml_line:
            rawhtml_line = str(rawhtml.readline())
        single_rawhtml = [j for i in rawhtml_line for j in i]
        for i in range(len(single_rawhtml)):
            if ''.join(single_rawhtml[i-7:i]) == "between":
                raw_HV_enddate = single_rawhtml[i+25:i+44]
                break
            else:
                pass
        HV_startdate.append(str(''.join(raw_HV_enddate)))
        for i in range(len(single_rawhtml)):
            if ''.join(single_rawhtml[i-7:i]) == "between":
                raw_HV_startdate = single_rawhtml[i+1:i+20]
                break
            else:
                pass
        HV_enddate.append(str(''.join(raw_HV_startdate)))
    print(HV_startdate)
    print(HV_enddate)
    # **** use these parameters to zoom in
    #HV_startdate = HV_startdate[0:7]
    #HV_enddate = HV_enddate[0:7]


    # modify and create a for loop that opens the temperature data one by one and aligns each day's data in a dictionary
    startdate = HV_startdate[0]
    enddate = HV_enddate[-1]
    temp_start_time = datetime.strptime(str(startdate), '%Y-%m-%d %H:%M:%S')
    temp_end_time = datetime.strptime(str(enddate), '%Y-%m-%d %H:%M:%S')
    # IMPORTANT has trouble creating time_diff smaller than 1 day
    time_diff = (temp_start_time - temp_end_time) // timedelta(days=1)
    print(time_diff)
    temp_time = temp_start_time
    for i in range(time_diff):
        year = datetime.strftime(temp_time, '%Y')
        month = datetime.strftime(temp_time, '%m')
        day = datetime.strftime(temp_time, '%d')
        temp_time_num = (year, month, day)
        # ***important: needs to only output valid files
        response = requests.get(
            f'http://cms2.physics.ucsb.edu/milliqan/EnvironSensorData/environ_aux_{temp_time_num[0]}{temp_time_num[1]}{temp_time_num[2]}.txt')
        if response.status_code == 200:
            URL.append(
                f'http://cms2.physics.ucsb.edu/milliqan/EnvironSensorData/environ_aux_{temp_time_num[0]}{temp_time_num[1]}{temp_time_num[2]}.txt')
        else:
            pass
        temp_time = temp_time - timedelta(days=1)
    URL_sorted = list(dict.fromkeys(URL))
    print(URL_sorted)
    for i in range(int(len(URL_sorted))):
        r = requests.get(URL_sorted[i])
        tempo = r.text[88:]
        dataset = tempo.split()
        temp_data.extend(dataset)
        # Attempt to add "None" into raw dataset
        for j in range(12):
            temp_data.append(None)
    try:
        temp_data.remove("\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
    except ValueError:
        pass
    try:
        temp_data.remove("\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
    except ValueError:
        pass
    try:
        temp_data.remove("\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
    except ValueError:
        pass
    # Sort out data
    # organize and create variables
    for j in range(len(HV_startdate)):
        for i in range(int(len(temp_data) / 12)):
            if temp_data[12*i] != None and temp_data[12*i + 11] != None:
                epoch_time.append(float(temp_data[12 * i]))
                time_stamp_utc.append(datetime.strptime(temp_data[12 * i + 1], '%Y:%m:%d:%H:%M:%S'))
                temp1.append(float(temp_data[12 * i + 2]))
                temp2.append(float(temp_data[12 * i + 3]))
                temp3.append(float(temp_data[12 * i + 4]))
                temp4.append(float(temp_data[12 * i + 5]))
                humi1.append(float(temp_data[12 * i + 6]))
                humi2.append(float(temp_data[12 * i + 7]))
                humi3.append(float(temp_data[12 * i + 8]))
                humi4.append(float(temp_data[12 * i + 9]))
                pressure.append(float(temp_data[12 * i + 10]))
                temp.append(float(temp_data[12 * i + 11]))
            else:
                epoch_time.append(temp_data[12 * i])
                time_stamp_utc.append(datetime.strptime(temp_data[12 * (i-1) + 1], '%Y:%m:%d:%H:%M:%S'))
                temp1.append(temp_data[12 * i + 2])
                temp2.append(temp_data[12 * i + 3])
                temp3.append(temp_data[12 * i + 4])
                temp4.append(temp_data[12 * i + 5])
                humi1.append(temp_data[12 * i + 6])
                humi2.append(temp_data[12 * i + 7])
                humi3.append(temp_data[12 * i + 8])
                humi4.append(temp_data[12 * i + 9])
                pressure.append(temp_data[12 * i + 10])
                temp.append(temp_data[12 * i + 11])
            if temp_data[12 * i + 1] != None and datetime.strptime(HV_startdate[j-1], '%Y-%m-%d %H:%M:%S') >= datetime.strptime(temp_data[12 * i + 1], '%Y:%m:%d:%H:%M:%S') >= datetime.strptime(HV_enddate[j-1], '%Y-%m-%d %H:%M:%S'):
                HV_setting.append(HV_num[j-1]/100 + 12)
            else:
                HV_setting.append(None)
    # add "None" into parts where you want the data to break
    return epoch_time, time_stamp_utc, temp1, temp2, temp3, temp4, humi1, humi2, humi3, humi4, pressure, temp, time_stamp_HV, HV_setting;

# overall thoughts on this problem: seems to be a more complex problem than graphing two lines of data, should consider what algorithm to use to make a vaild comparsion
# design problems: how to compare runs with different amount of sensors? average temp and HV or what else?
# need better statistical strategy, but finish some proofs of concept first

#def sortdata():

# IMPORTANT all you actaully need to break the annoying lines is add "None" at the end of a part of the data that's gonna break

def runplot():
    sensor_name_list = 'temp2', 'temp3'#, 'temp4'
    plt.figure("x1")
    # create a for loop that plots out all the designated parameters
    plt.plot(time_stamp_utc, HV_setting, label="HV Setting ((V * 10^-2)+12)")
    for i in range(len(sensor_name_list)):
        if sensor_name_list[i] == 'temp1':
            plt.plot(time_stamp_utc, temp1, label="temp1(\u00b0" + "C)")
        elif sensor_name_list[i] == 'temp2':
            plt.plot(time_stamp_utc, temp2, label="temp2(\u00b0" + "C)")
        elif sensor_name_list[i] == 'temp3':
            plt.plot(time_stamp_utc, temp3, label="temp3(\u00b0" + "C)")
        elif sensor_name_list[i] == 'temp4':
            plt.plot(time_stamp_utc, temp4, label="temp4(\u00b0" + "C)")
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
    #plt.ylabel("temperature (\u00b0" + "C)")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    #plt.legend(loc='upper right', borderaxespad=0.)
    plt.grid(True)
    plt.show()


getHV()
gettemp()
runplot()
