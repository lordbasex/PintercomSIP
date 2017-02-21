#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
import shutil

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='[%a, %d %b %Y %H:%M:%S ]',
                    filename='/var/log/pintercomsip.log',
                    filemode='w')
#logging.debug('A debug message')
#logging.info('Some information')
#logging.warning('A shot across the bows')


path = "/tmp/pintercomsip.call"
dst = "/var/spool/asterisk/outgoing/pintercomsip.call"
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(6, GPIO.IN)

try:
    while True:
        if (not GPIO.input(6)):
            logging.info('boton precionado - Led encendido')
            file = open(path,"w")
            file.write("Channel: Local/1000@pintercomsip\n")
            file.write("Extension: s\n")
            file.write("Context: street-user\n")
            file.write("Priority: 1\n")
            file.write("Callerid: PIntercomSIP\n")
            file.write("WaitTime: 35\n")
            file.write("Account: 1234567890\n")
            file.close()
            shutil.chown(path, user=120, group=125)
            shutil.move(path, dst)

            for i in range(0,5):
                GPIO.output(12,GPIO.HIGH)
                time.sleep(1)
                GPIO.output(12, GPIO.LOW)
                time.sleep(1)


            logging.info('tiempo libera proceso. - Led apagado')
finally:
    GPIO.output(12, GPIO.LOW) # por seguridad
    print ("Haciendo limpieza")
    GPIO.cleanup()
    print ("Hasta luego")
