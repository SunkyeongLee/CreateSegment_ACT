import aanalytics2 as api2
import json
from copy import deepcopy
from itertools import *
import csv
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

### New
def readCSV(csvFile):
    lines = open(csvFile).readlines()
    
    listCsv = []
    for line in lines[1:]:
        listCsv.append(line.split('\n')[0])

    return listCsv


def createSegment(jsonFile):
    dataInitiator()
    cid = "samsun0"
    ags = api2.Analytics(cid)
    ags.header

    createSeg = ags.createSegment(jsonFile)
    
    return createSeg

# 리스트 형식으로 return
def getJsonList(path):
    file_lst = os.listdir(path)
    # 파일 이름 리스트
    # print(file_lst)

    jsonList = []
    for file in file_lst:
        filepath = path + '/' + file
        jsonList.append(readJson(filepath))
        
    return jsonList

### New
def getJsonListCsv(path, fileLists):

    jsonList = []
    for file in fileLists:
        filepath = path + '/' + file
        jsonList.append(readJson(filepath))
        
    return jsonList


def getjsonDict(jsonList):
    jsonDict = {}
    for i in range(len(jsonList)):
        jsonDict[jsonList[i]['description']] = str(jsonList[i]['definition']['container'])

    return jsonDict


def getSegmentId(jsonList):
    jsonDict = {}
    for i in range(len(jsonList)):
        jsonDict[jsonList[i]['description']] = str(jsonList[i]['id'])

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

### NEW
def getSegment(path, target_path, fileLists):
    # getFileName
    jsonDict = getjsonDict(getJsonListCsv(path, readCSV(fileLists)))
    jsonSeg = getSegmentId(getJsonListCsv(path, readCSV(fileLists)))

    # Description : 딕셔너리를 key, value로 분리
    jsonKey = []
    jsonValue = []
    for key, value in jsonDict.items():
        jsonKey.append(key)
        jsonValue.append(value)

    # Segment ID : 딕셔너리를 key, value로 분리
    jsonSegKey = []
    jsonSegValue = []
    for key, value in jsonSeg.items():
        jsonSegKey.append(key)
        jsonSegValue.append(value)

    segmentName = setSegment(getAllCases(jsonKey), True)
    segmentValue = setSegment(getAllCases(jsonValue), False)

    # Segment
    segmentIdList = { 'segment_name': setSegment(getAllCases(jsonSegKey), True),
                    'segment_contains' : setSegment(getAllCases(jsonSegValue), False)}

    stackTodb(pd.DataFrame(segmentIdList), 'tb_segment_contains')

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
        
        # string = 'C:\\Users\Administrator\OneDrive - Concentrix Corporation\Documents\★Segment\segment_list\\' + str(callSegment["id"]) + '-' + time.strftime('%Y%m%d', time.localtime()) + '.json'
        string = 'C:\\Users\sunky\OneDrive - Concentrix Corporation\Documents\★Segment\segment_list\\' + str(callSegment["id"]) + '-' + time.strftime('%Y%m%d', time.localtime()) + '.json'
        with open(str(string), 'w', encoding='utf-8') as fileName:
            json.dump(target, fileName, indent="\t")

        segmentInfo.append(callSegment)

    
    # exportToCSV(pd.DataFrame(segmentInfo), 'Segment_List.csv')

    segmentList = pd.DataFrame(segmentInfo).drop("owner", axis=1)
    stackTodb(segmentList, 'tb_segment_list')

if __name__ == "__main__":
# 내꺼 : 200121276
# 공용계정 : 200043605

    # path = "segmentApi\gmc_node_final"
    # fileLists = "segmentApi\gmc_input_segment\cnx_seg_input.csv"
    # print(getJsonListCsv(path, readCSV(fileLists)))
    path = "segmentApi\gmc_node_final"
    fileLists = "segmentApi\gmc_input_segment\cnx_seg_input.csv"
    target_path = 'segmentApi\segmentApi_template.json'
    
    start = time.time()
    getSegment(path, target_path, fileLists)
    print("Time took: ", time.time() - start)