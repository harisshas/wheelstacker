from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
import tkinter as tk
from PIL import Image
import RPi.GPIO as GPIO
from time import sleep
from tkinter import HORIZONTAL
from tkinter import IntVar
from tkinter import W
from tkinter import N
from tkinter import CENTER
from tkinter import LEFT
from tkinter import PhotoImage
from tkinter import LabelFrame
from tkinter import messagebox as mbox
import logging
import glob
from time import strftime
import os
import subprocess
import socket
import threading
import serial
import datetime
#import tkcalendar as tkc
from tkcalendar import Calendar, DateEntry
#import ttkcalendar

ALARMONOFF=1
START=0
noofrows=3
noofcolumns=3

datetimestring = strftime('%d/%m/%y %H:%M:%S %p')
screen_shot_cmd = 'scrot -e \'mv $f /home/pi/Desktop/WheelStacker/screenshots/\''
sendscaninst="2"
#enteredwheelnumber

master = tk.Tk()
master.title("Wheel Stacker")
#master.configure(bg='black')
wheelnumbertext=StringVar()
passwordentered=StringVar()
lastscanvalues=StringVar()

logger = logging.getLogger('mylogger')
handler = logging.FileHandler('/home/pi/Desktop/WheelStacker/logs/WSTR.log')
logger.addHandler(handler)

logger.warning(datetimestring + " :: " + "starting program run")

def freezewheelbuttons():
    Cellbutton00['state']=DISABLED
    Cellbutton01['state']=DISABLED
    Cellbutton02['state']=DISABLED
    Cellbutton10['state']=DISABLED
    Cellbutton11['state']=DISABLED
    Cellbutton12['state']=DISABLED
    Cellbutton20['state']=DISABLED
    Cellbutton21['state']=DISABLED
    Cellbutton22['state']=DISABLED
    
def unfreezewheelbuttons():
    Cellbutton00['state']=NORMAL
    Cellbutton01['state']=NORMAL
    Cellbutton02['state']=NORMAL
    Cellbutton10['state']=NORMAL
    Cellbutton11['state']=NORMAL
    Cellbutton12['state']=NORMAL
    Cellbutton20['state']=NORMAL
    Cellbutton21['state']=NORMAL
    Cellbutton22['state']=NORMAL

def freezeallitems():
    Cellbutton00['state']=DISABLED
    wheelnumberbutton00['state']=DISABLED
    wheelloaddatebutton00['state']=DISABLED
    wheellockbutton00['state']=DISABLED
    wheelremarksbutton00['state']=DISABLED
    Cellbutton01['state']=DISABLED
    wheelnumberbutton01['state']=DISABLED
    wheelloaddatebutton01['state']=DISABLED
    wheellockbutton01['state']=DISABLED
    wheelremarksbutton01['state']=DISABLED
    Cellbutton02['state']=DISABLED
    wheelnumberbutton02['state']=DISABLED
    wheelloaddatebutton02['state']=DISABLED
    wheellockbutton02['state']=DISABLED
    wheelremarksbutton02['state']=DISABLED
    Cellbutton10['state']=DISABLED
    wheelnumberbutton10['state']=DISABLED
    wheelloaddatebutton10['state']=DISABLED
    wheellockbutton10['state']=DISABLED
    wheelremarksbutton10['state']=DISABLED
    Cellbutton11['state']=DISABLED
    wheelnumberbutton11['state']=DISABLED
    wheelloaddatebutton11['state']=DISABLED
    wheellockbutton11['state']=DISABLED
    wheelremarksbutton11['state']=DISABLED
    Cellbutton12['state']=DISABLED
    wheelnumberbutton12['state']=DISABLED
    wheelloaddatebutton12['state']=DISABLED
    wheellockbutton12['state']=DISABLED
    wheelremarksbutton12['state']=DISABLED
    Cellbutton20['state']=DISABLED
    wheelnumberbutton20['state']=DISABLED
    wheelloaddatebutton20['state']=DISABLED
    wheellockbutton20['state']=DISABLED
    wheelremarksbutton20['state']=DISABLED
    Cellbutton21['state']=DISABLED
    wheelnumberbutton21['state']=DISABLED
    wheelloaddatebutton21['state']=DISABLED
    wheellockbutton21['state']=DISABLED
    wheelremarksbutton21['state']=DISABLED
    Cellbutton22['state']=DISABLED
    wheelnumberbutton22['state']=DISABLED
    wheelloaddatebutton22['state']=DISABLED
    wheellockbutton22['state']=DISABLED
    wheelremarksbutton22['state']=DISABLED

def unfreezeallitems():
    Cellbutton00['state']=NORMAL
    wheelnumberbutton00['state']=NORMAL
    wheelloaddatebutton00['state']=NORMAL
    wheellockbutton00['state']=NORMAL
    wheelremarksbutton00['state']=NORMAL
    Cellbutton01['state']=NORMAL
    wheelnumberbutton01['state']=NORMAL
    wheelloaddatebutton01['state']=NORMAL
    wheellockbutton01['state']=NORMAL
    wheelremarksbutton01['state']=NORMAL
    Cellbutton02['state']=NORMAL
    wheelnumberbutton02['state']=NORMAL
    wheelloaddatebutton02['state']=NORMAL
    wheellockbutton02['state']=NORMAL
    wheelremarksbutton02['state']=NORMAL
    Cellbutton10['state']=NORMAL
    wheelnumberbutton10['state']=NORMAL
    wheelloaddatebutton10['state']=NORMAL
    wheellockbutton10['state']=NORMAL
    wheelremarksbutton10['state']=NORMAL
    Cellbutton11['state']=NORMAL
    wheelnumberbutton11['state']=NORMAL
    wheelloaddatebutton11['state']=NORMAL
    wheellockbutton11['state']=NORMAL
    wheelremarksbutton11['state']=NORMAL
    Cellbutton12['state']=NORMAL
    wheelnumberbutton12['state']=NORMAL
    wheelloaddatebutton12['state']=NORMAL
    wheellockbutton12['state']=NORMAL
    wheelremarksbutton12['state']=NORMAL
    Cellbutton20['state']=NORMAL
    wheelnumberbutton20['state']=NORMAL
    wheelloaddatebutton20['state']=NORMAL
    wheellockbutton20['state']=NORMAL
    wheelremarksbutton20['state']=NORMAL
    Cellbutton21['state']=NORMAL
    wheelnumberbutton21['state']=NORMAL
    wheelloaddatebutton21['state']=NORMAL
    wheellockbutton21['state']=NORMAL
    wheelremarksbutton21['state']=NORMAL
    Cellbutton22['state']=NORMAL
    wheelnumberbutton22['state']=NORMAL
    wheelloaddatebutton22['state']=NORMAL
    wheellockbutton22['state']=NORMAL
    wheelremarksbutton22['state']=NORMAL

