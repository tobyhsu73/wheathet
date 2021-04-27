import serial
import time
import paho.mqtt.client as mqtt
print(time.ctime())
broker_address="broker.emqx.io"
client = mqtt.Client("P1")
client.connect(broker_address)

x=str
ser2 = serial.Serial('COM15',2400)

while True:
    A = time.ctime()
    ser2.flushInput()
    while True:
        w1=ser2.read()#讀取第一個資料風向
        w1 = bytes.decode(w1)
        if w1 == 'B':#確定風向字頭 
            break

    if w1 == 'B':
        t2=ser2.read(3)#讀取風向值
        if t2==b'\r\nA':#風向錯誤值
            continue
        winddir =bytes.decode(t2)#風向
        winddir= str(winddir)
        #print(winddir)
        ser2.read(5)
        w2 =ser2.read(1)
        w2 =bytes.decode(w2)
        
        if w2 == 'D':#確定風速字頭
            w2=ser2.read(3)
            w3=ser2.read(1)
            windrate = bytes.decode(w2)#風速
            windrate=str(windrate)
            windrate1=bytes.decode(w3)
            windrate1=str(windrate1)
            windrate=windrate+'.'+windrate1
            #print(windrate)
            ser2.read(25)
            r1=ser2.read(1)
            r1=bytes.decode(r1)
            
            if r1=="J":#確定雨量字頭
                r1=ser2.read(3)
                r2=ser2.read(1)
                rain=bytes.decode(r1)#雨量
                rain=str(rain)
                rain1=bytes.decode(r2)
                rain1=str(rain1)
                rain=rain+'.'+rain1
                #print(rain)
                ser2.read(5)
                tem1 =ser2.read(1)
                tem1 =bytes.decode(tem1)
                if tem1=='L':
                    tem=ser2.read(3)
                    tem=bytes.decode(tem)#溫度
                    tem=str(tem)
                    tem1=ser2.read(1)
                    tem1=bytes.decode(tem1)
                    tem1=str(tem1)
                    tem=tem+'.'+tem1
                    #print(tem)
                    h1=ser2.read(1)
                    h1=bytes.decode(h1)
                    if h1=='M':
                        hum=ser2.read(2)
                        hum=bytes.decode(hum)#濕度
                        hum=str(hum)
                        hum1=ser2.read(1)
                        hum1=bytes.decode(hum1)
                        hum1=str(hum1)
                        hum=hum+'.'+hum1
                        #hum=hum+'.'+hum1+'%'
                        #print(hum)
                        n1=ser2.read(1)
                        n1=bytes.decode(n1)
                        if n1 == 'N':
                            n1=ser2.read(4)
                            n2=ser2.read(1)
                            atm=bytes.decode(n1)#氣壓
                            atm1=bytes.decode(n2)
                            atm=str(atm)
                            atm1=str(atm1)
                            atm=atm+'.'+atm1
                            
                            #print(atm)
        #x=(str(A)+' wind direction '+winddir+'°'+' windrate '+windrate+' m/s'+' rainfall '+rain+' mm/hr'+' temperature '+tem+'°C'+' humidity '+hum+' atmosphere '+atm+' hpa')            
        dataDict={"wind_direction":int(winddir), "windrate":float(windrate), "rainfall":float(rain), "temperature":float(tem), "humidity":float(hum), "atmosphere":float(atm), 'time':A}
        print(dataDict)
        #print(x)
        client.publish("IDSLAB/weather station",repr(dataDict))
        
        #接收到的字串，只需以eval(str)即可轉換為dict物件
            
            
        
        
        
        
