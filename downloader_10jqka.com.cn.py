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
        codes = []
        with open(self.configFile, "r") as f:
            codes = f.readlines()
        return codes

    def params(self):
        "return:[[code1, kpi1, period1], ... , [codeN, kpiN, periodN]]"
        configs = []
        codes = self.stockCodes()
        for code in codes:
            for kpi in self.__kpinames:
                for period in self.__periods:
                    item = [code.strip("\n"), kpi, period]
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


    def download(self, server, path, savePath):
        "Download function"
        reqheader = {
            'User-Agent': 'Mozilla/5.0',
            'Accept-Encoding' : 'gzip,deflate',
            'Connection': 'keep-alive'
        }

        conn = http.client.HTTPConnection(server)  #python 3.x
        # conn = httplib.HTTPConnection(server)  #python 2.x
        conn.request("GET", path, None, reqheader)
        response = conn.getresponse()
        data = response.read()
        print("download:", path,  "response status:", response.status, " reason:", response.reason) #python3.x
        # print "download:", path,  "response status:", response.status, " reason:", response.reason #python2.x

        with open(savePath, "wb") as f:
            f.write(data)
        conn.close()

    def downloadReport(self):
        params = self.downloadParams(self.stockcode, self.kpiname, self.reportperiod)
        self.download(params["server"], params["path"], params["savePath"])
    
def main(stockCodeFile):
    config = Config(stockCodeFile)
    downloadParams = config.params()

    for param in downloadParams:
        stockcode, kpiname, reportperiod = param[0], param[1], param[2]
        print("Downloading, code:", stockcode, " kpi:", config.kpiMap[kpiname], " report period:", config.periodMap[reportperiod]) #python3.x
        # print "Downloading, code:", stockcode, " kpi:", config.kpiMap[kpiname], " report period:", config.periodMap[reportperiod] #python2.x
        downloader = Downloader(stockcode, kpiname, reportperiod)
        downloader.downloadReport()


if __name__ == "__main__":
    args = sys.argv
    if (len(args) < 2):
        print("Usage:", args[0], " stockCodeFile")
        exit(0)
    stockCodeFile = args[1]
    main(stockCodeFile)