def read_from_port(serial_obj):
    global START
    global lastscanvalues
    while True:
        try:
            readstring = serial_obj.readline().decode("utf-8")
            #print(readstring)
        except serial.SerialException as e:
            #There is no new data from serial port
            logger.error(datetimestring + " :: " + "Serial data read exception")
            ComErrorAlarmlabel['text']="Serial Comm Error"
            return None
        except TypeError as e:
            #Disconnect of USB->UART occured
            #print("Serial data read exception")
            logger.error(datetimestring + " :: " + "Serial data read exception")
            ComErrorAlarmlabel['text']="Serial Comm Error"
            serial_obj.port.close()
            return None
        catcode=readstring.split("*")[0]
        #print(catcode)
        if catcode == "stat":
            stringarray=readstring.split("*")[1]
            #print("stat :"+stringarray)
            logger.warning(datetimestring + " :: " + "stat :"+stringarray)
            if "complete" in stringarray:
                #print("here")
                unfreezewheelbuttons()
                sendscansignal()
                Statusbutton['text']="IDLE-STOP"
                Statusicon['image']=idleicon
            if "move back to origin" in stringarray:
                Statusbutton['text']="FINISHING"
                Statusicon['image']=movedownicon
        if catcode == "msg":
            Statusbutton['text']="RUN"
            stringarray=readstring.split("*")[1]
            if "passing through origin" in stringarray:
                Statusbutton['text']="STARTING"
                Statusicon['image']=moveupicon
            if "row seq correct" in stringarray:
                Statusbutton['text']="RUNNING X"
                Statusicon['image']=moveupicon
            if "Moved to dest X" in stringarray:
                Statusbutton['text']="RUNNING X COMPLETE"
                Statusicon['image']=moveupicon
            if "col seq correct" in stringarray:
                Statusbutton['text']="RUNNING Y"
                Statusicon['image']=moverighticon
            if "Moved to dest Y" in stringarray:
                Statusbutton['text']="RUNNING Y COMPLETE"
                Statusicon['image']=moverighticon
            if "Moved back to dest X" in stringarray:
                Statusbutton['text']="RETURN X COMPLETE"
                Statusicon['image']=moveupicon
            if "back row seq correct" in stringarray:
                Statusbutton['text']="RETURNING X"
                Statusicon['image']=movedownicon
            if "row seq correct passing through back" in stringarray:
                Statusbutton['text']="RETURNING X"
                Statusicon['image']=movedownicon
            if "Moved back to dest Y" in stringarray:
                Statusbutton['text']="RETURN Y COMPLETE"
                Statusicon['image']=movelefticon
            if "back col seq correct" in stringarray:
                Statusbutton['text']="RETURNING Y"
                Statusicon['image']=movelefticon
            #print("msg :"+stringarray)
            logger.warning(datetimestring + " :: " + "msg :"+stringarray)
        if catcode == "err":
            Statusbutton['text']="ERROR"
            Statusicon['image']=erroricon
            stringarray=readstring.split("*")[1]
            #print("err :"+stringarray)
            logger.warning(datetimestring + " :: " + "err :"+stringarray)
        elif catcode == "scan":
           if START==0: 
               unfreezeallitems()
               START=1
           try:
               stringarray=readstring.split("*")[1]
               logger.warning(datetimestring + " :: " + "lastscan :"+stringarray)
               lastscanvalues=stringarray
               #print(stringarray)
               #print(list(stringarray))
               #print(list(stringarray)[0])
               if list(stringarray)[0] == '0':
                   Cellbutton00['image']=wheelcellemptyicon
                   wheelnumberbutton00['state']=DISABLED
                   wheelloaddatebutton00['state']=DISABLED
                   wheellockbutton00['state']=DISABLED
                   wheelremarksbutton00['state']=DISABLED
                   readdatalog = open ("/home/pi/Desktop/WheelStacker/data/WSTRdata.log", "r")
                   readdatalogtemp = open ("/home/pi/Desktop/WheelStacker/data/WSTRdatatemp.log", "w")
                   lineread=True                  
                   while lineread:
                        # Read next line
                        readdatalogline = readdatalog.readline()
                        #print(readdatalogline)
                        # If line is blank, then you struck the EOF
                        if not readdatalogline :
                            readdatalog.close()
                            readdatalogtemp.close()
                            os.system("rm /home/pi/Desktop/WheelStacker/data/WSTRdata.log")
                            os.system("mv /home/pi/Desktop/WheelStacker/data/WSTRdatatemp.log /home/pi/Desktop/WheelStacker/data/WSTRdata.log")
                            lineread=False
                        else:
                            cellnumber=readdatalogline.split("*")[0]
                            if cellnumber == "00":
                                #print("deleting log")
                                logger.warning(datetimestring + " :: " + "deleting log 00")
                            else:
                                readdatalogtemp.write(readdatalogline)
               elif list(stringarray)[0] == '1':
                   Cellbutton00['image']=wheelcellfullicon
                   wheelnumberbutton00['state']=NORMAL
                   wheelloaddatebutton00['state']=NORMAL
                   wheellockbutton00['state']=NORMAL
                   wheelremarksbutton00['state']=NORMAL
                   readdatalog = open ("/home/pi/Desktop/WheelStacker/data/WSTRdata.log", "r")
                   dataavailable=False
                   lineread=True                  
                   while lineread:
                        # Read next line
                        readdatalogline = readdatalog.readline()
                        #print(readdatalogline)
                        # If line is blank, then you struck the EOF
                        if not readdatalogline :
                            # Close file
                            if dataavailable==False:
                                wheelnumberbutton00['text']="Not Available"
                                wheelloaddatebutton00['text']="Not Available"
                                wheellockbutton00['text']="Unlocked"
                                wheelremarksbutton00['text']="None"
                            readdatalog.close()
                            lineread=False
                        else:
                            cellnumber=readdatalogline.split("*")[0]
                            if cellnumber == "00":
                                dataavailable=True
                                cellwheelnumber=readdatalogline.split("*")[1]
                                if not cellwheelnumber :
                                    wheelnumberbutton00['text']="Not Available"
                                else:
                                    wheelnumberbutton00['text']=cellwheelnumber
                                cellwheelloaddate=readdatalogline.split("*")[2]
                                if not cellwheelloaddate :
                                    wheelloaddatebutton00['text']="Not Available"
                                else:
                                    wheelloaddatebutton00['text']=cellwheelloaddate   
                                cellwheellockstatus=readdatalogline.split("*")[3]
                                if not cellwheellockstatus :
                                    wheellockbutton00['text']="Unlocked"
                                else:
                                    wheellockbutton00['text']=cellwheellockstatus
                                cellwheelremarksavail=readdatalogline.split("*")[4]
                                if not cellwheelremarksavail :
                                    wheelremarksbutton00['text']="None"
                                else:
                                    wheelremarksbutton00['text']=cellwheelremarksavail
               if list(stringarray)[1] == '0':
                   Cellbutton01['image']=wheelcellemptyicon
                   wheelnumberbutton01['state']=DISABLED
                   wheelloaddatebutton01['state']=DISABLED
                   wheellockbutton01['state']=DISABLED
                   wheelremarksbutton01['state']=DISABLED
                   readdatalog = open ("/home/pi/Desktop/WheelStacker/data/WSTRdata.log", "r")
                   readdatalogtemp = open ("/home/pi/Desktop/WheelStacker/data/WSTRdatatemp.log", "w")
                   lineread=True                  
                   while lineread:
                        # Read next line
                        readdatalogline = readdatalog.readline()
                        #print(readdatalogline)
                        # If line is blank, then you struck the EOF
                        if not readdatalogline :
                            readdatalog.close()
                            readdatalogtemp.close()
                            os.system("rm /home/pi/Desktop/WheelStacker/data/WSTRdata.log")
                            os.system("mv /home/pi/Desktop/WheelStacker/data/WSTRdatatemp.log /home/pi/Desktop/WheelStacker/data/WSTRdata.log")
                            lineread=False
                        else:
                            cellnumber=readdatalogline.split("*")[0]
                            if cellnumber == "01":
                                #print("deleting log")
                                logger.warning(datetimestring + " :: " + "deleting log 01")
                            else:
                                readdatalogtemp.write(readdatalogline)
               elif list(stringarray)[1] == '1':
                   Cellbutton01['image']=wheelcellfullicon
                   wheelnumberbutton01['state']=NORMAL
                   wheelloaddatebutton01['state']=NORMAL
                   wheellockbutton01['state']=NORMAL
                   wheelremarksbutton01['state']=NORMAL
                   readdatalog = open ("/home/pi/Desktop/WheelStacker/data/WSTRdata.log", "r")
                   dataavailable=False
                   lineread=True                  
                   while lineread:
                        # Read next line
                        readdatalogline = readdatalog.readline()
                        #print(readdatalogline)
                        # If line is blank, then you struck the EOF
                        if not readdatalogline :
                            # Close file
                            if dataavailable==False:
                                wheelnumberbutton01['text']="Not Available"
                                wheelloaddatebutton01['text']="Not Available"
                                wheellockbutton01['text']="Unlocked"
                                wheelremarksbutton01['text']="None"
                            readdatalog.close()
                            lineread=False
                        else:
                            cellnumber=readdatalogline.split("*")[0]
                            #print(cellnumber)
                            if cellnumber == "01":
                                dataavailable=True
                                cellwheelnumber=readdatalogline.split("*")[1]
                                if not cellwheelnumber :
                                    wheelnumberbutton01['text']="Not Available"
                                else:
                                    wheelnumberbutton01['text']=cellwheelnumber
                                cellwheelloaddate=readdatalogline.split("*")[2]
                                if not cellwheelloaddate :
                                    wheelloaddatebutton01['text']="Not Available"
                                else:
                                    wheelloaddatebutton01['text']=cellwheelloaddate   
                                cellwheellockstatus=readdatalogline.split("*")[3]
                                if not cellwheellockstatus :
                                    wheellockbutton01['text']="Unlocked"
                                else:
                                    wheellockbutton01['text']=cellwheellockstatus
                                cellwheelremarksavail=readdatalogline.split("*")[4]
                                if not cellwheelremarksavail :
                                    wheelremarksbutton01['text']="None"
                                else:
                                    wheelremarksbutton01['text']=cellwheelremarksavail
               if list(stringarray)[2] == '0':
                   Cellbutton02['image']=wheelcellemptyicon
                   wheelnumberbutton02['state']=DISABLED
                   wheelloaddatebutton02['state']=DISABLED
                   wheellockbutton02['state']=DISABLED
                   wheelremarksbutton02['state']=DISABLED
                   readdatalog = open ("/home/pi/Desktop/WheelStacker/data/WSTRdata.log", "r")
                   readdatalogtemp = open ("/home/pi/Desktop/WheelStacker/data/WSTRdatatemp.log", "w")
                   lineread=True                  
                   while lineread:
                        # Read next line
                        readdatalogline = readdatalog.readline()
                        #print(readdatalogline)
                        # If line is blank, then you struck the EOF
                        if not readdatalogline :
                            readdatalog.close()
                            readdatalogtemp.close()
                            os.system("rm /home/pi/Desktop/WheelStacker/data/WSTRdata.log")
                            os.system("mv /home/pi/Desktop/WheelStacker/data/WSTRdatatemp.log /home/pi/Desktop/WheelStacker/data/WSTRdata.log")
                            lineread=False
                        else:
                            cellnumber=readdatalogline.split("*")[0]
                            if cellnumber == "02":
                                #print("deleting log")
                                logger.warning(datetimestring + " :: " + "deleting log 02")
                            else:
                                readdatalogtemp.write(readdatalogline)
               elif list(stringarray)[2] == '1':
                   Cellbutton02['image']=wheelcellfullicon
                   wheelnumberbutton02['state']=NORMAL
                   wheelloaddatebutton02['state']=NORMAL
                   wheellockbutton02['state']=NORMAL
                   wheelremarksbutton02['state']=NORMAL
                   readdatalog = open ("/home/pi/Desktop/WheelStacker/data/WSTRdata.log", "r")
                   dataavailable=False
                   lineread=True                  
                   while lineread:
                        # Read next line
                        readdatalogline = readdatalog.readline()
                        #print(readdatalogline)
                        # If line is blank, then you struck the EOF
                        if not readdatalogline :
                            # Close file
                            if dataavailable==False:
                                wheelnumberbutton02['text']="Not Available"
                                wheelloaddatebutton02['text']="Not Available"
                                wheellockbutton02['text']="Unlocked"
                                wheelremarksbutton02['text']="None"
                            readdatalog.close()
                            lineread=False
                        else:
                            cellnumber=readdatalogline.split("*")[0]
                            if cellnumber == "02":
                                dataavailable=True
                                cellwheelnumber=readdatalogline.split("*")[1]
                                if not cellwheelnumber :
                                    wheelnumberbutton02['text']="Not Available"
                                else:
                                    wheelnumberbutton02['text']=cellwheelnumber
                                cellwheelloaddate=readdatalogline.split("*")[2]
                                if not cellwheelloaddate :
                                    wheelloaddatebutton02['text']="Not Available"
                                else:
                                    wheelloaddatebutton02['text']=cellwheelloaddate   
                                cellwheellockstatus=readdatalogline.split("*")[3]
                                if not cellwheellockstatus :
                                    wheellockbutton02['text']="Unlocked"
                                else:
                                    wheellockbutton02['text']=cellwheellockstatus
                                cellwheelremarksavail=readdatalogline.split("*")[4]
                                if not cellwheelremarksavail :
                                    wheelremarksbutton02['text']="None"
                                else:
                                    wheelremarksbutton02['text']=cellwheelremarksavail
               if list(stringarray)[3] == '0':
                   Cellbutton10['image']=wheelcellemptyicon
                   wheelnumberbutton10['state']=DISABLED
                   wheelloaddatebutton10['state']=DISABLED
                   wheellockbutton10['state']=DISABLED
                   wheelremarksbutton10['state']=DISABLED
                   readdatalog = open ("/home/pi/Desktop/WheelStacker/data/WSTRdata.log", "r")
                   readdatalogtemp = open ("/home/pi/Desktop/WheelStacker/data/WSTRdatatemp.log", "w")
                   lineread=True                  
                   while lineread:
                        # Read next line
                        readdatalogline = readdatalog.readline()
                        #print(readdatalogline)
                        # If line is blank, then you struck the EOF
                        if not readdatalogline :
                            readdatalog.close()
                            readdatalogtemp.close()
                            os.system("rm /home/pi/Desktop/WheelStacker/data/WSTRdata.log")
                            os.system("mv /home/pi/Desktop/WheelStacker/data/WSTRdatatemp.log /home/pi/Desktop/WheelStacker/data/WSTRdata.log")
                            lineread=False
                        else:
                            cellnumber=readdatalogline.split("*")[0]
                            if cellnumber == "10":
                                #print("deleting log")
                                logger.warning(datetimestring + " :: " + "deleting log 10")
                            else:
                                readdatalogtemp.write(readdatalogline)
               elif list(stringarray)[3] == '1':
                   Cellbutton10['image']=wheelcellfullicon
                   wheelnumberbutton10['state']=NORMAL
                   wheelloaddatebutton10['state']=NORMAL
                   wheellockbutton10['state']=NORMAL
                   wheelremarksbutton10['state']=NORMAL
                   readdatalog = open ("/home/pi/Desktop/WheelStacker/data/WSTRdata.log", "r")
                   dataavailable=False
                   lineread=True                  
                   while lineread:
                        # Read next line
                        readdatalogline = readdatalog.readline()
                        #print(readdatalogline)
                        # If line is blank, then you struck the EOF
                        if not readdatalogline :
                            # Close file
                            if dataavailable==False:
                                wheelnumberbutton10['text']="Not Available"
                                wheelloaddatebutton10['text']="Not Available"
                                wheellockbutton10['text']="Unlocked"
                                wheelremarksbutton10['text']="None"
                            readdatalog.close()
                            lineread=False
                        else:
                            cellnumber=readdatalogline.split("*")[0]
                            if cellnumber == "10":
                                dataavailable=True
                                cellwheelnumber=readdatalogline.split("*")[1]
                                if not cellwheelnumber :
                                    wheelnumberbutton10['text']="Not Available"
                                else:
                                    wheelnumberbutton10['text']=cellwheelnumber
                                cellwheelloaddate=readdatalogline.split("*")[2]
                                if not cellwheelloaddate :
                                    wheelloaddatebutton10['text']="Not Available"
                                else:
                                    wheelloaddatebutton10['text']=cellwheelloaddate   
                                cellwheellockstatus=readdatalogline.split("*")[3]
                                if not cellwheellockstatus :
                                    wheellockbutton10['text']="Unlocked"
                                else:
                                    wheellockbutton10['text']=cellwheellockstatus
                                cellwheelremarksavail=readdatalogline.split("*")[4]
                                if not cellwheelremarksavail :
                                    wheelremarksbutton10['text']="None"
                                else:
                                    wheelremarksbutton10['text']=cellwheelremarksavail
               if list(stringarray)[4] == '0':
                   Cellbutton11['image']=wheelcellemptyicon
                   wheelnumberbutton11['state']=DISABLED
                   wheelloaddatebutton11['state']=DISABLED
                   wheellockbutton11['state']=DISABLED
                   wheelremarksbutton11['state']=DISABLED
                   readdatalog = open ("/home/pi/Desktop/WheelStacker/data/WSTRdata.log", "r")
                   readdatalogtemp = open ("/home/pi/Desktop/WheelStacker/data/WSTRdatatemp.log", "w")
                   lineread=True                  
                   while lineread:
                        # Read next line
                        readdatalogline = readdatalog.readline()
                        #print(readdatalogline)
                        # If line is blank, then you struck the EOF
                        if not readdatalogline :
                            readdatalog.close()
                            readdatalogtemp.close()
                            os.system("rm /home/pi/Desktop/WheelStacker/data/WSTRdata.log")
                            os.system("mv /home/pi/Desktop/WheelStacker/data/WSTRdatatemp.log /home/pi/Desktop/WheelStacker/data/WSTRdata.log")
                            lineread=False
                        else:
                            cellnumber=readdatalogline.split("*")[0]
                            if cellnumber == "11":
                                #print("deleting log")
                                logger.warning(datetimestring + " :: " + "deleting log 11")
                            else:
                                readdatalogtemp.write(readdatalogline)
               elif list(stringarray)[4] == '1':
                   Cellbutton11['image']=wheelcellfullicon
                   wheelnumberbutton11['state']=NORMAL
                   wheelloaddatebutton11['state']=NORMAL
                   wheellockbutton11['state']=NORMAL
                   wheelremarksbutton11['state']=NORMAL
                   readdatalog = open ("/home/pi/Desktop/WheelStacker/data/WSTRdata.log", "r")
                   lineread=True                  
                   dataavailable=False         
                   while lineread:
                        # Read next line
                        readdatalogline = readdatalog.readline()
                        #print(readdatalogline)
                        # If line is blank, then you struck the EOF
                        if not readdatalogline :
                            # Close file
                            if dataavailable==False:
                                wheelnumberbutton11['text']="Not Available"
                                wheelloaddatebutton11['text']="Not Available"
                                wheellockbutton11['text']="Unlocked"
                                wheelremarksbutton11['text']="None"
                            readdatalog.close()
                            lineread=False
                        else:
                            cellnumber=readdatalogline.split("*")[0]
                            #print(cellnumber)
                            if cellnumber == "11":
                                dataavailable=True
                                cellwheelnumber=readdatalogline.split("*")[1]
                                if not cellwheelnumber :
                                    wheelnumberbutton11['text']="Not Available"
                                else:
                                    wheelnumberbutton11['text']=cellwheelnumber
                                cellwheelloaddate=readdatalogline.split("*")[2]
                                if not cellwheelloaddate :
                                    wheelloaddatebutton11['text']="Not Available"
                                else:
                                    wheelloaddatebutton11['text']=cellwheelloaddate   
                                cellwheellockstatus=readdatalogline.split("*")[3]
                                if not cellwheellockstatus :
                                    wheellockbutton11['text']="Unlocked"
                                else:
                                    wheellockbutton11['text']=cellwheellockstatus
                                cellwheelremarksavail=readdatalogline.split("*")[4]
                                if not cellwheelremarksavail :
                                    wheelremarksbutton11['text']="None"
                                else:
                                    wheelremarksbutton11['text']=cellwheelremarksavail

               if list(stringarray)[5] == '0':
                   Cellbutton12['image']=wheelcellemptyicon
                   wheelnumberbutton12['state']=DISABLED
                   wheelloaddatebutton12['state']=DISABLED
                   wheellockbutton12['state']=DISABLED
                   wheelremarksbutton12['state']=DISABLED
                   readdatalog = open ("/home/pi/Desktop/WheelStacker/data/WSTRdata.log", "r")
                   readdatalogtemp = open ("/home/pi/Desktop/WheelStacker/data/WSTRdatatemp.log", "w")
                   lineread=True                  
                   while lineread:
                        # Read next line
                        readdatalogline = readdatalog.readline()
                        #print(readdatalogline)
                        # If line is blank, then you struck the EOF
                        if not readdatalogline :
                            readdatalog.close()
                            readdatalogtemp.close()
                            os.system("rm /home/pi/Desktop/WheelStacker/data/WSTRdata.log")
                            os.system("mv /home/pi/Desktop/WheelStacker/data/WSTRdatatemp.log /home/pi/Desktop/WheelStacker/data/WSTRdata.log")
                            lineread=False
                        else:
                            cellnumber=readdatalogline.split("*")[0]
                            if cellnumber == "12":
                                #print("deleting log")
                                logger.warning(datetimestring + " :: " + "deleting log 12")
                            else:
                                readdatalogtemp.write(readdatalogline)
               elif list(stringarray)[5] == '1':
                   Cellbutton12['image']=wheelcellfullicon
                   wheelnumberbutton12['state']=NORMAL
                   wheelloaddatebutton12['state']=NORMAL
                   wheellockbutton12['state']=NORMAL
                   wheelremarksbutton12['state']=NORMAL
                   readdatalog = open ("/home/pi/Desktop/WheelStacker/data/WSTRdata.log", "r")
                   lineread=True
                   dataavailable=False
                   while lineread:
                        # Read next line
                        readdatalogline = readdatalog.readline()
                        #print(readdatalogline)
                        # If line is blank, then you struck the EOF
                        if not readdatalogline :
                            # Close file
                            if dataavailable==False:
                                wheelnumberbutton12['text']="Not Available"
                                wheelloaddatebutton12['text']="Not Available"
                                wheellockbutton12['text']="Unlocked"
                                wheelremarksbutton12['text']="None"
                            readdatalog.close()
                            #print("closing file")
                            lineread=False
                        else:
                            cellnumber=readdatalogline.split("*")[0]
                            #print(cellnumber)
                            if cellnumber == "12":
                                dataavailable=True
                                cellwheelnumber=readdatalogline.split("*")[1]
                                if not cellwheelnumber :
                                    wheelnumberbutton12['text']="Not Available"
                                else:
                                    wheelnumberbutton12['text']=cellwheelnumber
                                cellwheelloaddate=readdatalogline.split("*")[2]
                                if not cellwheelloaddate :
                                    wheelloaddatebutton12['text']="Not Available"
                                else:
                                    wheelloaddatebutton12['text']=cellwheelloaddate   
                                cellwheellockstatus=readdatalogline.split("*")[3]
                                if not cellwheellockstatus :
                                    wheellockbutton12['text']="Unlocked"
                                else:
                                    wheellockbutton12['text']=cellwheellockstatus
                                cellwheelremarksavail=readdatalogline.split("*")[4]
                                if not cellwheelremarksavail :
                                    wheelremarksbutton12['text']="None"
                                else:
                                    wheelremarksbutton12['text']=cellwheelremarksavail

               if list(stringarray)[6] == '0':
                   Cellbutton20['image']=wheelcellemptyicon
                   wheelnumberbutton20['state']=DISABLED
                   wheelloaddatebutton20['state']=DISABLED
                   wheellockbutton20['state']=DISABLED
                   wheelremarksbutton20['state']=DISABLED
                   readdatalog = open ("/home/pi/Desktop/WheelStacker/data/WSTRdata.log", "r")
                   readdatalogtemp = open ("/home/pi/Desktop/WheelStacker/data/WSTRdatatemp.log", "w")
                   lineread=True                  
                   while lineread:
                        # Read next line
                        readdatalogline = readdatalog.readline()
                        #print(readdatalogline)
                        # If line is blank, then you struck the EOF
                        if not readdatalogline :
                            readdatalog.close()
                            readdatalogtemp.close()
                            os.system("rm /home/pi/Desktop/WheelStacker/data/WSTRdata.log")
                            os.system("mv /home/pi/Desktop/WheelStacker/data/WSTRdatatemp.log /home/pi/Desktop/WheelStacker/data/WSTRdata.log")
                            lineread=False
                        else:
                            cellnumber=readdatalogline.split("*")[0]
                            if cellnumber == "20":
                                #print("deleting log")
                                logger.warning(datetimestring + " :: " + "deleting log 20")
                            else:
                                readdatalogtemp.write(readdatalogline)
               elif list(stringarray)[6] == '1':
                   Cellbutton20['image']=wheelcellfullicon
                   wheelnumberbutton20['state']=NORMAL
                   wheelloaddatebutton20['state']=NORMAL
                   wheellockbutton20['state']=NORMAL
                   wheelremarksbutton20['state']=NORMAL
                   readdatalog = open ("/home/pi/Desktop/WheelStacker/data/WSTRdata.log", "r")
                   dataavailable=False
                   lineread=True                  
                   while lineread:
                        # Read next line
                        readdatalogline = readdatalog.readline()
                        #print(readdatalogline)
                        # If line is blank, then you struck the EOF
                        if not readdatalogline :
                            # Close file
                            if dataavailable==False:
                                wheelnumberbutton20['text']="Not Available"
                                wheelloaddatebutton20['text']="Not Available"
                                wheellockbutton20['text']="Unlocked"
                                wheelremarksbutton20['text']="None"
                            readdatalog.close()
                            lineread=False
                        else:
                            cellnumber=readdatalogline.split("*")[0]
                            if cellnumber == "20":
                                dataavailable=True
                                cellwheelnumber=readdatalogline.split("*")[1]
                                if not cellwheelnumber :
                                    wheelnumberbutton20['text']="Not Available"
                                else:
                                    wheelnumberbutton20['text']=cellwheelnumber
                                cellwheelloaddate=readdatalogline.split("*")[2]
                                if not cellwheelloaddate :
                                    wheelloaddatebutton20['text']="Not Available"
                                else:
                                    wheelloaddatebutton20['text']=cellwheelloaddate   
                                cellwheellockstatus=readdatalogline.split("*")[3]
                                if not cellwheellockstatus :
                                    wheellockbutton20['text']="Unlocked"
                                else:
                                    wheellockbutton20['text']=cellwheellockstatus
                                cellwheelremarksavail=readdatalogline.split("*")[4]
                                if not cellwheelremarksavail :
                                    wheelremarksbutton20['text']="None"
                                else:
                                    wheelremarksbutton20['text']=cellwheelremarksavail
               if list(stringarray)[7] == '0':
                   Cellbutton21['image']=wheelcellemptyicon
                   wheelnumberbutton21['state']=DISABLED
                   wheelloaddatebutton21['state']=DISABLED
                   wheellockbutton21['state']=DISABLED
                   wheelremarksbutton21['state']=DISABLED
                   readdatalog = open ("/home/pi/Desktop/WheelStacker/data/WSTRdata.log", "r")
                   readdatalogtemp = open ("/home/pi/Desktop/WheelStacker/data/WSTRdatatemp.log", "w")
                   lineread=True                  
                   while lineread:
                        # Read next line
                        readdatalogline = readdatalog.readline()
                        #print(readdatalogline)
                        # If line is blank, then you struck the EOF
                        if not readdatalogline :
                            readdatalog.close()
                            readdatalogtemp.close()
                            os.system("rm /home/pi/Desktop/WheelStacker/data/WSTRdata.log")
                            os.system("mv /home/pi/Desktop/WheelStacker/data/WSTRdatatemp.log /home/pi/Desktop/WheelStacker/data/WSTRdata.log")
                            lineread=False
                        else:
                            cellnumber=readdatalogline.split("*")[0]
                            if cellnumber == "21":
                                #print("deleting log")
                                logger.warning(datetimestring + " :: " + "deleting log 21")
                            else:
                                readdatalogtemp.write(readdatalogline)
               elif list(stringarray)[7] == '1':
                   Cellbutton21['image']=wheelcellfullicon
                   wheelnumberbutton21['state']=NORMAL
                   wheelloaddatebutton21['state']=NORMAL
                   wheellockbutton21['state']=NORMAL
                   wheelremarksbutton21['state']=NORMAL
                   readdatalog = open ("/home/pi/Desktop/WheelStacker/data/WSTRdata.log", "r")
                   dataavailable=False
                   lineread=True                  
                   while lineread:
                        # Read next line
                        readdatalogline = readdatalog.readline()
                        #print(readdatalogline)
                        # If line is blank, then you struck the EOF
                        if not readdatalogline :
                            # Close file
                            if dataavailable==False:
                                wheelnumberbutton21['text']="Not Available"
                                wheelloaddatebutton21['text']="Not Available"
                                wheellockbutton21['text']="Unlocked"
                                wheelremarksbutton21['text']="None"
                            readdatalog.close()
                            lineread=False
                        else:
                            cellnumber=readdatalogline.split("*")[0]
                            if cellnumber == "21":
                                dataavailable=True
                                cellwheelnumber=readdatalogline.split("*")[1]
                                if not cellwheelnumber :
                                    wheelnumberbutton21['text']="Not Available"
                                else:
                                    wheelnumberbutton21['text']=cellwheelnumber
                                cellwheelloaddate=readdatalogline.split("*")[2]
                                if not cellwheelloaddate :
                                    wheelloaddatebutton21['text']="Not Available"
                                else:
                                    wheelloaddatebutton21['text']=cellwheelloaddate   
                                cellwheellockstatus=readdatalogline.split("*")[3]
                                if not cellwheellockstatus :
                                    wheellockbutton21['text']="Unlocked"
                                else:
                                    wheellockbutton21['text']=cellwheellockstatus
                                cellwheelremarksavail=readdatalogline.split("*")[4]
                                if not cellwheelremarksavail :
                                    wheelremarksbutton21['text']="None"
                                else:
                                    wheelremarksbutton21['text']=cellwheelremarksavail
               if list(stringarray)[8] == '0':
                   Cellbutton22['image']=wheelcellemptyicon
                   wheelnumberbutton22['state']=DISABLED
                   wheelloaddatebutton22['state']=DISABLED
                   wheellockbutton22['state']=DISABLED
                   wheelremarksbutton22['state']=DISABLED
                   readdatalog = open ("/home/pi/Desktop/WheelStacker/data/WSTRdata.log", "r")
                   readdatalogtemp = open ("/home/pi/Desktop/WheelStacker/data/WSTRdatatemp.log", "w")
                   lineread=True                  
                   while lineread:
                        # Read next line
                        readdatalogline = readdatalog.readline()
                        #print(readdatalogline)
                        # If line is blank, then you struck the EOF
                        if not readdatalogline :
                            readdatalog.close()
                            readdatalogtemp.close()
                            os.system("rm /home/pi/Desktop/WheelStacker/data/WSTRdata.log")
                            os.system("mv /home/pi/Desktop/WheelStacker/data/WSTRdatatemp.log /home/pi/Desktop/WheelStacker/data/WSTRdata.log")
                            lineread=False
                        else:
                            cellnumber=readdatalogline.split("*")[0]
                            if cellnumber == "22":
                                #print("deleting log")
                                logger.warning(datetimestring + " :: " + "deleting log 22")
                            else:
                                readdatalogtemp.write(readdatalogline)
               elif list(stringarray)[8] == '1':
                   Cellbutton22['image']=wheelcellfullicon
                   wheelnumberbutton22['state']=NORMAL
                   wheelloaddatebutton22['state']=NORMAL
                   wheellockbutton22['state']=NORMAL
                   wheelremarksbutton22['state']=NORMAL
                   readdatalog = open ("/home/pi/Desktop/WheelStacker/data/WSTRdata.log", "r")
                   dataavailable=False
                   lineread=True                  
                   while lineread:
                        # Read next line
                        readdatalogline = readdatalog.readline()
                        #print(readdatalogline)
                        # If line is blank, then you struck the EOF
                        if not readdatalogline :
                            # Close file
                            if dataavailable==False:
                                wheelnumberbutton22['text']="Not Available"
                                wheelloaddatebutton22['text']="Not Available"
                                wheellockbutton22['text']="Unlocked"
                                wheelremarksbutton22['text']="None"
                            readdatalog.close()
                            lineread=False
                        else:
                            cellnumber=readdatalogline.split("*")[0]
                            if cellnumber == "22":
                                dataavailable=True
                                cellwheelnumber=readdatalogline.split("*")[1]
                                if not cellwheelnumber :
                                    wheelnumberbutton22['text']="Not Available"
                                else:
                                    wheelnumberbutton22['text']=cellwheelnumber
                                cellwheelloaddate=readdatalogline.split("*")[2]
                                if not cellwheelloaddate :
                                    wheelloaddatebutton22['text']="Not Available"
                                else:
                                    wheelloaddatebutton22['text']=cellwheelloaddate   
                                cellwheellockstatus=readdatalogline.split("*")[3]
                                if not cellwheellockstatus :
                                    wheellockbutton22['text']="Unlocked"
                                else:
                                    wheellockbutton22['text']=cellwheellockstatus
                                cellwheelremarksavail=readdatalogline.split("*")[4]
                                if not cellwheelremarksavail :
                                    wheelremarksbutton22['text']="None"
                                else:
                                    wheelremarksbutton22['text']=cellwheelremarksavail

                   
           except Exception as e:
               logger.error(datetimestring + " :: " + "Serial data read & split exception")

