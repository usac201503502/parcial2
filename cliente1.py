import paho.mqtt.client as mqtt
import logging
import time
import os 
from brokerData import *

logging.basicConfig( #LGHM  configuración inicial del logging
    level = logging.DEBUG, 
    format = '[%(levelname)s] (%(threadName)-10s) %(message)s'
    )


def on_connect(client, userdata, rc):
    logging.info("Conectado al broker")

def on_message(client, userdata, msg):
    #Se muestra en pantalla informacion que ha llegado
    logging.info("Ha llegado el mensaje al topic: " + str(msg.topic))
    logging.info("El contenido del mensaje es: " + str(msg.payload))        

client = mqtt.Client(clean_session=True) #Nueva instancia de cliente
client.on_connect = on_connect #Se configura la funcion "Handler" cuando suceda la conexion
client.on_message = on_message #Se configura la funcion "Handler" que se activa al llegar un mensaje a un topic subscrito
client.username_pw_set(MQTT_USER, MQTT_PASS) #Credenciales requeridas por el broker
client.connect(host=MQTT_HOST, port = MQTT_PORT) #Conectar al servidor remoto

#Nos conectaremos a distintos topics:
qos = 2

#Subscripcion simple con tupla (topic,qos)
#client.subscribe(("sensores/6/hum", qos))

#Subscripcion multiple con lista de tuplas
client.subscribe([("comandos/03/201503502", qos), ("comandos/03/201503408", qos), ("comandos/03/201513732", qos)])


client.loop_start() #LGHM se inicia el hilo y se mantiene en el fondo esperando publicaciones de suscriptores

try:
    while True:
        logging.info("Esperando publicaciones...")
        time.sleep(10)

except KeyboardInterrupt:
    logging.warning("Desconectando del broker...")

finally:
    client.loop_stop() #Se mata el hilo que verifica los topics en el fondo
    client.disconnect() #Se desconecta del broker
    logging.info("Desconectado del broker. Saliendo...")