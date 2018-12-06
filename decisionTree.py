# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 21:29:08 2018

@author: disna
"""

import csv
import sys
import math

def calculateEntropy(arr):
    posClass = arr[0]
    negClass = arr[1]
    sumClass = arr[0] +arr[1]
    entropy =0
    if posClass==0:
        entropy = ((negClass/sumClass)* (math.log2(sumClass/negClass)) )
    elif negClass==0:
        entropy = ((posClass/sumClass)* (math.log2(sumClass/posClass)) )
    else:
        entropy = ((posClass/sumClass)* (math.log2(sumClass/posClass)) )+ ((negClass/sumClass)* (math.log2(sumClass/negClass)) )
    return entropy


def mutualInfoStub(node_Entropy,arr,labels,features):
    list_set = list(set(arr)) 
    arr_feature=[None,None]
    
    if list_set[0]=="y" or list_set[0]=="A" or list_set[0]=="yes" or list_set[0]=="before1950" or list_set[0]=="morethan3min" or list_set[0]=="expensive" or list_set[0]=="fast" or list_set[0]=="high" or list_set[0]=="Two" or list_set[0]=="morethan3min" or list_set[0]=="large":
        arr_feature[0] = list_set[0]
        arr_feature[1] = list_set[1]
    if list_set[0]=="n" or list_set[0]=="notA" or list_set[0]=="no" or list_set[0]=="after1950" or list_set[0]=="lessthan3min"  or list_set[0]=="slow" or list_set[0]=="cheap" or list_set[0]=="low" or list_set[0]=="MoreThanTwo" or list_set[0]=="lessthan3min" or list_set[0]=="small":
        arr_feature[0] = list_set[1]
        arr_feature[1] = list_set[0]
    
    #print ("list_set" + str(arr_feature))
    classes=[None,None]
    labels_set = list(set(labels))
    
    #print ("labels_set" +str(labels_set))
    if labels_set[0]=="y" or labels_set[0]=="democrat" or labels_set[0]=="A" or labels_set[0]=="yes":
            classes[0]=labels_set[0]
            classes[1]=labels_set[1]
    elif labels_set[0]=="n" or labels_set[0]=="republican" or labels_set[0]=="notA" or labels_set[0]=="no":
            classes[1]=labels_set[0]
            classes[0]=labels_set[1]
    pos_0 =0
    neg_0 =0
    pos_1 =0
    neg_1 =0
    label0 = []
    features0 = []
    features1 = []
    label1 = []
    for i in range(len(arr)):
        if arr[i]==arr_feature[0]:
            if labels[i]==classes[0]:
                pos_0 +=1
                label0.append(labels[i])
                features0.append(features[i])
            else:
                neg_0 +=1
                label0.append(labels[i])
                features0.append(features[i])
        if arr[i]==arr_feature[1]:
            if labels[i]==classes[0]:
                pos_1 +=1
                label1.append(labels[i])
                features1.append(features[i])
            else:
                neg_1 +=1
                label1.append(labels[i])
                features1.append(features[i])
    
    #print ("pos0 :" + str(pos_0))
    #print ("neg_0 :" + str(neg_0))
    #print ("pos_1 :" + str(pos_1))
    #print ("pos_1 :" + str(neg_1))
    entropy1 = calculateEntropy([pos_0,neg_0])
    entropy2 = calculateEntropy([pos_1,neg_1])
    mutualInfo = node_Entropy - ((len(label0)/len(arr)) * entropy1 )- ((len(label1)/len(arr)) * entropy2)
    
    return (mutualInfo,arr_feature[0],label0,features0, pos_0,neg_0, classes[0],arr_feature[1], label1, features1,pos_1,neg_1,classes[1])


with open(sys.argv[1]) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    count =0
    listArgs = []
    columnNames=[]
    features=[]
    rowCount=0
    
    for row in readCSV:
        row_feature=[]
        if count ==0:
            for r in row:
                columnNames.append(r)
            columnNames = columnNames[:-1]   
        if count!=0:
            for r in row:
               row_feature.append(r)
            row_feature = row_feature[:-1]
            features.append(row_feature)
            listArgs.append(row[len(row)-1])
        count +=1
    rowCount = len(listArgs)
    dictCount = dict((x,listArgs.count(x)) for x in set(listArgs))
    
    classes = [0,0]
    for key, value in dictCount.items():
        if key=="y" or key=="democrat" or key=="A" or key=="yes":
            classes[0]=value
        elif key=="n" or key=="republican" or key=="notA" or key=="no":
            classes[1]=value
    entropy_root = calculateEntropy(classes)

    ##RootNode
    print("["+str(classes[0])+"+/"+str(classes[1])+"-]")
    
    
    maxInfoGain =0
    splitColumn0 =None
    rightBranch = False
    leftBranch = False
    
    splitpos1 =0
    splitpos0 =0
    splitpos0_left =0
    splitpos0_right=0
    splitpos1_left =0
    splitpos1_right=0
    
    splitneg1 =0
    splitneg0 =0
    splitneg0_left =0
    splitneg0_right=0
    splitneg1_left =0
    splitneg1_right=0
    
    for i in range(len(columnNames)):
        arr = [el[i] for el in features]
        mutualInfo,labelPos,labelsPos,featuresPos,pos_0,neg_0 ,classes0,labelNeg,labelsNeg,featuresNeg, pos_1,neg_1,classes1 = mutualInfoStub(entropy_root,arr,listArgs,features)
        if mutualInfo >maxInfoGain and mutualInfo>=0.1:
            maxInfoGain = mutualInfo
            splitColumn0 = columnNames[i]
            splitLabel0 = labelPos
            splitLabels0 = labelsPos
            splitLabels1= labelsNeg
            splitLabel1 = labelNeg
            splitfeatures0 = featuresPos
            splitfeatures1= featuresNeg
            splitpos0= pos_0
            splitneg0 = neg_0
            splitpos1 = pos_1
            splitneg1 = neg_1
    
    #if 
    print(str(splitColumn0) +" = "+str(splitLabel0)+": ["+str(splitpos0)+"+/"+str(splitneg0)+"-]")
            
            
     ##Split on Left Node:
    splitColumn_left =None
    features = splitfeatures0
    listArgs = splitLabels0
    maxInfoGain =0
    entropy_leftNode = calculateEntropy([splitpos0,splitneg0])
     
    if splitpos0!=0 and splitneg0!=0:
        
        for i in range(len(columnNames)):
            arr = [el[i] for el in features]
            if columnNames[i]!= splitColumn0:
                mutualInfo_left,labelPos_left,labelsPos_left,featuresPos_left,pos_0_left,neg_0_left ,classes0_left, labelNeg_left,labelsNeg_left,featuresNeg_left,pos_1_left,neg_1_left,classes1_left = mutualInfoStub(entropy_leftNode,arr,listArgs,features)
                if mutualInfo_left >maxInfoGain and mutualInfo_left>=0.1:
                    maxInfoGain = mutualInfo_left
                    splitColumn_left = columnNames[i]
                    splitLabel0_left = labelPos_left
                    splitLabels0_left = labelsPos_left
                    splitLabels1_left= labelsNeg_left
                    splitfeatures0_left = featuresPos_left
                    splitfeatures1_left= featuresNeg_left
                    splitLabel1_left = labelNeg_left
                    splitpos0_left= pos_0_left
                    splitneg0_left = neg_0_left
                    splitpos1_left = pos_1_left
                    splitneg1_left = neg_1_left
        if maxInfoGain>=0.1:
            leftBranch = True
            print("| "+str(splitColumn_left) +" = "+str(splitLabel0_left)+": ["+str(splitpos0_left)+"+/"+str(splitneg0_left)+"-]")
            print("| "+str(splitColumn_left) +" = "+str(splitLabel1_left)+": ["+str(splitpos1_left)+"+/"+str(splitneg1_left)+"-]")
        
    print(str(splitColumn0) +" = "+str(splitLabel1)+": ["+str(splitpos1)+"+/"+str(splitneg1)+"-]")   
    splitColumn_right =None
    features = splitfeatures1
    listArgs = splitLabels1
    maxInfoGain =0
    entropy_rightNode = calculateEntropy([splitpos1,splitneg1])
     
    if splitpos1!=0 and splitneg1!=0:
        
        for i in range(len(columnNames)):
            arr = [el[i] for el in features]
            if columnNames[i]!= splitColumn0:
                mutualInfo_right,labelPos_right,labelsPos_right,featuresPos_right,pos_0_right,neg_0_right ,classes0_right,labelNeg_right,labelsNeg_right,featuresNeg_right, pos_1_right,neg_1_right, classes1_right = mutualInfoStub(entropy_rightNode,arr,listArgs,features)
                if mutualInfo_right >maxInfoGain and mutualInfo_right>=0.1:
                    maxInfoGain = mutualInfo_right
                    splitColumn_right = columnNames[i]
                    splitLabels0_right = labelsPos_right
                    splitLabel0_right = labelPos_right
                    splitLabels1_right= labelsNeg_right
                    splitfeatures0_right = featuresPos_right
                    splitfeatures1_right= featuresNeg_right
                    splitLabel1_right = labelNeg_right
                    splitpos0_right= pos_0_right
                    splitneg0_right = neg_0_right
                    splitpos1_right = pos_1_right
                    splitneg1_right = neg_1_right
        if maxInfoGain>=0.1:
            rightBranch = True
            print("| "+str(splitColumn_right) +" = "+str(splitLabel0_right)+": ["+str(splitpos0_right)+"+/"+str(splitneg0_right)+"-]")
            print("| "+str(splitColumn_right) +" = "+str(splitLabel1_right)+": ["+str(splitpos1_right)+"+/"+str(splitneg1_right)+"-]")
        
        
    errorTrain =0
    if splitpos0_left!=0 and splitneg0_left!=0:
        errorTrain += min(splitpos0_left,splitneg0_left)
    if splitpos1_left!=0 and splitneg1_left!=0:
        errorTrain += min(splitpos1_left,splitneg1_left)
    
    if splitpos0_right!=0 and splitneg0_right!=0:
        errorTrain += min(splitpos0_right,splitneg0_right)
    if splitpos1_right!=0 and splitneg1_right!=0:
        errorTrain += min(splitpos1_right,splitneg1_right)
        
    if leftBranch ==False:
        errorTrain += min(splitpos0,splitneg0)
    if rightBranch ==False:
        errorTrain += min(splitpos1,splitneg1)
    print("error(train): " +str(errorTrain/rowCount))

misclassification =0    
with open(sys.argv[2]) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')   
    count =0
    listArgs = []
    columnNames=[]
    features=[]
    for row in readCSV:
        row_feature=[]
        if count ==0:
            for r in row:
                columnNames.append(r)
            columnNames = columnNames[:-1]   
        if count!=0:
            for r in row:
               row_feature.append(r)
            row_feature = row_feature[:-1]
            features.append(row_feature)
            listArgs.append(row[len(row)-1])
        count +=1
    
    decidingClass = None
    ActualClass = None
    
    count=0
    for row_feature in features:
        
        ##features
        for j in range(len(row_feature)):
            if columnNames[j]==splitColumn0:
                ##left branch is there
                if row_feature[j]==splitLabel0 and leftBranch==True:
                    for k in range(len(row_feature)):
                        
                        if columnNames[k]==splitColumn_left:
                            if row_feature[k]==splitLabel0_left:
                                if splitpos0_left>splitneg0_left:
                                    decidingClass=classes0_left
                                else:
                                    decidingClass=classes1_left
                            if row_feature[k]==splitLabel1_left:
                                if splitpos1_left>splitneg1_left:
                                    decidingClass=classes0_left
                                else:
                                    decidingClass=classes1_left        
                        
                            
                ##left branch not there    
                elif row_feature[j]==splitLabel0 and leftBranch==False:
                    if splitpos0>splitneg0:
                        decidingClass=classes0
                    else:
                        decidingClass=classes1
                        
                elif row_feature[j]==splitLabel1 and rightBranch==False:
                    if splitpos1>splitneg1:
                        decidingClass=classes0
                    else:
                        decidingClass=classes1
                        
                elif row_feature[j]==splitLabel1 and rightBranch==True:
                    for k in range(len(row_feature)):
                         if columnNames[k]==splitColumn_right:
                            if row_feature[k]==splitLabel0_right:
                                if splitpos0_right>splitneg0_right:
                                    decidingClass=classes0_right
                                else:
                                    decidingClass=classes1_right
                            if row_feature[k]==splitLabel1_right:
                                if splitpos1_right>splitneg1_right:
                                    decidingClass=classes0_right
                                else:
                                    decidingClass=classes1_right
        if decidingClass!=listArgs[count]:
            misclassification += 1
        count+=1
    print("error(test): " +str(misclassification/len(listArgs)))
        