def sendscansignal():
    try:
       ser.write(sendscaninst.encode("utf-8"))
    #    print(sendscaninst)
    except Exception as e:
       #print("Serial data write exception")
       logger.error(datetimestring + " :: " + "Serial data write exception-scan instruction")
       ComErrorAlarmlabel['text']="Serial Comm Error"
        
def wheelcellselect(*args):
    global lastscanvalues
    #print(lastscanvalues)
    #print(lastscanvalues[3*args[0]+args[1]])
    instruction=lastscanvalues[3*args[0]+args[1]]
    sendstring=str(instruction)+"*"+str(args[0])+"*"+str(args[1])
    #print(sendstring)
    #print("x: "+str(args[0])+" y: "+str(args[1])) 
    logger.error(datetimestring + " :: " + "selected cell:"+ str(args[0]) + "x" + str(args[1]))
    try:
       ser.write(sendstring.encode("utf-8"))
       freezewheelbuttons()
    #    print(sendscaninst)
    except Exception as e:
       #print("Serial data write exception")
       logger.error(datetimestring + " :: " + "Serial data write exception-movetoxy instruction")
       ComErrorAlarmlabel['text']="Serial Comm Error"
    
    #logger.error("cell selected")
    
def wheelnumberbuttonselect(*args):
    #print("x: "+str(args[0])+" y: "+str(args[1])) 
    #logger.error(datetimestring + " :: " + "selected wheel number button cell:"+ str(args[0]) + "x" + str(args[1]))
    def wheelnumbereditsave(*args):
       #print("wheel number:"+Wheelnumberentrybutton.get())
       readdatalog = open ("/home/pi/Desktop/WheelStacker/data/WSTRdata.log", "r")
       readdatalogtemp = open ("/home/pi/Desktop/WheelStacker/data/WSTRdatatemp.log", "w")
       lineread=True
       datafound=False
       while lineread:
            # Read next line
            readdatalogline = readdatalog.readline()
            #print(readdatalogline)
            # If line is blank, then you struck the EOF
            if not readdatalogline :
                if datafound==False:
                    newstringinput=str(args[0]) + "" + str(args[1])+"*"+Wheelnumberentrybutton.get()+"*Not Available*UnLocked*None*No remarks"
                    readdatalogtemp.write(newstringinput)
                readdatalog.close()
                readdatalogtemp.close()
                os.system("rm /home/pi/Desktop/WheelStacker/data/WSTRdata.log")
                os.system("mv /home/pi/Desktop/WheelStacker/data/WSTRdatatemp.log /home/pi/Desktop/WheelStacker/data/WSTRdata.log")
                lineread=False
                sendscansignal()
                wheelnumbereditWindow.destroy()
            else:
                cellnumber=readdatalogline.split("*")[0]
                if cellnumber == str(args[0]) + "" + str(args[1]):
                    datafound=True
                    cellnumber=readdatalogline.split("*")[0]
                    wheelnumber=readdatalogline.split("*")[1]
                    wheelloaddate=readdatalogline.split("*")[2]
                    wheellockstatus=readdatalogline.split("*")[3]
                    remarkavailstatus=readdatalogline.split("*")[4]
                    remarkstext=readdatalogline.split("*")[5]
                    newstringinput=cellnumber+"*"+Wheelnumberentrybutton.get()+"*"+wheelloaddate+"*"+wheellockstatus+"*"+remarkavailstatus+"*"+remarkstext
                    readdatalogtemp.write(newstringinput)
                    #print("deleting log")
                    logger.warning(datetimestring + " :: " + "editing log-"+str(args[0]) + "" + str(args[1])+"changing:"+wheelnumber+"to:"+Wheelnumberentrybutton.get())
                else:
                    readdatalogtemp.write(readdatalogline)
        
    wheelnumbertext=""
    wheelnumbereditWindow = Toplevel(master) 
    wheelnumbereditWindow.title("  ")
    #wheelnumbereditWindow.wm_attributes('-type', 'splash')
    wheelnumbereditWindow.configure(bg='gray90')
    wheelnumbereditWindow.resizable(0,0)
    #wheelnumbereditWindow.attributes('-toolwindow', True)
    #wheelnumbereditWindow.overredirect(True)
    wheelnumbereditWindowWidth=300
    wheelnumbereditWindowHeight=150
    wheelnumbereditWindow.geometry('{}x{}+{}+{}'.format(wheelnumbereditWindowWidth, wheelnumbereditWindowHeight, int(master.winfo_screenwidth()/2)-int(wheelnumbereditWindowWidth/2), int(master.winfo_screenheight()/2)-int(wheelnumbereditWindowHeight/2)))
    wheelnumbereditWindowLabel = tk.Label(wheelnumbereditWindow, text="Edit Wheel Number",font=('Helvetica', 15, 'bold'), bg='gray90')
    wheelnumbereditWindowLabel['width']=27
    wheelnumbereditWindowLabel['height']=1
    wheelnumbereditWindowLabel.grid(row = 0, column = 0)
    wheelnumberedcellnumberLabel = tk.Label(wheelnumbereditWindow, text="Cell:"+ str(args[0]) + "x" + str(args[1]),font=('Helvetica', 13), bg='gray90')
    wheelnumberedcellnumberLabel['width']=27
    wheelnumberedcellnumberLabel['height']=1
    wheelnumberedcellnumberLabel.grid(row = 1, column = 0)
    Wheelnumberentrybutton = tk.Entry(wheelnumbereditWindow, font=('Helvetica', 15, 'bold'), width=25, textvariable=wheelnumbertext)
    Wheelnumberentrybutton.grid(row=2, column=0)
    Blanklabel = tk.Label(wheelnumbereditWindow, text="", font=('Helvetica', 10, 'bold'), bd=0, height=1, width=15, bg='gray90')
    Blanklabel.grid(row=3, column=0)
    Wheelnumberenterbutton = tk.Button(wheelnumbereditWindow, text="Enter & Exit", font=('Helvetica', 15, 'bold'), bd=1, height=1, width=15, command=lambda:wheelnumbereditsave(args[0],args[1]))
    Wheelnumberenterbutton.grid(row=4, column=0)
    
    readdatalog = open ("/home/pi/Desktop/WheelStacker/data/WSTRdata.log", "r")
    dataavailable=False
    lineread=True                  
    while lineread:
        readdatalogline = readdatalog.readline()
        if not readdatalogline :
           if dataavailable==False:
               Wheelnumberentrybutton.insert(0,"")
               #print("data not available")
           lineread=False
        else:
           cellnumber=readdatalogline.split("*")[0]
           if cellnumber == str(args[0]) + "" + str(args[1]):
                dataavailable=True
                cellwheelnumber=readdatalogline.split("*")[1]
                Wheelnumberentrybutton.insert(0,cellwheelnumber)
                #print("remarks availablity:"+cellremarksavail)
    
