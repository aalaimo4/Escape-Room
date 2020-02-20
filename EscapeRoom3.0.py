#!/usr/bin/env python3
########################################################################
# Filename    : I2CLCD1602.py
# Description : Use the LCD display data
# Author      : freenove
# modification: 2018/08/03
########################################################################
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD
from time import sleep, strftime
from datetime import datetime

import RPi.GPIO as GPIO
import MFRC522
import sys
import os

# for camera
from picamera import PiCamera
from time import sleep

camera = PiCamera()
#camera.start_preview(alpha=200)

# Create an object of the class MFRC522
mfrc = MFRC522.MFRC522()

#for keypad
import RPi.GPIO as GPIO
import Keypad       #import module Keypad

ROWS = 4        # number of rows of the Keypad
COLS = 4        #number of columns of the Keypad
keys =  [   '1','2','3','A',    #key code
            '4','5','6','B',
            '7','8','9','C',
            '*','0','#','D'     ]
rowsPins = [18,32,36,37]        #connect to the row pinouts of the keypad
colsPins = [35,33,31,29]        #connect to the column pinouts of the keypad

# for  timer
import time
                    
    
def loop1():
    t = 3600
    i = 1
    mcp.output(3,1)     # turn on LCD backlight
    lcd.begin(16,2)     # set number of LCD lines and columns
    
    # for keypad
    keypad = Keypad.Keypad(keys,rowsPins,colsPins,ROWS,COLS)    #creat Keypad object
    keypad.setDebounceTime(50)      #set the debounce time
    
    global mfrc
    mfrc = MFRC522.MFRC522()
    isScan = True
    global pass1, pass2, pass3, pass4, pass5, timetocum
    pass1 = 0
    pass2 = 0
    pass3 = 0
    pass4 = 0
    pass5 = 0
    timetocum = 0
    
    while(True):
        
        # for keypad
        key = keypad.getKey()       #obtain the state of keys
        if(key != keypad.NULL):     #if there is key pressed, print its key code.
            print ("You Pressed Key : %c "%(key))
            pass5 = pass4
            pass4 = pass3
            pass3 = pass2
            pass2 = pass1
            pass1 = key
            
        if(key == "A" or key == "B"):
            camera.capture('/home/pi/Desktop/image%s.jpg' % i)
            lcd.clear()
            lcd.message('Picture Taken!\n')
            time.sleep(3)
            t = t - 3
            i = i + 1
            
        if(key == "*"):
            print (pass5,pass4,pass3,pass2)
            
            if(pass5 == "0"):
                if(pass4 =="2"):
                    if(pass3 == "1"):
                        if(pass2 == "5"):
                            print('You win!')
                            lcd.clear()
                            lcd.message( "-Bomb Disarmed-\n" )
                            lcd.message( "-----"+timeformat+"-----" )
                            camera.capture('/home/pi/Desktop/Winning.jpg')
                            return(False)
                            
        # for RFID
        # Scan for cards    
        (status,TagType) = mfrc.MFRC522_Request(mfrc.PICC_REQIDL)
        # If a card is found
        if status == mfrc.MI_OK:
            print ("Card detected")
            lcd.clear()
            lcd.message('Token Accepted\n')
            lcd.message('LOCK#004 16.29.7')
            time.sleep(5)
            t = t - 5
        
        # for timer
        mins, secs = divmod(t,60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        t-= 1
        #######################
              
        lcd.setCursor(0,0)  # set cursor position
        lcd.clear()
        lcd.message( 'Enter Code: '+ str(pass4) + str(pass3) + str(pass2) + str(pass1) +'\n' )# display code
        lcd.message( timeformat )   # display the time
        
        
            
        
def destroy():
    lcd.clear()
    #camera.stop_preview()
    
PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
# Create PCF8574 GPIO adapter.
try:
    mcp = PCF8574_GPIO(PCF8574_address)
except:
    try:
        mcp = PCF8574_GPIO(PCF8574A_address)
    except:
        print ('I2C Address Error !')
        exit(1)
# Create LCD, passing in MCP GPIO adapter.
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)

if __name__ == '__main__':
    print ('Program is starting ... ')

    try:
        loop1()
        
    except KeyboardInterrupt:
        destroy()
        #camera.stop_preview()

