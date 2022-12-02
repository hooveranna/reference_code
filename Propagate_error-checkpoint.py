#!/usr/bin/env python3
import sys
import csv
import os
import numpy as np


def fixAndTransposeCsvFile(filename, count, trials):
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        i = 0
        total_data = np.empty([int(count),int(trials)])
        print("rows = "+str(len(total_data))+" columns = "+str(len(total_data[0])))
        for row in csv_reader:
            # making sure you're not in the header row
            if (i != 0) and (i < (int(trials) + 1)):
                j = 0
                #print(len(row))
                for datapoint in row:
                    #print(datapoint)
                    #make sure you're in the actual data
                    if j > 8:
                        #print("i=" + str(i) + " j=" + str(j))
                        #print (datapoint)
                        total_data[j-9][i-1] = datapoint
                    j += 1
            i += 1

    return total_data

def findCountAndTrialNum(filename):
    all_timestamps = []
    i = 0
    timeconst = 0
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        k = 0
        for row in csv_reader:
            if k == 1:
                j = 0
                for datapoint in row:
                    if j == 7:
                        print(datapoint)
                        timeconst = datapoint
                    j += 1
            k += 1
    for i in range(len(raw_data)):
        all_timestamps.append(float(i) / float(timeconst))
        i += 1
    return all_timestamps


def calcTimestamp(filename, raw_data):
    all_timestamps = []
    i = 0
    timeconst = 0
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        k = 0
        for row in csv_reader:
            if k == 1:
                j = 0
                for datapoint in row:
                    if j == 7:
                        print(datapoint)
                        timeconst = datapoint
                    j += 1
            k += 1
    for i in range(len(raw_data)):
        all_timestamps.append(float(i) / float(timeconst))
        i += 1
    return all_timestamps


def calcErrorFromFixed(raw_data, all_averages):
    ## HERE'S WHERE YOU ADD IN THE DIGITIZATION ERROR CONSTANT
    all_err = (5.2/(256.0))**2 / 12.0
    all_events=[] #array to store errors
    i = 0
    for row in raw_data:
        #print(i)
        #print(row[0])
        #row[0] = row[0][-7:]
        #print(column)
        timestamp_err = 0
        #print(*row, sep='\n')
        for datapoint in row:
            #print(datapoint)
            if float(datapoint) != 0:
                datapoint_err = all_err / (float(datapoint)**2)
            else:
                datapoint_err = all_err / (0.1**2)
            timestamp_err = timestamp_err + datapoint_err
        all_events.append(np.sqrt(timestamp_err) * all_averages[i])
        i += 1
    ##print(i)
    return all_events

def calcAverageFromFixed(raw_data):
    all_err = (9.2/256.0)**2
    all_events=[] #array to store errors
    i = 0
    for row in raw_data:
        sum_row = 0
        num_row = 0
        #print(*row, sep='\n')
        for datapoint in row:
            #print(datapoint)
            sum_row = sum_row + float(datapoint)
            num_row += 1
        all_events.append(sum_row / num_row)
        i += 1
    return all_events

def calcSTDEVMFromFixed(raw_data, all_averages):
    all_err = (9.2/256.0)**2
    all_events=[] #array to store errors
    i = 0
    for row in raw_data:
        sum_row = 0
        num_row = 0
        #print(*row, sep='\n')
        for datapoint in row:
            #print(datapoint)
            sum_row = sum_row + (float(datapoint) - all_averages[i])**2
            num_row += 1
        all_events.append(np.sqrt(sum_row / (num_row-1))/np.sqrt(num_row))
        i += 1
    return all_events


def calcTotalError(all_stdevms, all_events):
    all_tot_errs = []
    i = 0
    for err in all_events:
        all_tot_errs.append(np.sqrt((all_stdevms[i])**2 + (err)**2))
        i += 1
    return all_tot_errs

# takes a single argument, the name of the file to be parsed
if (len(sys.argv) != 4):
    print("Usage: parseBitscope.py count trials filename.csv"); sys.exit(-1)
if(sys.argv[3][-4:] == ".csv"):
    raw_data = fixAndTransposeCsvFile(sys.argv[3], sys.argv[1], sys.argv[2])

    all_timestamps = calcTimestamp(sys.argv[3], raw_data)
    all_averages = calcAverageFromFixed(raw_data)
    all_stdevms = calcSTDEVMFromFixed(raw_data, all_averages)
    all_events = calcErrorFromFixed(raw_data, all_averages)
    all_tot_errs = calcTotalError(all_stdevms, all_events)
    outfilename=sys.argv[3][:-4] + "_errors.csv"
    if os.path.exists(outfilename):
        os.remove(outfilename) #this deletes the file
    outfile=open(outfilename,'w')
    outfile.write(" "+","+"timestamp"+","+"Averages"+","+"total Errors"+","
                    +"STDEVM"+","+"Dig Err"+"\n")
    for i in range(len(all_events)):
        outfile.write(str(i)+","+str(all_timestamps[i])+","
                        +str(all_averages[i])+","+str(all_tot_errs[i])
                        +","+str(all_stdevms[i])+","+str(all_events[i])+"\n")
    outfile.close()
else:
    print(sys.argv[1][-4:])
    print("Argument does not have .csv as suffix"); sys.exit(-1);