def wheelloaddatebuttonselect(*args):
    
    def wheelloaddateeditsave(*args):
       #print("x: "+str(args[0])+" y: "+str(args[1]))
       #now=datetime.datetime.now()
       #datetimestringtemp = str(now.year)+"-"+str(now.month)+"-"+str(now.day)
       #print(datetimestringtemp)
       #print(cal.selection_get())
       #print(datetime.datetime.strptime(str(cal.selection_get()), '%Y-%m-%d').strftime('%d-%m-%Y'))
       dateselected=datetime.datetime.strptime(str(cal.selection_get()),'%Y-%m-%d').strftime('%d-%m-%Y')
       #print(dateselected)
       readdatalog = open ("/home/pi/Desktop/WheelStacker/data/WSTRdata.log", "r")
       readdatalogtemp = open ("/home/pi/Desktop/WheelStacker/data/WSTRdatatemp.log", "w")
       lineread=True
       datafound=False
       while lineread:
            # Read next line
            readdatalogline = readdatalog.readline()
            #print(readdatalogline)
            # If line is blank, then you struck the EOF
            if not readdatalogline :
                if datafound==False:
                    newstringinput=str(args[0]) + "" + str(args[1])+"*Not Available*"+dateselected+"*UnLocked*None*No remarks"
                    readdatalogtemp.write(newstringinput)
                readdatalog.close()
                readdatalogtemp.close()
                os.system("rm /home/pi/Desktop/WheelStacker/data/WSTRdata.log")
                os.system("mv /home/pi/Desktop/WheelStacker/data/WSTRdatatemp.log /home/pi/Desktop/WheelStacker/data/WSTRdata.log")
                lineread=False
                sendscansignal()
                wheelloaddateeditWindow.destroy()
            else:
                cellnumber=readdatalogline.split("*")[0]
                if cellnumber == str(args[0]) + "" + str(args[1]):
                    datafound=True
                    cellnumber=readdatalogline.split("*")[0]
                    wheelnumber=readdatalogline.split("*")[1]
                    wheelloaddate=readdatalogline.split("*")[2]
                    wheellockstatus=readdatalogline.split("*")[3]
                    remarkavailstatus=readdatalogline.split("*")[4]
                    remarkstext=readdatalogline.split("*")[5]
                    newstringinput=cellnumber+"*"+wheelnumber+"*"+dateselected+"*"+wheellockstatus+"*"+remarkavailstatus+"*"+remarkstext
                    readdatalogtemp.write(newstringinput)
                    
                    logger.warning(datetimestring + " :: " + "editing log-"+str(args[0]) + "" + str(args[1])+"changing:"+wheelloaddate+"to:"+dateselected)
                else:
                    readdatalogtemp.write(readdatalogline)
       
    #logger.error(datetimestring + " :: " + "selected wheel load date button cell:"+ str(args[0]) + "x" + str(args[1]))
    #logger.error("cell selected")
    wheelloaddateeditWindow = Toplevel(master) 
    wheelloaddateeditWindow.title("  ")
    #wheelnumbereditWindow.wm_attributes('-type', 'splash')
    wheelloaddateeditWindow.configure(bg='gray90')
    wheelloaddateeditWindow.resizable(0,0)
    #wheelnumbereditWindow.attributes('-toolwindow', True)
    #wheelnumbereditWindow.overredirect(True)
    wheelloaddateeditWindowWidth=325
    wheelloaddateeditWindowHeight=350
    wheelloaddateeditWindow.geometry('{}x{}+{}+{}'.format(wheelloaddateeditWindowWidth, wheelloaddateeditWindowHeight, int(master.winfo_screenwidth()/2)-int(wheelloaddateeditWindowWidth/2), int(master.winfo_screenheight()/2)-int(wheelloaddateeditWindowHeight/2)))
    wheelloaddateeditWindowLabel = tk.Label(wheelloaddateeditWindow, text="Edit Wheel Load date",font=('Helvetica', 15, 'bold'), bg='gray90')
    wheelloaddateeditWindowLabel['width']=27
    wheelloaddateeditWindowLabel['height']=1
    wheelloaddateeditWindowLabel.grid(row = 0, column = 0)
    wheelloaddateeditcellnumberLabel = tk.Label(wheelloaddateeditWindow, text="Cell:"+ str(args[0]) + "x" + str(args[1]),font=('Helvetica', 13), bg='gray90')
    wheelloaddateeditcellnumberLabel['width']=27
    wheelloaddateeditcellnumberLabel['height']=1
    wheelloaddateeditcellnumberLabel.grid(row = 1, column = 0)
    #cal = Calendar(wheelloaddateeditWindow, font="Arial 14", selectmode='day', cursor="hand1", year=2018, month=2, day=5)
    dayselected=IntVar()
    monthselected=IntVar()
    yearselected=IntVar()
    now=datetime.datetime.now()
    dayselected=now.day
    monthselected=now.month
    yearselected=now.year
    cal = Calendar(wheelloaddateeditWindow, font="Arial 14", selectmode='day', year=yearselected, month=monthselected, day=dayselected)
    cal.grid(row = 2, column = 0)
    Blanklabel = tk.Label(wheelloaddateeditWindow, text="", font=('Helvetica', 10, 'bold'), bd=0, height=1, width=15, bg='gray90')
    Blanklabel.grid(row=3, column=0)
    wheelloaddateenterbutton = tk.Button(wheelloaddateeditWindow, text="Enter & Exit", font=('Helvetica', 15, 'bold'), bd=1, height=1, width=15, command=lambda:wheelloaddateeditsave(args[0],args[1]))
    wheelloaddateenterbutton.grid(row=4, column=0)
    
def celllockbuttonselect(*args):
    passwordentered=""
    intention=StringVar()
    def checkpassword(*args):
        readdatalog = open ("/home/pi/Desktop/WheelStacker/data/pwd.log", "r")
        readdatalogline = readdatalog.readline()
        #print(readdatalogline)
        #print(passwordentry.get())
        if not readdatalogline :
           logger.error(datetimestring + " :: " + "password file not found")
        else:
            if readdatalogline==passwordentry.get():
               #print("login success")
               readdatalog = open ("/home/pi/Desktop/WheelStacker/data/WSTRdata.log", "r")
               readdatalogtemp = open ("/home/pi/Desktop/WheelStacker/data/WSTRdatatemp.log", "w")
               lineread=True
               datafound=False
               while lineread:
                    # Read next line
                    readdatalogline = readdatalog.readline()
                    #print(readdatalogline)
                    # If line is blank, then you struck the EOF
                    if not readdatalogline :
                        if datafound==False:
                            newstringinput=str(args[0]) + "" + str(args[1])+"*Not Available*Not Available*"+intention+"*None*No remarks"
                            readdatalogtemp.write(newstringinput)
                        readdatalog.close()
                        readdatalogtemp.close()
                        os.system("rm /home/pi/Desktop/WheelStacker/data/WSTRdata.log")
                        os.system("mv /home/pi/Desktop/WheelStacker/data/WSTRdatatemp.log /home/pi/Desktop/WheelStacker/data/WSTRdata.log")
                        lineread=False
                        sendscansignal()
                        celllockstatuseditWindow.destroy()
                    else:
                        cellnumber=readdatalogline.split("*")[0]
                        if cellnumber == str(args[0]) + "" + str(args[1]):
                            datafound=True
                            cellnumber=readdatalogline.split("*")[0]
                            wheelnumber=readdatalogline.split("*")[1]
                            wheelloaddate=readdatalogline.split("*")[2]
                            wheellockstatus=readdatalogline.split("*")[3]
                            remarkavailstatus=readdatalogline.split("*")[4]
                            remarkstext=readdatalogline.split("*")[5]
                            newstringinput=cellnumber+"*"+wheelnumber+"*"+wheelloaddate+"*"+intention+"*"+remarkavailstatus+"*"+remarkstext
                            readdatalogtemp.write(newstringinput)
                            logger.warning(datetimestring + " :: " + "editing log-"+str(args[0]) + "" + str(args[1])+"changing:"+wheellockstatus+"to:"+intention)
                        else:
                            readdatalogtemp.write(readdatalogline)
            else:
                #print("login fail")
                Blanklabel['text']="Invalid password"
                
    #print("x: "+str(args[0])+" y: "+str(args[1])) 
    #logger.error(datetimestring + " :: " + "selected cell lock button cell:"+ str(args[0]) + "x" + str(args[1]))
    #logger.error("cell selected")
    celllockstatuseditWindow = Toplevel(master) 
    celllockstatuseditWindow.title("  ")
    #wheelnumbereditWindow.wm_attributes('-type', 'splash')
    celllockstatuseditWindow.configure(bg='gray90')
    celllockstatuseditWindow.resizable(0,0)
    #wheelnumbereditWindow.attributes('-toolwindow', True)
    #wheelnumbereditWindow.overredirect(True)
    celllockstatuseditWindowWidth=300
    celllockstatuseditWindowHeight=350
    celllockstatuseditWindow.geometry('{}x{}+{}+{}'.format(celllockstatuseditWindowWidth, celllockstatuseditWindowHeight, int(master.winfo_screenwidth()/2)-int(celllockstatuseditWindowWidth/2), int(master.winfo_screenheight()/2)-int(celllockstatuseditWindowHeight/2)))
    celllockstatuseditWindowLabel = tk.Label(celllockstatuseditWindow, text="Edit Cell Lock Status",font=('Helvetica', 15, 'bold'), bg='gray90')
    celllockstatuseditWindowLabel['width']=27
    celllockstatuseditWindowLabel['height']=1
    celllockstatuseditWindowLabel.grid(row = 0, column = 0)
    celllockstatusediteditcellnumberLabel = tk.Label(celllockstatuseditWindow, text="Cell:"+ str(args[0]) + "x" + str(args[1]),font=('Helvetica', 13), bg='gray90')
    celllockstatusediteditcellnumberLabel['width']=27
    celllockstatusediteditcellnumberLabel['height']=1
    celllockstatusediteditcellnumberLabel.grid(row = 1, column = 0)
    celllockstatusediticonLabel = tk.Label(celllockstatuseditWindow, text="", image=lockopenpic, bg='gray90')
    celllockstatusediticonLabel['width']=155
    celllockstatusediticonLabel['height']=155
    celllockstatusediticonLabel.grid(row = 2, column = 0)
    celllockstatuseditstatusLabel = tk.Label(celllockstatuseditWindow, text="Locked",font=('Helvetica', 15, 'bold'), bg='gray90')
    celllockstatuseditstatusLabel['width']=27
    celllockstatuseditstatusLabel['height']=1
    celllockstatuseditstatusLabel.grid(row = 3, column = 0)
    celllockpasswordLabel = tk.Label(celllockstatuseditWindow, text="Enter password to unlock",font=('Helvetica', 13), bg='gray90')
    celllockpasswordLabel['width']=27
    celllockpasswordLabel['height']=1
    celllockpasswordLabel.grid(row = 4, column = 0)
    passwordentry = tk.Entry(celllockstatuseditWindow, font=('Helvetica', 15, 'bold'), width=25, textvariable=passwordentered, show="*")
    passwordentry.grid(row=5, column=0)
    Blanklabel = tk.Label(celllockstatuseditWindow, text="", font=('Helvetica', 10), bd=0, height=1, width=15, bg='gray90', fg='red')
    Blanklabel.grid(row=6, column=0)
    Lockunlockbutton = tk.Button(celllockstatuseditWindow, text="Lock", font=('Helvetica', 15, 'bold'), bd=1, height=1, width=15, command=lambda:checkpassword(args[0],args[1]))
    Lockunlockbutton.grid(row=7, column=0)
    
    readdatalog = open ("/home/pi/Desktop/WheelStacker/data/WSTRdata.log", "r")
    dataavailable=False
    lineread=True                  
    while lineread:
        readdatalogline = readdatalog.readline()
        if not readdatalogline :
           if dataavailable==False:
               celllockstatusediticonLabel['image']=lockopenpic
               celllockstatuseditstatusLabel['text']="UnLocked"
               celllockpasswordLabel['text']="Enter password to lock"
               Lockunlockbutton['text']="Lock"
               intention="Locked"
               #print("data not available")
           lineread=False
        else:
           cellnumber=readdatalogline.split("*")[0]
           if cellnumber == str(args[0]) + "" + str(args[1]):
                dataavailable=True
                celllockstatus=readdatalogline.split("*")[3]
                if celllockstatus == "Locked":
                   celllockstatusediticonLabel['image']=lockclosepic
                   celllockstatuseditstatusLabel['text']="Locked"
                   celllockpasswordLabel['text']="Enter password to unlock"
                   Lockunlockbutton['text']="UnLock"
                   intention="UnLocked"
                elif celllockstatus == "UnLocked":
                   celllockstatusediticonLabel['image']=lockopenpic
                   celllockstatuseditstatusLabel['text']="UnLocked"
                   celllockpasswordLabel['text']="Enter password to lock"
                   Lockunlockbutton['text']="Lock"
                   intention="Locked"
                   #print("data available:"+cellwheelnumber)
    
