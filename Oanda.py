#!/usr/bin/python3.7
#UIControler and Main init
import Constants as con
import ControllerB as b
import math
import ContOand as CO
from tkinter import *
from tkinter import ttk
from functools import partial

inicioPrograma = False

def base():
    global inicioPrograma
    start()
    CloseTt['state'] = 'normal'
    if inicioPrograma == False:
        InitOa['state'] = 'disable'
        inicioPrograma = True
        sesion.apiGetData()
        #Inicio de secion
        sesion.apiBalance()
        #Obtener el balance
        BalanceLabel['text'] = sesion.balance
        csvB['state'] = 'normal'
    else:
        feet_entry['state'] = 'normal'
        curencyCombo['state'] = 'normal'
        sesion.cerrar()
        sesion.apiBalance()
        BalanceLabel['text'] = sesion.balance
    bc2['state'] = 'normal'
    bv2['state'] = 'normal'
    print(cantidad.get(),met.get())

def start():
    bc1['state'] = 'disable'
    bc2['state'] = 'disable'
    bc3['state'] = 'disable'
    bc4['state'] = 'disable'
    bc5['state'] = 'disable'
    bc6['state'] = 'disable'

    bv1['state'] = 'disable'
    bv2['state'] = 'disable'
    bv3['state'] = 'disable'
    bv4['state'] = 'disable'
    bv5['state'] = 'disable'
    bv6['state'] = 'disable'

def Compra200():
    start()
    sesion.compra((math.floor(int(cantidad.get())/16))*32,met.get())
    bv1['state'] = 'normal'
    bv3['state'] = 'normal'

def Compra100():
    start()
    bv1['state'] = 'normal'
    bv3['state'] = 'normal'
    feet_entry['state'] = 'disable'
    curencyCombo['state'] = 'disable'
    sesion.compra((math.floor(int(cantidad.get())/16))*16,met.get())
    sesion.SetStopLoss(True)

def Compra50():
    start()
    bc4['state'] = 'normal'
    sesion.contraCompra((math.floor(int(cantidad.get())/16))*8)

def Compra25():
    start()
    bc5['state'] = 'normal'
    sesion.contraCompra((math.floor(int(cantidad.get())/16))*4)

def Compra13():
    start()
    bc6['state'] = 'normal'
    sesion.contraCompra((math.floor(int(cantidad.get())/16))*2)

def Compra6():
    sesion.contraCompra(math.floor(int(cantidad.get())/16))
    start()

def Venta200():
    start()
    bc1['state'] = 'normal'
    bc3['state'] = 'normal'
    sesion.venta((math.floor(int(cantidad.get())/16))*32,met.get())

def Venta100():
    start()
    bc1['state'] = 'normal'
    bc3['state'] = 'normal'
    feet_entry['state'] = 'disable'
    curencyCombo['state'] = 'disable'
    sesion.venta((math.floor(int(cantidad.get())/16))*16,met.get())
    sesion.SetStopLoss(False)

def Venta50():
    start()
    bv4['state'] = 'normal'
    sesion.contraVenta((math.floor(int(cantidad.get())/16))*8)

def Venta25():
    start()
    bv5['state'] = 'normal'
    sesion.contraVenta((math.floor(int(cantidad.get())/16))*4)

def Venta13():
    start()
    bv6['state'] = 'normal'
    sesion.contraVenta((math.floor(int(cantidad.get())/16))*2)

def Venta6():
    start()
    sesion.contraVenta((math.floor(int(cantidad.get())/16)))

def CSVGenerator():
    store = CO.ReportManipulation(con.USERID,con.URL)
    store.apiGetData()
    store.MainCsv(store.getTheAccounts())

def Compra(p):
    switcher = {
        200:Compra200,
        100:Compra100,
        50:Compra50,
        25:Compra25,
        13:Compra13,
        6:Compra6,
        -200:Venta200,
        -100:Venta100,
        -50:Venta50,
        -25:Venta25,
        -13:Venta13,
        -6:Venta6
    }
    opcion = switcher.get(p)
    print(opcion())

root = Tk()
root.title("Oanda client")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

cantidad = StringVar()
met = StringVar()
Sloss = StringVar()

