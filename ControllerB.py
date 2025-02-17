#!/usr/bin/python3.7
import simplejson as json
import requests
import urllib3
import math
from decimal import Decimal


requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
except AttributeError:
    # no pyopenssl support used / needed / available
    pass

class OandaBasic(object):
    def __init__(self,usrOanda,url):
        self.usrOanda = usrOanda
        self.url = url
    def __str__(self):
        return self.usrOanda
    def apiGetData(self):
        variable = requests.get(
            self.url,
            headers = {'Authorization':'Bearer ' + self.usrOanda}
        )
        self.idAcc = variable.json()['accounts'][0]['id']
        #self.accBalance = variable.json()['accounts'][0]['balance']
        print(self.idAcc)
    def apiBalance(self):
        variable = requests.get(
        self.url + '/' + self.idAcc,
        headers = {'Authorization':'Bearer ' + self.usrOanda}
        )
        self.balance = variable.json()['account']['balance']

class OandaTransaction(OandaBasic):
    def __init__(self, usrOanda,url,units,currency,sLoss):
        OandaBasic.__init__(self,usrOanda,url)
        #OandaBasic.apiGetData()
        self.units = units
        self.currency = currency
        self.sLoss = sLoss
    def requestTransaction(self):
        x = {"order":{ "type": "MARKET","instrument":self.currency,"units":str(self.units),"timeInForce":"FOK","positionFill":"DEFAULT"}}
        y = json.dumps(x)
        variable2 = requests.post(
            self.url + '/' + str(self.idAcc) + '/orders' ,
            y,
            headers = {'Authorization':'Bearer ' + self.usrOanda,'Content-Type': 'application/json'}
        )
        print(variable2,variable2.json())
        return variable2
    def compra(self,nUnits,nCurrency,loss=50):
        self.units = nUnits
        self.currency = nCurrency
        self.sLoss = loss
        self.requestTransaction()
    def venta(self,nUnits,nCurrency,loss=50):
        self.currency = nCurrency
        self.sLoss = loss
        self.units = (nUnits)*-1
        self.requestTransaction()
    def contraCompra(self,nUnits):
        self.units = nUnits
        self.counterRequestTransaction()
    def contraVenta(self,nUnits):
        self.units = nUnits
        self.counterRequestTransaction()
    def openTrades(self):
        variable3 = requests.get(
            self.url + '/' + str(self.idAcc) + '/openTrades',
            headers = {'Authorization':'Bearer ' + self.usrOanda}
        )
        return variable3
    def cerrar(self):
        variable3 = self.openTrades()
        print(variable3.json())
        var1 = variable3.json()['trades']
        var2 = len(var1)
        for i in range(var2):
            res = var1[i]
            print(str(i) + '\t' + str(res) + '\n')
            #data = {'order':{'units': str(int(res['currentUnits'])*-1),'instrument':res['instrument'],'timeInForce': 'FOK','type': "MARKET",'positionFill': "DEFAULT"}}
            data = {'units':'ALL'}
            y=json.dumps(data)
            variable2 = requests.put(
                'https://api-fxtrade.oanda.com/v3/accounts/' + str(self.idAcc) + '/trades/' + str(res['id']) + '/close',
                y,
                headers = {'Authorization':'Bearer ' + self.usrOanda,'Content-Type': 'application/json'}
            )
            print(variable2)
    def testing(self):
        variable3 = requests.get(
            self.url + '/' + str(self.idAcc) + '/openTrades',
            headers = {'Authorization':'Bearer ' + self.usrOanda}
        )
        print(variable3,variable3.json())
    def counterRequestTransaction (self):
        variable3 = self.openTrades()
        var1 = variable3.json()['trades']
        data = {'units': str(self.units) }
        y=json.dumps(data)
        requests.put(
            'https://api-fxtrade.oanda.com/v3/accounts/' + str(self.idAcc) + '/trades/' + str(var1[0]['id']) + '/close',
            y,
            headers = {'Authorization':'Bearer ' + self.usrOanda,'Content-Type': 'application/json'}
        )
    def SetStopLoss(self, CoVFlag):
        variable3 = self.openTrades()
        var1 = variable3.json()['trades']
        StopLoss = 0
        TakeProfit = 0
        valor = float(var1[0]['price'])
        if CoVFlag:
            StopLoss = valor - 0.002
            TakeProfit = valor + 0.005
        else:
            StopLoss = valor + 0.002
            TakeProfit = valor - 0.005

        data = {"takeProfit": {"price": "{0:.5f}".format(TakeProfit) },"stopLoss": {"price": "{0:.5f}".format(StopLoss)}}
        print(data)
        y=json.dumps(data)
        holasss = requests.put(
            'https://api-fxtrade.oanda.com/v3/accounts/' + str(self.idAcc) + '/trades/' + str(var1[0]['id']) + '/orders',
            y,
            headers = {'Authorization':'Bearer ' + self.usrOanda,'Content-Type': 'application/json'}
        )
        print(holasss,holasss.json())