def cellremarkbuttonselect(*args):
    def cleartext(*args):
        #print("clear text pressed")
        remarkseditWindowtextentry.delete(0.0,END)
    def saveremarks(*args):
        #print("save remarks pressed")
        #print("text entry:")
        #print(remarkseditWindowtextentry.get(1.0,END))
        stringenetered=remarkseditWindowtextentry.get(1.0,END)
        #print(stringenetered)
        #print(len(stringenetered))
        if stringenetered=="\n":
           #print("entered blank text")
           readdatalog = open ("/home/pi/Desktop/WheelStacker/data/WSTRdata.log", "r")
           readdatalogtemp = open ("/home/pi/Desktop/WheelStacker/data/WSTRdatatemp.log", "w")
           lineread=True
           datafound=False
           while lineread:
                # Read next line
                readdatalogline = readdatalog.readline()
                #print(readdatalogline)
                # If line is blank, then you struck the EOF
                if not readdatalogline :
                    if datafound==False:
                        newstringinput=str(args[0]) + "" + str(args[1])+"*Not Available*Not Available*UnLocked*None*No remarks\n"
                        readdatalogtemp.write(newstringinput)
                    readdatalog.close()
                    readdatalogtemp.close()
                    os.system("rm /home/pi/Desktop/WheelStacker/data/WSTRdata.log")
                    os.system("mv /home/pi/Desktop/WheelStacker/data/WSTRdatatemp.log /home/pi/Desktop/WheelStacker/data/WSTRdata.log")
                    lineread=False
                    sendscansignal()
                    remarkseditWindow.destroy()
                else:
                    cellnumber=readdatalogline.split("*")[0]
                    if cellnumber == str(args[0]) + "" + str(args[1]):
                        datafound=True
                        cellnumber=readdatalogline.split("*")[0]
                        wheelnumber=readdatalogline.split("*")[1]
                        wheelloaddate=readdatalogline.split("*")[2]
                        wheellockstatus=readdatalogline.split("*")[3]
                        remarkavailstatus=readdatalogline.split("*")[4]
                        remarkstext=readdatalogline.split("*")[5]
                        newstringinput=cellnumber+"*"+wheelnumber+"*"+wheelloaddate+"*"+wheellockstatus+"*None*No remarks\n"
                        readdatalogtemp.write(newstringinput)
                        logger.warning(datetimestring + " :: " + "editing remarks of log-"+str(args[0]) + "" + str(args[1])+"changing:"+remarkstext+"to:None")
                    else: 
                        readdatalogtemp.write(readdatalogline)
        else:
           #print("not entered blank text")
           readdatalog = open ("/home/pi/Desktop/WheelStacker/data/WSTRdata.log", "r")
           readdatalogtemp = open ("/home/pi/Desktop/WheelStacker/data/WSTRdatatemp.log", "w")
           lineread=True
           datafound=False
           while lineread:
                # Read next line
                readdatalogline = readdatalog.readline()
                #print(readdatalogline)
                # If line is blank, then you struck the EOF
                if not readdatalogline :
                    if datafound==False:
                        newstringinput=str(args[0]) + "" + str(args[1])+"*Not Available*Not Available*UnLocked*Available*"+stringenetered
                        readdatalogtemp.write(newstringinput)
                    readdatalog.close()
                    readdatalogtemp.close()
                    os.system("rm /home/pi/Desktop/WheelStacker/data/WSTRdata.log")
                    os.system("mv /home/pi/Desktop/WheelStacker/data/WSTRdatatemp.log /home/pi/Desktop/WheelStacker/data/WSTRdata.log")
                    lineread=False
                    sendscansignal()
                    remarkseditWindow.destroy()
                else:
                    cellnumber=readdatalogline.split("*")[0]
                    if cellnumber == str(args[0]) + "" + str(args[1]):
                        datafound=True
                        cellnumber=readdatalogline.split("*")[0]
                        wheelnumber=readdatalogline.split("*")[1]
                        wheelloaddate=readdatalogline.split("*")[2]
                        wheellockstatus=readdatalogline.split("*")[3]
                        remarkavailstatus=readdatalogline.split("*")[4]
                        remarkstext=readdatalogline.split("*")[5]
                        newstringinput=cellnumber+"*"+wheelnumber+"*"+wheelloaddate+"*"+wheellockstatus+"*Available*"+stringenetered
                        readdatalogtemp.write(newstringinput)
                        logger.warning(datetimestring + " :: " + "editing remarks of log-"+str(args[0]) + "" + str(args[1])+"changing:"+remarkstext+"to:"+stringenetered)
                    else: 
                        readdatalogtemp.write(readdatalogline)
    #print("x: "+str(args[0])+" y: "+str(args[1])) 
    #logger.error(datetimestring + " :: " + "selected cell remark button cell:"+ str(args[0]) + "x" + str(args[1]))
    #logger.error("cell selected")
    remarkseditWindow = Toplevel(master) 
    remarkseditWindow.title("  ")
    #wheelnumbereditWindow.wm_attributes('-type', 'splash')
    remarkseditWindow.configure(bg='gray90')
    remarkseditWindow.resizable(0,0)
    #wheelnumbereditWindow.attributes('-toolwindow', True)
    #wheelnumbereditWindow.overredirect(True)
    remarkseditWindowWidth=300
    remarkseditWindowHeight=300
    remarkseditWindow.geometry('{}x{}+{}+{}'.format(remarkseditWindowWidth, remarkseditWindowHeight, int(master.winfo_screenwidth()/2)-int(remarkseditWindowWidth/2), int(master.winfo_screenheight()/2)-int(remarkseditWindowHeight/2)))
    remarkseditWindowLabel = tk.Label(remarkseditWindow, text="Edit Remarks",font=('Helvetica', 15, 'bold'), bg='gray90')
    remarkseditWindowLabel['width']=27
    remarkseditWindowLabel['height']=1
    remarkseditWindowLabel.grid(row = 0, column = 0)
    remarkseditWindowcellnumberLabel = tk.Label(remarkseditWindow, text="Cell:"+ str(args[0]) + "x" + str(args[1]),font=('Helvetica', 13), bg='gray90')
    remarkseditWindowcellnumberLabel['width']=27
    remarkseditWindowcellnumberLabel['height']=1
    remarkseditWindowcellnumberLabel.grid(row = 1, column = 0)
    remarkseditWindowtextentry = tk.Text(remarkseditWindow,font=('Helvetica', 15, 'bold'))
    remarkseditWindowtextentry['width']=22
    remarkseditWindowtextentry['height']=5
    remarkseditWindowtextentry.grid(row = 2, column = 0)
    Blanklabel = tk.Label(remarkseditWindow, text="", font=('Helvetica', 10), bd=0, height=1, width=15, bg='gray90', fg='red')
    Blanklabel.grid(row=3, column=0)
    Clearbutton = tk.Button(remarkseditWindow, text="Clear", font=('Helvetica', 15, 'bold'), bd=1, height=1, width=15, command=lambda:cleartext(args[0],args[1]))
    Clearbutton.grid(row=4, column=0)
    Saveremarksbutton = tk.Button(remarkseditWindow, text="Save & Exit", font=('Helvetica', 15, 'bold'), bd=1, height=1, width=15, command=lambda:saveremarks(args[0],args[1]))
    Saveremarksbutton.grid(row=5, column=0)
    readdatalog = open ("/home/pi/Desktop/WheelStacker/data/WSTRdata.log", "r")
    dataavailable=False
    lineread=True                  
    while lineread:
        readdatalogline = readdatalog.readline()
        if not readdatalogline :
           if dataavailable==False:
               #print("data not available")
               remarkseditWindowtextentry.insert(END, "")
           lineread=False
        else:
           cellnumber=readdatalogline.split("*")[0]
           if cellnumber == str(args[0]) + "" + str(args[1]):
                dataavailable=True
                cellremarksavail=readdatalogline.split("*")[4]
                #print("remarks availablity:"+cellremarksavail)
                if cellremarksavail=="Available":
                    #print("remarks available")
                    cellremarks=readdatalogline.split("*")[5]
                    remarkseditWindowtextentry.insert(END, cellremarks)
                elif cellremarksavail=="None":
                    #print("remarks not available")
                    remarkseditWindowtextentry.insert(END, "")
    
def disptime():
    global datetimestring
    datetimestring = strftime('%d/%m/%y %H:%M:%S %p') 
    Datetimebutton.config(text = datetimestring) 
    Datetimebutton.after(1000, disptime)
    
def exitbutton():

    try:
       ser.flushInput()
       ser.flushOutput()
       ser.close()
    except Exception as e:
         #print("Serial close exception")
        logger.error(datetimestring + " :: " + "Serial close exception")
    try:
        thread.exit()
        #print("Closing serial thread")
    except Exception as e:
        #print("Closing serial thread exception")
        logger.error(datetimestring + " :: " + "Closing serial thread exception")
    try:
        #master.destroy()
        #print("Closing program")
        logger.error(datetimestring + " :: " + "Closing program")
        sys.exit()
#       print("Closing program after")
    except Exception as e:
        #print("Closing program exception")
        logger.error(datetimestring + " :: " + "Closing program exception")
        

def snapshotbutton():
    try:
        os.system(screen_shot_cmd)
        #print("screen shot taken")
        logger.warning(datetimestring + " :: " + "screen shot taken")
    except Exception as e:
        #print("Screenshot exception")
        logger.error(datetimestring + " :: " + "Screenshot exception")
        return None
    
def AlarmOnOffbutton():
    global ALARMONOFF
    global changeparcheck
    changeparcheck=1
    if ALARMONOFF == 0:
        ALARMONOFF=1
        AlarmOnOffbutton['image']=alarmoffpic
    else:
        ALARMONOFF=0
        AlarmOnOffbutton['image']=alarmonpic
   