sesion = b.OandaTransaction(con.USERID,con.URL,16,met.get(),50)

feet_entry = ttk.Entry(mainframe, width=7, textvariable=cantidad)
feet_entry.grid(column=3, row=1, sticky=(W, E))
feet_entry.insert(END, '16')

#default already set on the currency 
loss_entry = ttk.Entry(mainframe, width=7, textvariable=Sloss)
loss_entry.grid(column=2, row=6, sticky=(W, E))

#botones
#Compra
bc1 = ttk.Button(mainframe, text="200", command=partial(Compra,200),state=DISABLED)
bc1.grid(column=1, row=3, sticky=W)
bc2 = ttk.Button(mainframe, text="100", command=partial(Compra,100),state=DISABLED)
bc2.grid(column=2, row=3, sticky=W)
bc3 = ttk.Button(mainframe, text="50", command=partial(Compra,50),state=DISABLED)
bc3.grid(column=3, row=3, sticky=W)
bc4 = ttk.Button(mainframe, text="25", command=partial(Compra,25),state=DISABLED)
bc4.grid(column=4, row=3, sticky=W)
bc5 = ttk.Button(mainframe, text="13", command=partial(Compra,13),state=DISABLED)
bc5.grid(column=5, row=3, sticky=W)
bc6 = ttk.Button(mainframe, text="6", command=partial(Compra,6),state=DISABLED)
bc6.grid(column=6, row=3, sticky=W)
#venta
bv1 = ttk.Button(mainframe, text="200", command=partial(Compra,-200),state=DISABLED)
bv1.grid(column=1, row=5, sticky=W)
bv2 = ttk.Button(mainframe, text="100", command=partial(Compra,-100),state=DISABLED)
bv2.grid(column=2, row=5, sticky=W)
bv3 = ttk.Button(mainframe, text="50", command=partial(Compra,-50),state=DISABLED)
bv3.grid(column=3, row=5, sticky=W)
bv4 = ttk.Button(mainframe, text="25", command=partial(Compra,-25),state=DISABLED)
bv4.grid(column=4, row=5, sticky=W)
bv5 = ttk.Button(mainframe, text="13", command=partial(Compra,-13),state=DISABLED)
bv5.grid(column=5, row=5, sticky=W)
bv6 = ttk.Button(mainframe, text="6", command=partial(Compra,-6),state=DISABLED)
bv6.grid(column=6, row=5, sticky=W)

#comboBox
curencyCombo = ttk.Combobox(mainframe, values = con.CURRENCY,textvariable=met)
curencyCombo.grid(column=5,row=1,sticky=W, columnspan =2)
curencyCombo.current(0)

#botones primarios
InitOa = ttk.Button(mainframe, text="Iniciar", command=base)
InitOa.grid(column=1, row=1, sticky=W)
CloseTt = ttk.Button(mainframe, text="Cerrar todo", command=base,state=DISABLED)
CloseTt.grid(column=4, row=1, sticky=W)

#Etiquetas del programa
ttk.Label(mainframe, text="Cantidad:").grid(column=2, row=1, sticky=W)
ttk.Label(mainframe, text="Compra").grid(column=3, row=2, sticky=W)
ttk.Label(mainframe, text="Venta").grid(column=3, row=4, sticky=W)
ttk.Label(mainframe, text="Stop loss").grid(column=1, row=6, sticky=W)
ttk.Label(mainframe, text="Balance:").grid(column=3, row=6, sticky=W)
BalanceLabel = ttk.Label(mainframe, text='0' if ~inicioPrograma else sesion.balance)
BalanceLabel.grid(column=4, row=6, sticky=W)
ttk.Label(mainframe, text="Reporte:").grid(column=5, row=6, sticky=W)

#Creacion de CSV
csvB = ttk.Button(mainframe, text="CSV", command=CSVGenerator,state=DISABLED)
csvB.grid(column=6, row=6, sticky=W)

#testing button para revisar en terminal las operaciones abiertas, solo para tesing
ttk.Button(mainframe, text='test', command=sesion.testing).grid(column=6, row=7, sticky=W)


for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

feet_entry.focus()
#root.bind('<Return>', calculate)

root.mainloop()