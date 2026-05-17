
import network
import time
from machine import Pin
import dht
from umqtt.simple import MQTTClient

#Nova biblioteca para importar (nao esquecer do outro arquivo .py)
from servo import Servo

MQTT_CLIENT_ID = "meu_esp_32"
MQTT_BROKER    = "broker.mqttdashboard.com"
MQTT_USER      = ""
MQTT_PASSWORD  = ""
MQTT_TOPIC     = "mica_lamp"

sensor = dht.DHT22(Pin(15))
botao = Pin(32, Pin.IN, Pin.PULL_DOWN)
led = Pin(27, Pin.OUT)                      
servo = Servo(pin=16, start=0)                  #Definindo o servo

print("Conectando ao Wifi", end="")   
sta_if = network.WLAN(network.STA_IF) 
sta_if.active(True)                   
sta_if.connect('Wokwi-GUEST', '')     
while not sta_if.isconnected():       
  print(".")                          
  time.sleep(0.3)                      
print(" Conectado!")

print("Conectando ao MQTT server")
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
client.connect()                      
print("Deu boa malandragem!")

def mqtt_message(topic, msg):
  msg = msg.decode('utf-8')
  print("Incoming message:", msg)
  if(msg=='on'):
    led.on()
  if(msg=='off'):
    led.off()
  if msg.startswith("servo"):
    ang = int(msg[5:])                        #Ajustes no Callback para servo
    servo.move(ang)

client.set_callback(mqtt_message)           
client.subscribe(MQTT_TOPIC)                

while True:
    if botao.value():
        sensor.measure()

        temperatura = sensor.temperature()
        umidade = sensor.humidity()

        print("Temperatura:", temperatura)
        print("Umidade:", umidade)

        client.publish("mica_lamp/temperatura", str(temperatura))
        client.publish("mica_lamp/umidade", str(umidade))

        time.sleep(1)

    client.check_msg()
    time.sleep(0.2)                 
    