def settingsbutton():
    #print("settings button clicked")
    settingsWindow = Toplevel(master) 
    settingsWindow.title("Settings")
    settingsWindowWidth=500
    settingsWindowHeight=400
    settingsWindow.geometry('{}x{}+{}+{}'.format(settingsWindowWidth, settingsWindowHeight, int(master.winfo_screenwidth()/2)-int(settingsWindowWidth/2), int(master.winfo_screenheight()/2)-int(settingsWindowHeight/2)))
    # Create a Tkinter variable
    res_choice_sel = StringVar(master)
    baud_rate_sel = StringVar(master)
    pwm_freq_sel = StringVar(master)
    # Dictionary with options
    res_choices = ["1ms","10ms","20ms","50ms"]
    baud_rate_choices = ["2400", "4800", "9600","19200","38400"]
    pwm_freq_choices = ["64kHz", "8kHz", "1kHz","500hz"]
    
    res_choice_sel.set(res_choices[0]) # set the default option
    baud_rate_sel.set(baud_rate_choices[2])
    pwm_freq_sel.set(pwm_freq_choices[1])

    res_choice_sel_popupMenu = tk.OptionMenu(settingsWindow, res_choice_sel, *res_choices)
    res_choice_sel_popupMenu['width']=5
    res_choice_sel_Label = tk.Label(settingsWindow, text="Set Resolution:", anchor='w', justify=LEFT)
    res_choice_sel_Label['width']=18
    res_choice_sel_Label.grid(row = 0, column = 0)
    res_choice_sel_popupMenu.grid(row = 0, column =1)
    
    
    baud_rate_sel_popupMenu = tk.OptionMenu(settingsWindow, baud_rate_sel, *baud_rate_choices)
    baud_rate_sel_popupMenu['width']=5
    baud_rate_sel_Label = tk.Label(settingsWindow, text="Set Baud Rate:", anchor='w', justify=LEFT)
    baud_rate_sel_Label['width']=18
    baud_rate_sel_Label.grid(row = 1, column = 0)
    baud_rate_sel_popupMenu.grid(row = 1, column =1)
    
    pwm_freq_sel_popupMenu = tk.OptionMenu(settingsWindow, pwm_freq_sel, *pwm_freq_choices)
    pwm_freq_sel_popupMenu['width']=5
    pwm_freq_sel_Label = tk.Label(settingsWindow, text="Set PWM freq:", anchor='w', justify=LEFT)
    pwm_freq_sel_Label['width']=18
    pwm_freq_sel_Label.grid(row = 2, column = 0)
    pwm_freq_sel_popupMenu.grid(row = 2, column =1)
    
    screenshot_folder_sel_Label = tk.Label(settingsWindow, text="Select folder for\nstoring screenshot:", anchor='w', justify=LEFT)
    screenshot_folder_sel_Label['width']=18
    screenshot_folder_sel_Label['height']=2
    screenshot_folder_sel_Label.grid(row = 3, column = 0)
        
    def screenshot_folder_sel_browse_button(*args):
        folder_path = StringVar()
        filename = filedialog.askdirectory()
        folder_path.set(filename)
        if str(filename) == "":
            screenshot_folder_sel_browse_button['text']="Browse"
        else:
            screenshot_folder_sel_browse_button['text']=str(filename)
        #print(filename)
        
    def check_ip_add(*args):
        #print("check ip address button clicked")
        # getting IP Address
        address = subprocess.check_output(['hostname', '-s', '-I']).decode('utf-8')[:-1]
        #print(address.split(" ")[0])
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            ipaddrstr=str(address.split(" ")[0])
            if ipaddrstr == "" or len(ipaddrstr) > 20:
                check_ip_address_Button['text']="NA Check"
                logger.error(datetimestring + " :: " + "No connections found")
                #print("No connections found")
            else:
                check_ip_address_Button['text']=ipaddrstr
        except Exception as e:
            check_ip_address_Button['text']="NA Check"
            logger.error(datetimestring + " :: " + "IP addr retrieval error")
            #print("IP addr retrieval error")
        try:
            ipaddrstr=str(address.split(" ")[1])
            if ipaddrstr == "" or len(ipaddrstr) > 20:
                check_ip_address2_Button['text']=""
                check_ip_address2_Button['width']=0
                check_ip_address2_Button['bd']=0
                logger.error(datetimestring + " :: " + "No additional connections found")
                #print("No connections found")
            else:
                check_ip_address2_Button['text']=ipaddrstr
                check_ip_address2_Button['bd']=1
        except Exception as e:
            check_ip_address2_Button['text']=""
            check_ip_address2_Button['width']=12
            check_ip_address2_Button['bd']=0
            logger.error(datetimestring + " :: " + "Secondary IP addr retrieval error")
            #print("Secondary IP addr retrieval error")
            
    def check_hostname(*args):
        hostname = socket.gethostname() 
        check_hostname_Button['text']=hostname
        
    def show_logs_button(*args):
        logsWindow = Toplevel(master) 
        logsWindow.title("Log Window")
        logsWindowWidth=800
        logsWindowHeight=500
        logsWindow.geometry('{}x{}+{}+{}'.format(logsWindowWidth, logsWindowHeight, int(master.winfo_screenwidth()/2)-int(logsWindowWidth/2), int(master.winfo_screenheight()/2)-int(logsWindowHeight/2)))
        horizontalscrollbar = tk.Scrollbar(logsWindow, orient = 'horizontal') 
        # attach Scrollbar to root window at the bootom 
        horizontalscrollbar.pack(side = BOTTOM, fill = X) 
        # create a vertical scrollbar-no need to write orient as it is by default vertical 
        verticalscrollbar = tk.Scrollbar(logsWindow) 
        # attach Scrollbar to root window on the side 
        verticalscrollbar.pack(side = RIGHT, fill = Y)
        rd = open ("/home/pi/Desktop/WheelStacker/logs/WSTR.log", "r")
        texthold = tk.Text(logsWindow, wrap = NONE, xscrollcommand = horizontalscrollbar.set,  yscrollcommand = verticalscrollbar.set, state=NORMAL, width=80, height=50)
        while True:
            # Read next line
            line = rd.readline()
            # If line is blank, then you struck the EOF
            if not line :
                break;
            texthold.insert(END,line.strip())
            texthold.insert(END,"\n")
        # Close file 
        rd.close()
        texthold.pack(side=TOP, fill=X)
        texthold["state"] = DISABLED
        # here command represents the method to be executed xview is executed on object 't' Here t may represent any widget 
        horizontalscrollbar.config(command=texthold.xview) 
        # here command represents the method to be executed yview is executed on object 't' Here t may represent any widget 
        verticalscrollbar.config(command=texthold.yview)
        
    def clear_logs_button(*args):
        os.system("rm /home/pi/Desktop/WheelStacker/logs/WSTR.log")
        os.system("touch /home/pi/Desktop/WheelStacker/logs/WSTR.log")
        handler = logging.FileHandler('/home/pi/Desktop/WheelStacker/logs/WSTR.log')
        logger.addHandler(handler)
        
    def start_prog_onboot_button(*args):
        rd = open ("/etc/profile", "r")
        chkboot = 0
        while True:
            # Read next line
            line = rd.readline()
            # If line is blank, then you struck the EOF
            if not line :
                break;
            #print(line.strip())
            if "python3 /home/pi/Desktop/WheelStacker/WheelStacker.py" in line:
                chkboot = 1
                break;
        # Close file 
        rd.close()
        if chkboot == 0:
            os.system("sudo sh -c \"echo python3 /home/pi/Desktop/WheelStacker/WheelStacker.py >> /etc/profile\"")
            start_prog_onboot_button['text']="Enabled"
        else:
            #start_prog_onboot_button['text']="Enabled"
            os.system("sudo sed -i.bak '$d' /etc/profile")
            start_prog_onboot_button['text']=DISABLED
            
    def reboot_button(*args):
        #sendstringtest=str(BPMSlider.get())+"*"+str(TiVSlider.get())+"*"+str(IERSlider.get()*10)+"*"+str(PIPLSlider.get())+"*"+str(PEEPLSlider.get())+"*"+str(FIOLSlider.get())+"*0*"+str(ALARMONOFF)
        #ser.write(sendstringtest.encode("utf-8"))
        os.system("sudo reboot")
        
                    
    screenshot_folder_sel_browse_button = tk.Button(settingsWindow, text="Browse", command=screenshot_folder_sel_browse_button, width=10, height=2, wraplength=100)
    screenshot_folder_sel_browse_button.grid(row=3, column=1)
   
    check_ip_Label = tk.Label(settingsWindow, text="IP address:", width=18, height=1, anchor='w', justify=LEFT)
    check_ip_Label.grid(row=5, column=0)
    
    check_ip_address_Button = tk.Button(settingsWindow, text="Check", justify=CENTER, command=check_ip_add)
    check_ip_address_Button['width']=12
    check_ip_address_Button.grid(row = 5, column = 1)
    
    check_ip_address2_Button = tk.Button(settingsWindow, text="", justify=CENTER, bd=0)
    check_ip_address2_Button['width']=0
    check_ip_address2_Button.grid(row = 5, column = 2)
    
    check_hostname_Label = tk.Label(settingsWindow, text="Hostname:", width=18, height=1, anchor='w', justify=LEFT)
    check_hostname_Label.grid(row=6, column=0)
    
    check_hostname_Button = tk.Button(settingsWindow, text="Check", justify=CENTER, command=check_hostname)
    check_hostname_Button['width']=12
    check_hostname_Button.grid(row = 6, column = 1)
    
    check_cwd_Label = tk.Label(settingsWindow, text="Current working directory:", width=21, height=1, anchor='w', justify=LEFT)
    check_cwd_Label.grid(row=7, column=0)
        
    dirpath = os.getcwd()
    cwd_Label = tk.Label(settingsWindow, text=dirpath, width=20, height=1, anchor='w', justify=LEFT)
    cwd_Label.grid(row=7, column=1)
    
    check_USB_dev_Label = tk.Label(settingsWindow, text="Current MC unit addr:", width=21, height=1, anchor='w', justify=LEFT)
    check_USB_dev_Label.grid(row=8, column=0)
    
    try:
        ard_addr = glob.glob("/dev/ttyACM*")[0]        
    except Exception as e:
        logger.error(datetimestring + " :: " + "arduino not sensed")
        ard_addr = "None"
            
    USB_dev_Label = tk.Label(settingsWindow, text=ard_addr, width=25, height=1, anchor='w', justify=LEFT)
    USB_dev_Label.grid(row=8, column=1)
    #foldername = os.path.basename(dirpath)
    #print("Directory name is : " + foldername)
    
    show_logs_button = tk.Button(settingsWindow, text="Open logs", command=show_logs_button, width=18, height=1)
    show_logs_button.grid(row=9, column=0)
    
    clear_logs_button = tk.Button(settingsWindow, text="Clear logs", command=clear_logs_button, width=18, height=1)
    clear_logs_button.grid(row=9, column=1)
    
    start_prog_onboot_label = tk.Label(settingsWindow, text="Start program on boot:", width=20, height=1, anchor='w', justify=LEFT)
    start_prog_onboot_label.grid(row=10, column=0)
    
    start_prog_onboot_button = tk.Button(settingsWindow, command=start_prog_onboot_button, width=18, height=1)
    rd = open ("/etc/profile", "r")
    chkboot = 0
    while True:
        # Read next line
        line = rd.readline()
        # If line is blank, then you struck the EOF
        if not line :
            break;
        #print(line.strip())
        if "python3 /home/pi/Desktop/WheelStacker/WheelStacker.py" in line:
            chkboot = 1
            break;
    # Close file 
    rd.close()
    if chkboot == 0:
        start_prog_onboot_button['text']=DISABLED
    else:
        start_prog_onboot_button['text']="Enabled"
    start_prog_onboot_button.grid(row=10, column=1)
    
    reboot_button = tk.Button(settingsWindow, text="Reboot", command=reboot_button, width=18, height=1)
    reboot_button.grid(row=11, column=0)
            
    # on change dropdown value
    def change_dropdown_res(*args):
        print( res_choice_sel.get() )
        
    def change_dropdown_bdr(*args):
        print( baud_rate_sel.get() )
        
    def change_dropdown_pwm(*args):
        print( pwm_freq_sel.get() )

    # link function to change dropdown
    res_choice_sel.trace('w', change_dropdown_res)
    baud_rate_sel.trace('w', change_dropdown_bdr)
    pwm_freq_sel.trace('w', change_dropdown_pwm)


master.minsize(1820, 890)
master.geometry("500x600")
windowWidth = master.winfo_reqwidth()
windowHeight = master.winfo_reqheight()

# Creating a photoimage object to use image
lockopenpic = PhotoImage(file = "/home/pi/Desktop/WheelStacker/images/lock_open.png")
lockclosepic = PhotoImage(file = "/home/pi/Desktop/WheelStacker/images/lock_close.png")
alarmoffpic = PhotoImage(file = "/home/pi/Desktop/WheelStacker/images/alarmoff_icon.png")
alarmonpic = PhotoImage(file = "/home/pi/Desktop/WheelStacker/images/alarmon_icon.png")
snapshotpic = PhotoImage(file = "/home/pi/Desktop/WheelStacker/images/screen_shot.pgm")
settingsiconpic = PhotoImage(file = "/home/pi/Desktop/WheelStacker/images/settings_icon.png")
wheelcellfullicon = PhotoImage(file = "/home/pi/Desktop/WheelStacker/images/Wheel_cell_full.png")
wheelcellemptyicon = PhotoImage(file = "/home/pi/Desktop/WheelStacker/images/Wheel_cell_empty.png")
movelefticon=PhotoImage(file = "/home/pi/Desktop/WheelStacker/images/move_left.png")
moverighticon=PhotoImage(file = "/home/pi/Desktop/WheelStacker/images/move_right.png")
moveupicon=PhotoImage(file = "/home/pi/Desktop/WheelStacker/images/move_up.png")
movedownicon=PhotoImage(file = "/home/pi/Desktop/WheelStacker/images/move_down.png")
idleicon=PhotoImage(file = "/home/pi/Desktop/WheelStacker/images/stop.png")
erroricon=PhotoImage(file = "/home/pi/Desktop/WheelStacker/images/error.png")

DisplayGroup = LabelFrame(master, text = "")
DisplayGroup.grid(row=0, column=0)

AlarmDisplayGroup = LabelFrame(DisplayGroup, text = "", width=400, height=2)
AlarmDisplayGroup.grid(row=0, column=0)

Datetimebutton = tk.Button(AlarmDisplayGroup, text="Date & Time", font=('Helvetica', 13, 'bold'), bd=0)
Datetimebutton.grid(row=0, column=0)

Statusbutton = tk.Button(AlarmDisplayGroup, text="IDLE-STOP", font=('Helvetica', 13, 'bold'), bd=0, width=25, height=2)
Statusbutton.grid(row=0, column=1)

Statusicon = tk.Label(AlarmDisplayGroup, bd=0, width=70, height=50, image=idleicon)
Statusicon.grid(row=0, column=2)

Titlelabel = tk.Label(AlarmDisplayGroup, text="        Wheel Stacker Project GOC", font=('Helvetica', 22, 'bold'), width=49, height=2, bd=0)
Titlelabel.grid(row=0, column=3)

ComErrorAlarmlabel = tk.Label(AlarmDisplayGroup, text="", font=('Helvetica', 18, 'bold'), width=17, height=2, bd=0, fg="red")
ComErrorAlarmlabel.grid(row=0, column=4)

Snapshotbutton = tk.Button(AlarmDisplayGroup, text="", bd=0, image=snapshotpic, command=snapshotbutton, width=70, height=50)
Snapshotbutton.grid(row=0, column=5)

Settingsbutton = tk.Button(AlarmDisplayGroup, text="", bd=0, image=settingsiconpic, command=settingsbutton, width=70, height=50)
Settingsbutton.grid(row=0, column=6)

