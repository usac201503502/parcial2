import paho.mqtt.client as mqtt
from brokerData import *
import threading
import logging
import os


logging.basicConfig( #LGHM configuracion del loggin para pruebas
    level = logging.WARNING, 
    format = '[%(levelname)s] (%(processName)-10s) %(message)s'
    )

def on_connect(client, userdata, rc):
    logging.info("Conectado al broker")

def on_publish(client, userdata, mid): 
    publishText = "Publicacion satisfactoria"
    logging.debug(publishText)

def rep_audio(): #LGHM Funcion para hilo de reproducion de audio
    os.system('aplay Recibido.wav') #PJHB

def grab_audio(tiempo, user):
    os.system('arecord -d '+str(tiempo)+' -f U8 -r 8000 prueba.wav')
    audio = open("prueba.wav", "rb") #PJHB Se abre el archivo de audio a enviar en bytes crudos
    leer_audio = audio.read() #PJHB Lectura de la información del archivo de audio
    audio.close()
    enviar_audio = bytearray(leer_audio) #PJHB Se crea un arreglo de bytes en el cual se colocara cada byte del audio
    topic = "audio/03/"+user #LGHM construccion del topic 
    logging.debug(topic)
    publishData(str(topic),enviar_audio) #LGHM publicando en el topic deseado
    logging.debug("audio enviado al usuario")

def on_message(client, userdata, msg):
    #Se muestra en pantalla informacion que ha llegado
    papi= str(msg.topic)
    if papi[0]=="a":  #LGHM si es audio proceder a reproducirlo
        logging.info("Ha llegado el audio al topic: " + str(msg.topic))
        print (papi.split('/')[2]+': Reproduciendo audio...')
        logging.info("Reproduciendo: ") 
        data = msg.payload
        
        file = open("Recibido.wav", "wb") #PJHB Crea archivo de audio
        recibir_audio = file.write(data) #PJHB 
        file.close() #PJHB
        t3 = threading.Thread(name = 'Escuchando', #LGHM hilo para escuchar el audio y seguir programa principal
                        target = rep_audio,
                        args = (),
                        daemon = True
                        )
        t3.start()
    else: #LGHM si es texto tipo usuario o sala procede normalmente
        logging.info("Ha llegado el mensaje al topic: " + str(msg.topic))
        logging.info("El contenido del mensaje es: " + str(msg.payload))
        wenas = str(msg.topic) 
        wenas2 = msg.payload
        print(wenas.split('/')[2]+': '+str(wenas2.decode('utf-8')))  
        


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
                topic = "salas/03/"+sala #LGHM construccion del topic 
                logging.info(topic)
                publishData(str(topic),mensaje) #LGHM publicando en el topic deseado
                logging.info("mensaje enviado a la sala")                
            else: logging.info("Accion no soportada")        
        elif self.sel == str(2) :
            nuevo = input("1) Usuario\n2) Sala\nSeleccionar: ") #LGHM seleccionar si usuario o sala
            if nuevo == str(1):
                user = input("Usuario destino: ") #LGHM escribir el carnet del usuario destino
                tiempo = str(input("Duracion de grabacion [s]: ")) #LGHM agregar duracion en segundos 

                t = str(tiempo)
                t5 = threading.Thread(name = 'grabando', #LGHM hilo para grabar 
                        target = grab_audio,
                        args = (t,user),
                        daemon = True
                        )
                t5.start()

            elif nuevo == str(2): #LGHM Si la eleccion fue una sala
                sala = input("Sala destino: ")
                tiempo = str(input("Duracion de grabacion [s]: ")) #LGHM agregar duracion en segundos 
                t = str(tiempo)
                t6 = threading.Thread(name = 'grabando2', #LGHM hilo para grabar 
                        target = grab_audio,
                        args = (t,sala),
                        daemon = True
                        )
                t6.start()              
            else: logging.info("Accion no soportada") 
        else: logging.info("Accion no soportada")        




