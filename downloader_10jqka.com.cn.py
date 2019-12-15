#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author:Alan Chan
Date: 14/12 2019
Description:Download xls report from basic.10jqka.com.cn
Note: stockCodeFile, one code one line, such as:
code1
code2
codeN
"""

import sys
import time
import gzip
import json
import http.client #python 3.x
# import httplib   #python 2.x

class Config:
    """
    configure file:
    stockcode1
    stockcode2
    stockcodeN
    """
    __kpinames = ("main", "debt", "benefit", "cash") #"主要指标、资产负债表、利润表、现金流量表"
    __periods  = ("year", "report", "simple") #按年度、按报告期、按季度
    kpiMap    = {"main": "主要指标", "debt": "资产负债表", "benefit": "利润表", "cash": "现金流量表"}
    periodMap = {"year": "按年度", "report": "按报告期", "simple": "按季度"}

    def __init__(self, configFile):
        self.configFile = configFile

    def stockCodes(self):
        "return: [code1, code2 ... codeN]"
        tmps  = []
        codes = []
        with open(self.configFile, "r") as f:
            tmps = f.readlines()
        for code in tmps:
            codes.append(code.strip("\n"))
        return codes

    def params(self):
        "return:[[code1, kpi1, period1], ... , [codeN, kpiN, periodN]]"
        configs = []
        codes = self.stockCodes()
        for code in codes:
            for kpi in self.__kpinames:
                for period in self.__periods:
                    item = [code, kpi, period]
                    configs.append(item)
        return configs

class Downloader:
    def __init__(self, stockcode, kpiname, reportperiod):
        self.stockcode = stockcode
        self.kpiname = kpiname
        self.reportperiod = reportperiod

    def downloadParams(self, stockcode, kpiname, reportperiod):
        '''
        filename = stockcode + "_" + kpiname + "_" + reportperiod + ".xls"
        server = "basic.10jqka.com.cn"
        path   = "/api/stock/export.php?export=" + kpiname + "&type=" + reportperiod + "&code=" + stockcode
        '''
        savePath = stockcode + "_" + kpiname + "_" + reportperiod + ".xls"
        server = "basic.10jqka.com.cn"
        path   = "/api/stock/export.php?export=" + kpiname + "&type=" + reportperiod + "&code=" + stockcode
        return {"server": server, "path": path, "savePath":savePath}

    def download(self, server, path, requestHeader = None):
        "Download function"
        if (requestHeader == None):
            requestHeader = {
                'User-Agent': 'Mozilla/5.0',
                'Accept-Encoding' : 'gzip,deflate',
                'Connection': 'keep-alive',
                #'Referer': 'http://stockpage.10jqka.com.cn/realHead_v2.html'
            }

        conn = http.client.HTTPConnection(server)  #python 3.x
        # conn = httplib.HTTPConnection(server)  #python 2.x
        conn.request("GET", path, None, requestHeader)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        return (response.status, response.reason, data)

    def saveFile(self, data, savePath):
        with open(savePath, "wb") as f:
            f.write(data)

    def downloadReport(self):
        params = self.downloadParams(self.stockcode, self.kpiname, self.reportperiod)
        responseTuple = self.download(params["server"], params["path"])
        print("download:", params["path"],  "response status:", responseTuple[0], " reason:", responseTuple[1]) #python3.x
        # print "download:", params["path"],  "response status:", responseTuple[0], " reason:", responseTuple[1] #python2.x
        if responseTuple[0] == 200:
            self.saveFile(responseTuple[2], params["savePath"])


class PriceDownloader(Downloader):
    __server = "d.10jqka.com.cn"
    __path = ""
    def __init__(self, code, savePath):
        self.code, self.savePath = code, savePath
        self.__path = "/v2/realhead/hs_" + code + "/last.js"

    def downloadPrices(self):
        requestHeader = {
            'User-Agent': 'Mozilla/5.0',
            'Accept-Encoding' : 'gzip,deflate',
            'Connection': 'keep-alive',
            'Referer': 'http://stockpage.10jqka.com.cn/realHead_v2.html'
        }

        responseTuple = self.download(self.__server, self.__path, requestHeader)
        print("download:", self.__path,  "response status:", responseTuple[0], " reason:", responseTuple[1]) #python3.x
        # print "download:", self.__path,  "response status:", responseTuple[0], " reason:", responseTuple[1] #python2.x
        if responseTuple[0] == 200:
            jsonStr = self.getJsonStr(str(gzip.decompress(responseTuple[2]), encoding='utf-8'))
            self.saveFile(jsonStr.encode('utf-8'), self.savePath)

    def getJsonStr(self, str1):
        "get substring between ( and ) in str"
        begin = str1.find('(')
        end   = str1.find(')')
        if begin == -1 or end == -1 :
            return None
        return str1[begin + 1: end]


def main(stockCodeFile):

    #download xls files
    config = Config(stockCodeFile)
    stockCodes = config.stockCodes()
    downloadParams = config.params()

    for param in downloadParams:
        stockcode, kpiname, reportperiod = param[0], param[1], param[2]
        print("Downloading, code:", stockcode, " kpi:", config.kpiMap[kpiname], " report period:", config.periodMap[reportperiod]) #python3.x
        # print "Downloading, code:", stockcode, " kpi:", config.kpiMap[kpiname], " report period:", config.periodMap[reportperiod] #python2.x
        downloader = Downloader(stockcode, kpiname, reportperiod)
        downloader.downloadReport()

    for code in stockCodes:
        day = time.strftime("%Y%m%d", time.localtime())
        priceDownloader = PriceDownloader(code, code + "_" + day + "_price.json")
        priceDownloader.downloadPrices()


if __name__ == "__main__":
    args = sys.argv
    if (len(args) < 2):
        print("Usage:", args[0], " stockCodeFile")
        exit(0)
    stockCodeFile = args[1]
    main(stockCodeFile)