AlarmOnOffbutton = tk.Button(AlarmDisplayGroup, text="", bd=0, image=alarmoffpic, command=AlarmOnOffbutton)
AlarmOnOffbutton.grid(row=0, column=7)

Exitbutton = tk.Button(AlarmDisplayGroup, text="X", font=('Helvetica', 20, 'bold'), bd=0, command=exitbutton)
Exitbutton.grid(row=0, column=8)

ActiveAppGroup = LabelFrame(master, text = "")
ActiveAppGroup.grid(row=1, column=0)

wheelcellwidth=605
wheelcellheight=265

wheelpicwidth=500
wheelpicheight=150

wheeldetaillabelwidth=10
wheeldetaillabelheight=1

wheelremarkbuttonwidth=22
wheelremarkbuttonheight=1

Cellgroup00 = LabelFrame(ActiveAppGroup, text = "", width=wheelcellwidth, height=wheelcellheight, bd=1)
Cellgroup00.grid(row=0, column=0)

Cellbutton00 = tk.Button(Cellgroup00, text="", bd=0, image=wheelcellemptyicon, width=wheelpicwidth, height=wheelpicheight,command= lambda: wheelcellselect(0,0))
Cellbutton00.grid(row=0, column=0)

wheeldetailgroup00= LabelFrame(Cellgroup00, text = "", bd=1)
wheeldetailgroup00.grid(row=1, column=0)

wheelnumberlabel00 = tk.Label(wheeldetailgroup00, text="Wheel No:", font=('Helvetica', 13, 'bold'), bd=1, width=wheeldetaillabelwidth, height=wheeldetaillabelheight, anchor='w', justify=LEFT)
wheelnumberlabel00.grid(row=0, column=0)

wheelnumberbutton00 = tk.Button(wheeldetailgroup00, text="Empty", font=('Helvetica', 13, 'bold'), bd=1, width=22, height=1,command=lambda:wheelnumberbuttonselect(0,0))
wheelnumberbutton00.grid(row=0, column=1)

wheelloaddatelabel00 = tk.Label(wheeldetailgroup00, text="Loaded on:", font=('Helvetica', 13, 'bold'), bd=1, width=wheeldetaillabelwidth, height=wheeldetaillabelheight, anchor='w', justify=LEFT)
wheelloaddatelabel00.grid(row=1, column=0)

wheelloaddatebutton00 = tk.Button(wheeldetailgroup00, text="Empty", font=('Helvetica', 13, 'bold'), bd=1, width=22, height=1,command = lambda: wheelloaddatebuttonselect(0,0))
wheelloaddatebutton00.grid(row=1, column=1)

wheellockstatuslabel00 = tk.Label(wheeldetailgroup00, text="Status:", font=('Helvetica', 13, 'bold'), bd=1, width=wheeldetaillabelwidth, height=wheeldetaillabelheight, anchor='w', justify=LEFT)
wheellockstatuslabel00.grid(row=2, column=0)

wheellockbutton00 = tk.Button(wheeldetailgroup00, text="UnLocked", font=('Helvetica', 13, 'bold'), bd=1, width=22, height=1,command= lambda: celllockbuttonselect(0,0))
wheellockbutton00.grid(row=2, column=1)

wheelremarkslabel00 = tk.Label(wheeldetailgroup00, text="Remarks:", font=('Helvetica', 13, 'bold'), bd=0, width=wheeldetaillabelwidth, height=wheeldetaillabelheight)
wheelremarkslabel00.grid(row=0, column=2)

wheelremarksbutton00 = tk.Button(wheeldetailgroup00, text="None", font=('Helvetica', 13), bd=0, width=wheelremarkbuttonwidth, height=wheelremarkbuttonheight,command=lambda:cellremarkbuttonselect(0,0))
wheelremarksbutton00.grid(row=1, column=2)

Cellgroup01 = LabelFrame(ActiveAppGroup, text = "", width=wheelcellwidth, height=wheelcellheight, bd=1)
Cellgroup01.grid(row=0, column=1)

Cellbutton01 = tk.Button(Cellgroup01, text="", bd=0, image=wheelcellemptyicon, width=wheelpicwidth, height=wheelpicheight,command=lambda: wheelcellselect(1,0))
Cellbutton01.grid(row=0, column=0)

wheeldetailgroup01= LabelFrame(Cellgroup01, text = "", bd=1)
wheeldetailgroup01.grid(row=1, column=0)

wheelnumberlabel01 = tk.Label(wheeldetailgroup01, text="Wheel No:", font=('Helvetica', 13, 'bold'), bd=1, width=wheeldetaillabelwidth, height=wheeldetaillabelheight, anchor='w', justify=LEFT)
wheelnumberlabel01.grid(row=0, column=0)

wheelnumberbutton01 = tk.Button(wheeldetailgroup01, text="Empty", font=('Helvetica', 13, 'bold'), bd=1, width=22, height=1,command=lambda:wheelnumberbuttonselect(0,1))
wheelnumberbutton01.grid(row=0, column=1)

wheelloaddatelabel01 = tk.Label(wheeldetailgroup01, text="Loaded on:", font=('Helvetica', 13, 'bold'), bd=1, width=wheeldetaillabelwidth, height=wheeldetaillabelheight, anchor='w', justify=LEFT)
wheelloaddatelabel01.grid(row=1, column=0)

wheelloaddatebutton01 = tk.Button(wheeldetailgroup01, text="Empty", font=('Helvetica', 13, 'bold'), bd=1, width=22, height=1,command = lambda: wheelloaddatebuttonselect(0,1))
wheelloaddatebutton01.grid(row=1, column=1)

wheellockstatuslabel01 = tk.Label(wheeldetailgroup01, text="Status:", font=('Helvetica', 13, 'bold'), bd=1, width=wheeldetaillabelwidth, height=wheeldetaillabelheight, anchor='w', justify=LEFT)
wheellockstatuslabel01.grid(row=2, column=0)

wheellockbutton01 = tk.Button(wheeldetailgroup01, text="UnLocked", font=('Helvetica', 13, 'bold'), bd=1, width=22, height=1,command= lambda: celllockbuttonselect(0,1))
wheellockbutton01.grid(row=2, column=1)

wheelremarkslabel01 = tk.Label(wheeldetailgroup01, text="Remarks:", font=('Helvetica', 13, 'bold'), bd=0, width=wheeldetaillabelwidth, height=wheeldetaillabelheight)
wheelremarkslabel01.grid(row=0, column=2)

wheelremarksbutton01 = tk.Button(wheeldetailgroup01, text="None", font=('Helvetica', 13), bd=0, width=wheelremarkbuttonwidth, height=wheelremarkbuttonheight,command=lambda:cellremarkbuttonselect(0,1))
wheelremarksbutton01.grid(row=1, column=2)

Cellgroup02 = LabelFrame(ActiveAppGroup, text = "", width=wheelcellwidth, height=wheelcellheight, bd=1)
Cellgroup02.grid(row=0, column=2)

Cellgroup10 = LabelFrame(ActiveAppGroup, text = "", width=wheelcellwidth, height=wheelcellheight, bd=1)
Cellgroup10.grid(row=1, column=0)

Cellgroup11 = LabelFrame(ActiveAppGroup, text = "", width=wheelcellwidth, height=wheelcellheight, bd=1)
Cellgroup11.grid(row=1, column=1)

Cellgroup12 = LabelFrame(ActiveAppGroup, text = "", width=wheelcellwidth, height=wheelcellheight, bd=1)
Cellgroup12.grid(row=1, column=2)

Cellgroup20 = LabelFrame(ActiveAppGroup, text = "", width=wheelcellwidth, height=wheelcellheight, bd=1)
Cellgroup20.grid(row=2, column=0)

Cellgroup21 = LabelFrame(ActiveAppGroup, text = "", width=wheelcellwidth, height=wheelcellheight, bd=1)
Cellgroup21.grid(row=2, column=1)

Cellgroup22 = LabelFrame(ActiveAppGroup, text = "", width=wheelcellwidth, height=wheelcellheight, bd=1)
Cellgroup22.grid(row=2, column=2)

Cellbutton20 = tk.Button(Cellgroup20, text="", bd=0, image=wheelcellemptyicon, width=wheelpicwidth, height=wheelpicheight,command=lambda: wheelcellselect(2,0))
Cellbutton20.grid(row=0, column=0)

Cellbutton10 = tk.Button(Cellgroup10, text="", bd=0, image=wheelcellemptyicon, width=wheelpicwidth, height=wheelpicheight,command=lambda: wheelcellselect(0,1))
Cellbutton10.grid(row=0, column=0)

Cellbutton11 = tk.Button(Cellgroup11, text="", bd=0, image=wheelcellemptyicon, width=wheelpicwidth, height=wheelpicheight,command=lambda: wheelcellselect(1,1))
Cellbutton11.grid(row=0, column=0)

Cellbutton21 = tk.Button(Cellgroup21, text="", bd=0, image=wheelcellemptyicon, width=wheelpicwidth, height=wheelpicheight,command=lambda: wheelcellselect(2,1))
Cellbutton21.grid(row=0, column=0)

Cellbutton02 = tk.Button(Cellgroup02, text="", bd=0, image=wheelcellemptyicon, width=wheelpicwidth, height=wheelpicheight,command=lambda: wheelcellselect(0,2))
Cellbutton02.grid(row=0, column=0)

Cellbutton12 = tk.Button(Cellgroup12, text="", bd=0, image=wheelcellemptyicon, width=wheelpicwidth, height=wheelpicheight,command=lambda: wheelcellselect(1,2))
Cellbutton12.grid(row=0, column=0)

Cellbutton22 = tk.Button(Cellgroup22, text="", bd=0, image=wheelcellemptyicon, width=wheelpicwidth, height=wheelpicheight,command=lambda: wheelcellselect(2,2))
Cellbutton22.grid(row=0, column=0)

wheeldetailgroup02= LabelFrame(Cellgroup02, text = "", bd=1)
wheeldetailgroup02.grid(row=1, column=0)

wheelnumberlabel02 = tk.Label(wheeldetailgroup02, text="Wheel No:", font=('Helvetica', 13, 'bold'), bd=1, width=wheeldetaillabelwidth, height=wheeldetaillabelheight, anchor='w', justify=LEFT)
wheelnumberlabel02.grid(row=0, column=0)

wheelnumberbutton02 = tk.Button(wheeldetailgroup02, text="Empty", font=('Helvetica', 13, 'bold'), bd=1, width=22, height=1,command=lambda:wheelnumberbuttonselect(0,2))
wheelnumberbutton02.grid(row=0, column=1)

wheelloaddatelabel02 = tk.Label(wheeldetailgroup02, text="Loaded on:", font=('Helvetica', 13, 'bold'), bd=1, width=wheeldetaillabelwidth, height=wheeldetaillabelheight, anchor='w', justify=LEFT)
wheelloaddatelabel02.grid(row=1, column=0)

wheelloaddatebutton02 = tk.Button(wheeldetailgroup02, text="Empty", font=('Helvetica', 13, 'bold'), bd=1, width=22, height=1,command = lambda: wheelloaddatebuttonselect(0,2))
wheelloaddatebutton02.grid(row=1, column=1)

wheellockstatuslabel02 = tk.Label(wheeldetailgroup02, text="Status:", font=('Helvetica', 13, 'bold'), bd=1, width=wheeldetaillabelwidth, height=wheeldetaillabelheight, anchor='w', justify=LEFT)
wheellockstatuslabel02.grid(row=2, column=0)

wheellockbutton02 = tk.Button(wheeldetailgroup02, text="UnLocked", font=('Helvetica', 13, 'bold'), bd=1, width=22, height=1,command= lambda: celllockbuttonselect(0,2))
wheellockbutton02.grid(row=2, column=1)

wheelremarkslabel02 = tk.Label(wheeldetailgroup02, text="Remarks:", font=('Helvetica', 13, 'bold'), bd=0, width=wheeldetaillabelwidth, height=wheeldetaillabelheight)
wheelremarkslabel02.grid(row=0, column=2)

wheelremarksbutton02 = tk.Button(wheeldetailgroup02, text="None", font=('Helvetica', 13), bd=0, width=wheelremarkbuttonwidth, height=wheelremarkbuttonheight,command=lambda:cellremarkbuttonselect(0,2))
wheelremarksbutton02.grid(row=1, column=2)

wheeldetailgroup10= LabelFrame(Cellgroup10, text = "", bd=1)
wheeldetailgroup10.grid(row=1, column=0)

wheelnumberlabel10 = tk.Label(wheeldetailgroup10, text="Wheel No:", font=('Helvetica', 13, 'bold'), bd=1, width=wheeldetaillabelwidth, height=wheeldetaillabelheight, anchor='w', justify=LEFT)
wheelnumberlabel10.grid(row=0, column=0)

wheelnumberbutton10 = tk.Button(wheeldetailgroup10, text="Empty", font=('Helvetica', 13, 'bold'), bd=1, width=22, height=1,command= lambda: wheelnumberbuttonselect(1,0))
wheelnumberbutton10.grid(row=0, column=1)

wheelloaddatelabel10 = tk.Label(wheeldetailgroup10, text="Loaded on:", font=('Helvetica', 13, 'bold'), bd=1, width=wheeldetaillabelwidth, height=wheeldetaillabelheight, anchor='w', justify=LEFT)
wheelloaddatelabel10.grid(row=1, column=0)

wheelloaddatebutton10 = tk.Button(wheeldetailgroup10, text="Empty", font=('Helvetica', 13, 'bold'), bd=1, width=22, height=1,command = lambda: wheelloaddatebuttonselect(1,0))
wheelloaddatebutton10.grid(row=1, column=1)

wheellockstatuslabel10 = tk.Label(wheeldetailgroup10, text="Status:", font=('Helvetica', 13, 'bold'), bd=1, width=wheeldetaillabelwidth, height=wheeldetaillabelheight, anchor='w', justify=LEFT)
wheellockstatuslabel10.grid(row=2, column=0)

wheellockbutton10 = tk.Button(wheeldetailgroup10, text="UnLocked", font=('Helvetica', 13, 'bold'), bd=1, width=22, height=1,command= lambda: celllockbuttonselect(1,0))
wheellockbutton10.grid(row=2, column=1)

wheelremarkslabel10 = tk.Label(wheeldetailgroup10, text="Remarks:", font=('Helvetica', 13, 'bold'), bd=0, width=wheeldetaillabelwidth, height=wheeldetaillabelheight)
wheelremarkslabel10.grid(row=0, column=2)

