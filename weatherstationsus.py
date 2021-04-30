import paho.mqtt.client as mqtt #import the client1
import time
############
def on_message(client, userdata, message):
    x=str(message.payload.decode("utf-8"))
    if message.retain==1:
        print("This is a retained message")
    data=eval(x)#data是接收到的資料dictionary，可以直接用
    print(data)
    print(data['wind_direction'])
    print(data['rainfall'])
#######################################
broker_address="broker.emqx.io"
#broker_address="iot.eclipse.org"
while True:
    client = mqtt.Client("P555") #create new instance要記得更改，隨便一個id都可以
    client.on_message=on_message #attach function to callback

    client.connect(broker_address) #connect to broker
    client.loop_start() #start the loop

    client.subscribe("IDSLAB/weather station")
    

    time.sleep(1) # wait
    client.loop_stop()
   