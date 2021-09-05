import aanalytics2 as api2
import json
from copy import deepcopy
from itertools import *
import os
from ast import literal_eval
import pandas as pd
import time

def dataInitiator():
    api2.configure()
    logger = api2.Login() 
    logger.connector.config


def exportToCSV(dataSet, fileName):
    dataSet.to_csv(fileName, sep=',', index=False)


def readJson(jsonFile):
    with open(jsonFile, 'r', encoding='UTF8') as bla:
        jsonFile = json.loads(bla.read())

    return jsonFile


def createSegment(jsonFile):
    dataInitiator()
    cid = "samsun0"
    ags = api2.Analytics(cid)
    ags.header

    createSeg = ags.createSegment(jsonFile)
    
    return createSeg


def getJsonList(path):
    file_lst = os.listdir(path)
    # 파일 이름 리스트
    # print(file_lst)

    jsonList = []
    for file in file_lst:
        filepath = path + '/' + file
        jsonList.append(readJson(filepath))
        
    return jsonList


def getjsonDict(jsonList):
    jsonDict = {}
    for i in range(len(jsonList)):
        jsonDict[jsonList[i]['description']] = str(jsonList[i]['definition']['container'])

    return jsonDict


# input : list
def getAllCases(dataset):
    
    dataset_list = []
    for i in range(1, len(dataset)):
        #permutations
        printList = list(combinations(dataset, i+1))
        dataset_list.append(printList)

    # 중첩 리스트 제거
    dataset_list_raw = []
    for i in range(len(dataset_list)):
        for j in range(len(dataset_list[i])):
            dataset_list_raw.append(dataset_list[i][j])

    return dataset_list_raw


# List로 out
def setSegment(dataset, ifKey):
    segmentList = []
    for i in range(len(dataset)):
        if ifKey == True:
            name = '[API Test] ' + ' > '.join(dataset[i])
            segmentList.append(name)
        else:
            value = ','.join(dataset[i])
            segmentList.append(value)

    return segmentList


def getSegment(path, target_path):
    # getFileName
    jsonDict = getjsonDict(getJsonList(path))

    # key, value로 분리
    jsonKey = []
    jsonValue = []
    for key, value in jsonDict.items():
        jsonKey.append(key)
        jsonValue.append(value)

    segmentName = setSegment(getAllCases(jsonKey), True)
    segmentValue = setSegment(getAllCases(jsonValue), False)

    # template
    targetFile = readJson(target_path)
    target = deepcopy(targetFile)
    
    # 변경 후 호출
    segmentInfo = []
    for i in range(len(segmentName)):
        target['name'] = segmentName[i]
        target['definition']['container']['pred']['stream'] = list(literal_eval(segmentValue[i]))

        callSegment = createSegment(target)
        print(callSegment)
        segmentInfo.append(callSegment)

    
    exportToCSV(pd.DataFrame(segmentInfo), 'Segment_List.csv')


if __name__ == "__main__":
# 내꺼 : 200121276
# 공용계정 : 200043605

    path = ".\jsonFile\segmentApi\gmc_node"
    target_path = 'jsonFile\segmentApi\segmentApi_template.json'

    start = time.time()
    getSegment(path, target_path)
    print("Time took: ", time.time() - start)