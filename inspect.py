# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 20:09:15 2018

@author: disna
"""
import csv
import sys
import math

with open(sys.argv[1]) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    count =0
    listArgs = []
    for row in readCSV:

        if count!=0:
            listArgs.append(row[len(row)-1])
        count +=1
    dictCount = dict((x,listArgs.count(x)) for x in set(listArgs))
    
    maxVal=0
    maxKey=None
    entropy =0
    errorCount=0
    for key, value in dictCount.items():
        if value>maxVal:
            maxVal=value
            maxKey=key
        entropy += ((value/len(listArgs))*(math.log2(len(listArgs)/value)))
    
    for key, value in dictCount.items():
        if key!=maxKey:
            errorCount += value
    
    print("entropy: "+str(entropy))
    print("error: "+str(errorCount/len(listArgs)))