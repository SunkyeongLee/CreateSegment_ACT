import aanalytics2 as api2
import json
import os
from itertools import *
from sqlalchemy import create_engine
import pandas as pd
import createSegment as cs

def updateSegment(segmentID, jsonFile):
    cs.dataInitiator()
    cid = "samsun0"
    ags = api2.Analytics(cid)
    ags.header

    createSeg = ags.updateSegment(segmentID, jsonFile)
    
    return createSeg

def getSegmentId(path, segmentId):

    jsonList = []
    for i in range(len(segmentId)):
        filepath = path + '\\' + segmentId[i] + '.json'
        jsonList.append(cs.readJson(filepath))
        
    return jsonList

def idToList(segmentId):
    db_connection_str = 'mysql+pymysql://root:12345@127.0.0.1:3307/segment'
    db_connection = create_engine(db_connection_str, encoding='utf-8')
    conn = db_connection.connect()

    query = """
    SELECT id FROM segment.tb_segment_list as seg
    left join segment.tb_segment_contains as cont
    on seg.name = cont.segment_name
    where segment_contains like '%%{0}%%'
    """.format(segmentId)
    
    result = pd.read_sql_query(query, conn)
    result_to_list = result['id'].values.tolist()
    conn.close()

    return result_to_list

if __name__ == "__main__":

    # updateSegment 할때 사용
    # segmentID = "s200001591_618b56fff05ace19edf4ce8c"
    # jsonFile = readJson("segmentApi\gmc_test_update\cnx_update.json")
    # print(updateSegment(segmentID, jsonFile))



    # path = 'C:\\Users\sunky\OneDrive - Concentrix Corporation\Documents\★Segment\segment_list'
    # segmentId = idToList("s200001591_56b04bf3e4b041b05a529c49")
    # print(getSegmentId(path, segmentId))

    print(cs.readJson('segmentApi\gmc_node\\1.home.json'))