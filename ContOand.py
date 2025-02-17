#!/usr/bin/python3.7
import ControllerB as c
import math
import csv
import json
import requests
import urllib3
import os


requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
except AttributeError:
    # no pyopenssl support used / needed / available
    pass

class ReportManipulation(c.OandaBasic):
    def __init__(self, usrOanda,url):
        c.OandaBasic.__init__(self,usrOanda,url)
    def getTheAccounts(self):
        variable = requests.get(
        self.url + '/' + self.idAcc + '/orders?state=ALL&count=250',
        headers = {'Authorization':'Bearer ' + self.usrOanda}
        )
        return variable.json()
    def MainCsv(self, variable):
        var1 = variable['orders']
        var2 = len(var1)
        with open('reporte.csv', mode='w') as csv_file:
            fieldnames = ['id', 'createTime', 'type', 'instrument', 'state','units']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            for i in range(var2):
                try:
                    print(i,var1[i]['id'],var1[i]['createTime'],var1[i]['type'], var1[i]['instrument'],var1[i]['state'],var1[i]['units'])
                    writer.writerow({'id': var1[i]['id'], 'createTime': var1[i]['createTime'], 'type': var1[i]['type'], 'instrument':var1[i]['instrument'], 'state':var1[i]['state'],'units':var1[i]['units']})
                except:
                    continue
    def deleteCSV(self):
        os.remove('reporte.csv')

