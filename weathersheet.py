import serial
import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials
t=0
try:
    
    ser2 = serial.Serial('COM15',2400)
    auth_json_path = 'D:\lab\py2\idslab-d70a2e57470c.json'
    gss_scopes = ['https://spreadsheets.google.com/feeds' ]
    #連線
    credentials = ServiceAccountCredentials.from_json_keyfile_name(auth_json_path,gss_scopes)
    gss_client = gspread.authorize(credentials)
    #開啟 Google Sheet 資料表
    spreadsheet_key = '1SP5U7RmoU-_cDnrPJNAp2gkWDRq4bSE8JrOllBJzr9k'
    sheet = gss_client.open_by_key(spreadsheet_key).sheet1
    #sheet.clear()
    listtitle=["year","month","date","hour:minute","wind direction","windrate","rainfall","temperature","humidity",'atmosphere']
    sheet.append_row(listtitle)
    while True:
        
        x = time.ctime()
        year=x[20]+x[21]+x[22]+x[23]
        month=x[4]+x[5]+x[6]
        date=x[8]+x[9]
        hour=x[10]+x[11]+x[12]+x[13]+x[14]+x[15]
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


        listdata=[year,month,date,hour,winddir,windrate,rain,tem,hum,atm]
        sheet.append_row(listdata)
        t=t+1
        time.sleep(300)
except:
    pass
