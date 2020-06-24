import paho.mqtt.client as mqtt
from brokerData import *
import logging

logging.basicConfig( #LGHM configuracion del loggin para pruebas
    level = logging.INFO, 
    format = '[%(levelname)s] (%(processName)-10s) %(message)s'
    )

def on_connect(client, userdata, rc):
    logging.info("Conectado al broker")

def on_publish(client, userdata, mid): 
    publishText = "Publicacion satisfactoria"
    logging.debug(publishText)

def on_message(client, userdata, msg):
    #Se muestra en pantalla informacion que ha llegado
    logging.info("Ha llegado el mensaje al topic: " + str(msg.topic))
    logging.info("El contenido del mensaje es: " + str(msg.payload)) 
    papi= str(msg.topic)
    if papi[0]=="a":  #LGHM seleccionando audio
        logging.info("nel")
    else:
        pass    

client = mqtt.Client(clean_session=True) #Nueva instancia de cliente
client.on_connect = on_connect #Se configura la funcion "Handler" cuando suceda la conexion
client.on_publish = on_publish #Se configura la funcion "Handler" que se activa al publicar algo
client.on_message = on_message #Se configura la funcion "Handler" que se activa al llegar un mensaje a un topic subscrito
client.username_pw_set(MQTT_USER, MQTT_PASS) #Credenciales requeridas por el broker
client.connect(host=MQTT_HOST, port = MQTT_PORT) #Conectar al servidor remoto


def publishData(topic, value, qos = 0, retain = False): #LGHM Función para publicar datos tipo chat
    client.publish(topic, value, qos, retain)

class seleccion(object): #LGHM clase para seleccion y envio de datos
    def __init__(self, sel):#LGHM Constructor
        self.sel = str(sel)

    def chat(self):
        logging.debug(self.sel)
        #nuevo = input("1) Usuario\n2) Sala\nSeleccionar: ")
        if self.sel == str(1) :
            nuevo = input("1) Usuario\n2) Sala\nSeleccionar: ")    #LGHM seleccionar si usuario o sala
            if nuevo == str(1):
                user = input("Usuario destino: ") #LGHM escribir el carnet del usuario destino
                mensaje = input("Escriba mensaje: ")
                topic = "usuarios/03/"+user #LGHM construccion del topic 
                logging.debug(topic)
                publishData(str(topic),mensaje) #LGHM publicando en el topic deseado
                logging.debug("mensaje enviado al usuario")
            elif nuevo == str(2): #LGHM Si la eleccion fue una sala
                sala = input("Sala destino: ")
                mensaje = input("Escriba mensaje: ")
                topic = "audio/03/"+sala #LGHM construccion del topic 
                logging.info(topic)
                publishData(str(topic),mensaje) #LGHM publicando en el topic deseado
                logging.info("mensaje enviado a la sala")                
            else: logging.info("Accion no soportada")        
        elif self.sel == 2 :
            pass
        else: logging.info("Accion no soportada")        




