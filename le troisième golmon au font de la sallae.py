import network
import urequests
import utime
import machine
sta = network.WLAN(network.STA_IF)
 
if not sta.isconnected():
    print('connecting to network...')
    sta.active(True)
    sta.connect("raspi-SIN", "SINisBest")
    
    while not sta.isconnected():
        pass
 
print('network config:', sta.ifconfig())
 

timer = machine.Timer(0)
 
def comptageminutes(timer):
        global minutes
        minutes+=1
 
timer.init(period=10000, mode=machine.Timer.PERIODIC, callback=comptageminutes)
print("quelle heure est-il?")
while True:
    resp = urequests.get("http://10.24.2.43:8000/heuresysteme", headers = {'content-type': "application/x-www-form-urlencoded"})
   
    print(resp.text)
    minutes= int(resp.text[4:6])
    print(resp.text[1:3]+":"+str(minutes))
    utime.sleep(60)



#print(heures,minutes)