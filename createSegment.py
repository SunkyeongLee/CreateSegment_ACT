import aanalytics2 as api2
import json
from copy import deepcopy
from itertools import *
import os
from ast import literal_eval
from sqlalchemy import create_engine
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


def stackTodb(dataFrame, dbTableName):
    print(dataFrame)
    db_connection_str = 'mysql+pymysql://root:12345@127.0.0.1:3307/segment'
    db_connection = create_engine(db_connection_str, encoding='utf-8')
    conn = db_connection.connect()

    dataFrame.to_sql(name=dbTableName, con=db_connection, if_exists='append', index=False)
    print("finished")


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
        
        string = 'C:\\Users\sunky\OneDrive - Concentrix Corporation\Documents\Segment\segment_list\\' + str(callSegment["id"]) + '.json'
        with open(str(string), 'w', encoding='utf-8') as fileName:
            json.dump(target, fileName, indent="\t")

        segmentInfo.append(callSegment)

    
    exportToCSV(pd.DataFrame(segmentInfo), 'Segment_List.csv')

    segmentList = pd.DataFrame(segmentInfo).drop("owner", axis=1)
    stackTodb(segmentList, 'tb_segment_list')

if __name__ == "__main__":
# 내꺼 : 200121276
# 공용계정 : 200043605

    path = "segmentApi\gmc_node"
    target_path = 'segmentApi\segmentApi_template.json'

    start = time.time()
    getSegment(path, target_path)
    print("Time took: ", time.time() - start)

    # a = readJson("segmentApi\gmc_test_update\cnx_home.json")
    # print(createSegment(a))