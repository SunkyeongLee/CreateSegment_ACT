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

if __name__ == "__main__":

    segmentID = "s200001591_6158744f7cc94228bc427bf6"
    jsonFile = readJson("segmentApi\gmc_test_update\cnx_home.json")
    print(updateSegment(segmentID, jsonFile))