wheelremarksbutton10 = tk.Button(wheeldetailgroup10, text="None", font=('Helvetica', 13), bd=0, width=wheelremarkbuttonwidth, height=wheelremarkbuttonheight,command=lambda:cellremarkbuttonselect(1,0))
wheelremarksbutton10.grid(row=1, column=2)

wheeldetailgroup11= LabelFrame(Cellgroup11, text = "", bd=1)
wheeldetailgroup11.grid(row=1, column=0)

wheelnumberlabel11 = tk.Label(wheeldetailgroup11, text="Wheel No:", font=('Helvetica', 13, 'bold'), bd=1, width=wheeldetaillabelwidth, height=wheeldetaillabelheight, anchor='w', justify=LEFT)
wheelnumberlabel11.grid(row=0, column=0)

wheelnumberbutton11 = tk.Button(wheeldetailgroup11, text="Empty", font=('Helvetica', 13, 'bold'), bd=1, width=22, height=1,command=lambda:wheelnumberbuttonselect(1,1))
wheelnumberbutton11.grid(row=0, column=1)

wheelloaddatelabel11 = tk.Label(wheeldetailgroup11, text="Loaded on:", font=('Helvetica', 13, 'bold'), bd=1, width=wheeldetaillabelwidth, height=wheeldetaillabelheight, anchor='w', justify=LEFT)
wheelloaddatelabel11.grid(row=1, column=0)

wheelloaddatebutton11 = tk.Button(wheeldetailgroup11, text="Empty", font=('Helvetica', 13, 'bold'), bd=1, width=22, height=1,command = lambda: wheelloaddatebuttonselect(1,1))
wheelloaddatebutton11.grid(row=1, column=1)

wheellockstatuslabel11 = tk.Label(wheeldetailgroup11, text="Status:", font=('Helvetica', 13, 'bold'), bd=1, width=wheeldetaillabelwidth, height=wheeldetaillabelheight, anchor='w', justify=LEFT)
wheellockstatuslabel11.grid(row=2, column=0)

wheellockbutton11 = tk.Button(wheeldetailgroup11, text="UnLocked", font=('Helvetica', 13, 'bold'), bd=1, width=22, height=1,command= lambda: celllockbuttonselect(1,1))
wheellockbutton11.grid(row=2, column=1)

wheelremarkslabel11 = tk.Label(wheeldetailgroup11, text="Remarks:", font=('Helvetica', 13, 'bold'), bd=0, width=wheeldetaillabelwidth, height=wheeldetaillabelheight)
wheelremarkslabel11.grid(row=0, column=2)

wheelremarksbutton11 = tk.Button(wheeldetailgroup11, text="None", font=('Helvetica', 13), bd=0, width=wheelremarkbuttonwidth, height=wheelremarkbuttonheight,command=lambda:cellremarkbuttonselect(1,1))
wheelremarksbutton11.grid(row=1, column=2)

wheeldetailgroup12= LabelFrame(Cellgroup12, text = "", bd=1)
wheeldetailgroup12.grid(row=1, column=0)

wheelnumberlabel12 = tk.Label(wheeldetailgroup12, text="Wheel No:", font=('Helvetica', 13, 'bold'), bd=1, width=wheeldetaillabelwidth, height=wheeldetaillabelheight, anchor='w', justify=LEFT)
wheelnumberlabel12.grid(row=0, column=0)

wheelnumberbutton12 = tk.Button(wheeldetailgroup12, text="Empty", font=('Helvetica', 13, 'bold'), bd=1, width=22, height=1,command=lambda:wheelnumberbuttonselect(1,2))
wheelnumberbutton12.grid(row=0, column=1)

wheelloaddatelabel12 = tk.Label(wheeldetailgroup12, text="Loaded on:", font=('Helvetica', 13, 'bold'), bd=1, width=wheeldetaillabelwidth, height=wheeldetaillabelheight, anchor='w', justify=LEFT)
wheelloaddatelabel12.grid(row=1, column=0)

wheelloaddatebutton12 = tk.Button(wheeldetailgroup12, text="Empty", font=('Helvetica', 13, 'bold'), bd=1, width=22, height=1,command = lambda: wheelloaddatebuttonselect(1,2))
wheelloaddatebutton12.grid(row=1, column=1)

wheellockstatuslabel12 = tk.Label(wheeldetailgroup12, text="Status:", font=('Helvetica', 13, 'bold'), bd=1, width=wheeldetaillabelwidth, height=wheeldetaillabelheight, anchor='w', justify=LEFT)
wheellockstatuslabel12.grid(row=2, column=0)

wheellockbutton12 = tk.Button(wheeldetailgroup12, text="UnLocked", font=('Helvetica', 13, 'bold'), bd=1, width=22, height=1,command= lambda: celllockbuttonselect(1,2))
wheellockbutton12.grid(row=2, column=1)

wheelremarkslabel12 = tk.Label(wheeldetailgroup12, text="Remarks:", font=('Helvetica', 13, 'bold'), bd=0, width=wheeldetaillabelwidth, height=wheeldetaillabelheight)
wheelremarkslabel12.grid(row=0, column=2)

wheelremarksbutton12 = tk.Button(wheeldetailgroup12, text="None", font=('Helvetica', 13), bd=0, width=wheelremarkbuttonwidth, height=wheelremarkbuttonheight,command=lambda:cellremarkbuttonselect(1,2))
wheelremarksbutton12.grid(row=1, column=2)

wheeldetailgroup20= LabelFrame(Cellgroup20, text = "", bd=1)
wheeldetailgroup20.grid(row=1, column=0)

wheelnumberlabel20 = tk.Label(wheeldetailgroup20, text="Wheel No:", font=('Helvetica', 13, 'bold'), bd=1, width=wheeldetaillabelwidth, height=wheeldetaillabelheight, anchor='w', justify=LEFT)
wheelnumberlabel20.grid(row=0, column=0)

wheelnumberbutton20 = tk.Button(wheeldetailgroup20, text="Empty", font=('Helvetica', 13, 'bold'), bd=1, width=22, height=1,command=lambda:wheelnumberbuttonselect(2,0))
wheelnumberbutton20.grid(row=0, column=1)

wheelloaddatelabel20 = tk.Label(wheeldetailgroup20, text="Loaded on:", font=('Helvetica', 13, 'bold'), bd=1, width=wheeldetaillabelwidth, height=wheeldetaillabelheight, anchor='w', justify=LEFT)
wheelloaddatelabel20.grid(row=1, column=0)

wheelloaddatebutton20 = tk.Button(wheeldetailgroup20, text="Empty", font=('Helvetica', 13, 'bold'), bd=1, width=22, height=1,command = lambda: wheelloaddatebuttonselect(2,0))
wheelloaddatebutton20.grid(row=1, column=1)

wheellockstatuslabel20 = tk.Label(wheeldetailgroup20, text="Status:", font=('Helvetica', 13, 'bold'), bd=1, width=wheeldetaillabelwidth, height=wheeldetaillabelheight, anchor='w', justify=LEFT)
wheellockstatuslabel20.grid(row=2, column=0)

wheellockbutton20 = tk.Button(wheeldetailgroup20, text="UnLocked", font=('Helvetica', 13, 'bold'), bd=1, width=22, height=1,command= lambda: celllockbuttonselect(2,0))
wheellockbutton20.grid(row=2, column=1)

wheelremarkslabel20 = tk.Label(wheeldetailgroup20, text="Remarks:", font=('Helvetica', 13, 'bold'), bd=0, width=wheeldetaillabelwidth, height=wheeldetaillabelheight)
wheelremarkslabel20.grid(row=0, column=2)

wheelremarksbutton20 = tk.Button(wheeldetailgroup20, text="None", font=('Helvetica', 13), bd=0, width=wheelremarkbuttonwidth, height=wheelremarkbuttonheight,command=lambda:cellremarkbuttonselect(2,0))
wheelremarksbutton20.grid(row=1, column=2)

wheeldetailgroup21= LabelFrame(Cellgroup21, text = "", bd=1)
wheeldetailgroup21.grid(row=1, column=0)

wheelnumberlabel21 = tk.Label(wheeldetailgroup21, text="Wheel No:", font=('Helvetica', 13, 'bold'), bd=1, width=wheeldetaillabelwidth, height=wheeldetaillabelheight, anchor='w', justify=LEFT)
wheelnumberlabel21.grid(row=0, column=0)

wheelnumberbutton21 = tk.Button(wheeldetailgroup21, text="Empty", font=('Helvetica', 13, 'bold'), bd=1, width=22, height=1,command=lambda:wheelnumberbuttonselect(2,1))
wheelnumberbutton21.grid(row=0, column=1)

wheelloaddatelabel21 = tk.Label(wheeldetailgroup21, text="Loaded on:", font=('Helvetica', 13, 'bold'), bd=1, width=wheeldetaillabelwidth, height=wheeldetaillabelheight, anchor='w', justify=LEFT)
wheelloaddatelabel21.grid(row=1, column=0)

wheelloaddatebutton21 = tk.Button(wheeldetailgroup21, text="Empty", font=('Helvetica', 13, 'bold'), bd=1, width=22, height=1,command = lambda: wheelloaddatebuttonselect(2,1))
wheelloaddatebutton21.grid(row=1, column=1)

wheellockstatuslabel21 = tk.Label(wheeldetailgroup21, text="Status:", font=('Helvetica', 13, 'bold'), bd=1, width=wheeldetaillabelwidth, height=wheeldetaillabelheight, anchor='w', justify=LEFT)
wheellockstatuslabel21.grid(row=2, column=0)

wheellockbutton21 = tk.Button(wheeldetailgroup21, text="UnLocked", font=('Helvetica', 13, 'bold'), bd=1, width=22, height=1,command= lambda: celllockbuttonselect(2,1))
wheellockbutton21.grid(row=2, column=1)

wheelremarkslabel21 = tk.Label(wheeldetailgroup21, text="Remarks:", font=('Helvetica', 13, 'bold'), bd=0, width=wheeldetaillabelwidth, height=wheeldetaillabelheight)
wheelremarkslabel21.grid(row=0, column=2)

wheelremarksbutton21 = tk.Button(wheeldetailgroup21, text="None", font=('Helvetica', 13), bd=0, width=wheelremarkbuttonwidth, height=wheelremarkbuttonheight,command=lambda:cellremarkbuttonselect(2,1))
wheelremarksbutton21.grid(row=1, column=2)

wheeldetailgroup22= LabelFrame(Cellgroup22, text = "", bd=1)
wheeldetailgroup22.grid(row=1, column=0)

wheelnumberlabel22 = tk.Label(wheeldetailgroup22, text="Wheel No:", font=('Helvetica', 13, 'bold'), bd=1, width=wheeldetaillabelwidth, height=wheeldetaillabelheight, anchor='w', justify=LEFT)
wheelnumberlabel22.grid(row=0, column=0)

wheelnumberbutton22 = tk.Button(wheeldetailgroup22, text="Empty", font=('Helvetica', 13, 'bold'), bd=1, width=22, height=1,command=lambda:wheelnumberbuttonselect(2,2))
wheelnumberbutton22.grid(row=0, column=1)

wheelloaddatelabel22 = tk.Label(wheeldetailgroup22, text="Loaded on:", font=('Helvetica', 13, 'bold'), bd=1, width=wheeldetaillabelwidth, height=wheeldetaillabelheight, anchor='w', justify=LEFT)
wheelloaddatelabel22.grid(row=1, column=0)

wheelloaddatebutton22 = tk.Button(wheeldetailgroup22, text="Empty", font=('Helvetica', 13, 'bold'), bd=1, width=22, height=1,command = lambda: wheelloaddatebuttonselect(2,2))
wheelloaddatebutton22.grid(row=1, column=1)

wheellockstatuslabel22 = tk.Label(wheeldetailgroup22, text="Status:", font=('Helvetica', 13, 'bold'), bd=1, width=wheeldetaillabelwidth, height=wheeldetaillabelheight, anchor='w', justify=LEFT)
wheellockstatuslabel22.grid(row=2, column=0)

wheellockbutton22 = tk.Button(wheeldetailgroup22, text="UnLocked", font=('Helvetica', 13, 'bold'), bd=1, width=22, height=1,command= lambda: celllockbuttonselect(2,2))
wheellockbutton22.grid(row=2, column=1)

wheelremarkslabel22 = tk.Label(wheeldetailgroup22, text="Remarks:", font=('Helvetica', 13, 'bold'), bd=0, width=wheeldetaillabelwidth, height=wheeldetaillabelheight)
wheelremarkslabel22.grid(row=0, column=2)

wheelremarksbutton22 = tk.Button(wheeldetailgroup22, text="None", font=('Helvetica', 13), bd=0, width=wheelremarkbuttonwidth, height=wheelremarkbuttonheight,command=lambda:cellremarkbuttonselect(2,2))
wheelremarksbutton22.grid(row=1, column=2)

disptime()

try:
    ard_addr = glob.glob("/dev/ttyACM*")[0]
    logger.warning(datetimestring + " :: " + "connecting to " + ard_addr)
    ser = serial.Serial(port=str(ard_addr), baudrate = 9600)
    logger.warning(datetimestring + " :: " + "Serial variable created")
except Exception as e:
    #print("Serial declare exception")
    logger.error(datetimestring + " :: " + "Serial declare exception")
    ComErrorAlarmlabel['text']="Serial Comm Error"
    
try:
    thread = threading.Thread(target=read_from_port, args=(ser,))
    thread.daemon = True
#     print("serial thread declared")
except Exception as e:
    Statusbutton['text']="IDLE-STOP"
    #print("Thread declaration exception")
    logger.error(datetimestring + " :: " + "Thread declaration exception")
    ComErrorAlarmlabel['text']="Serial Comm Error"

freezeallitems()

try:
   ser.write(sendscaninst.encode("utf-8"))
#    print(sendscaninst)
except Exception as e:
   #print("Serial data write exception")
   logger.error(datetimestring + " :: " + "Serial data write exception-scan instruction")
   ComErrorAlarmlabel['text']="Serial Comm Error"

    
try:
    thread.start()
#     print("serial thread started")
    logger.error(datetimestring + " :: " + "serial thread started")
    
except Exception as e:
    #print("Thread start exception")
    logger.error(datetimestring + " :: " + "Thread start exception")
    ComErrorAlarmlabel['text']="Serial Comm Error"

master.mainloop()
#print("Main loop")
