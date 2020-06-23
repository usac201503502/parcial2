import paho.mqtt.client as mqtt
import binascii as bichito
import logging
import threading
import time
import os 
import sys
from selec import *

logging.basicConfig( #LGHM  configuración inicial del logging
    level = logging.INFO,
    format = '[%(levelname)s] (%(threadName)-10s) %(message)s'
    )

archivo = open("usuario1.txt", "r")
com = "comandos"
com1 ="/03/"+str(archivo.read())

def estatus ():
    while True :
        logging.info("Esperando publicaciones...")
        time.sleep(10)
def escribir ():        
        holis = seleccion(input("1) Enviar Texto\n2) Enviar Audio\nSeleccionar: "))
        holis.chat()
        time.sleep(0.1)
qos = 2
client.subscribe([(str(com+com1), qos), ("comandos/03/201503408", qos), ("comandos/03/201513732", qos),("usuarios/03/201503502", qos)])


t1 = threading.Thread(name = 'Esperando',
                        target = estatus,
                        args = (),
                        daemon = True
                        )

t2 = threading.Thread(name = 'Enviando',
                        target = escribir,
                        args = (),
                        daemon = True
                        )                        

client.loop_start() #LGHM se inicia el hilo y se mantiene en el fondo esperando publicaciones de suscriptores
t1.start()   
t2.start()

try:
    while True:
        pass  
        #logging.debug("Esperando publicaciones...")
        #holis = seleccion(input("1) Enviar Texto\n2) Enviar Audio\nSeleccionar: "))
        #holis.chat()
        #time.sleep(10)

except KeyboardInterrupt:
    logging.warning("Desconectando del broker...")
    if t1.isAlive():
        t1._stop()

    

finally:
    client.loop_stop() #Se mata el hilo que verifica los topics en el fondo
    client.disconnect() #Se desconecta del broker
    logging.info("Desconectado del broker. Saliendo...")
    sys.exit()