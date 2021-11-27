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


def readJson(jsonFile):
    with open(jsonFile, 'r', encoding='UTF8') as bla:
        jsonFile = json.loads(bla.read())

    return jsonFile


def updateSegment(segmentID, jsonFile):
    dataInitiator()
    cid = "samsun0"
    ags = api2.Analytics(cid)
    ags.header

    createSeg = ags.updateSegment(segmentID, jsonFile)
    
    return createSeg

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

    print(idToList("s200001591_56b04bf3e4b041b05a529c49"))
    