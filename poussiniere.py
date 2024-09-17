import network
import urequests
import utime
import machine
from machine import Pin, SoftI2C
import ssd1306
sta = network.WLAN(network.STA_IF)
 
if not sta.isconnected():
    print('connecting to network...')
    sta.active(True)
    sta.connect("raspi-SIN", "SINisBest")
 
    while not sta.isconnected():
        pass
 
print('network config:', sta.ifconfig())

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))# Pin pour l'afficheur
display = ssd1306.SSD1306_I2C(128, 64, i2c)
timer = machine.Timer(0)
 
def comptageminutes(timer):
    global minute
    minute = minute + 1
 
timer.init(period=60000, mode=machine.Timer.PERIODIC, callback=comptageminutes)# une interruption pour réduire l'écart

resp = urequests.get("http://10.24.2.43:8000/heuresysteme", headers = {'content-type': "application/x-www-form-urlencoded"})#permet d'afficher l'heure pour programmer les repas
temps = resp.text

print(temps)
print("quelle heure est-il?")
minute= int(resp.text[4:6])
heure= int(resp.text[1:3])
utime.sleep(1)
print(resp.text[1:3]+":"+str(minute))
resp.close()


while True:
    rep = urequests.get("http://10.24.2.43:8000/intervalle/reception", headers = {'content-type': "application/x-www-form-urlencoded"})
    nouri = rep.text
    rep.close()
    print("quelle est l'intervalle de distribution des repas")
    print(nouri)
    
    
    minute_repas = minute + int(nouri)
    if minute_repas > 59:
        heure_repas = heure + (minute_repas // 60)
        minute_repas -= 60
    print("prochain repas :", heure_repas," : ", minute_repas)     
    
    if heure_repas== heure and minute_repas == minute :
        urequests.post("http://10.24.2.43:8000/repas/ajout", data = "repas=1", headers = {'content-type': "application/x-www-form-urlencoded"})
    
#     current_time = utime.localtime(utime.time())
#     heure = current_time[3]
#     minute = current_time[4]
#     seconde = current_time[5]
    if minute> 59:
        minute=0
        heure+=1
    affichage=str(heure)+":"+str(minute)
    affichages=str(heure_repas)+":"+str(minute_repas)
    display.fill(0)
    display.text(affichage, 50, 10)
    display.text(affichages,50, 30)
    display.show()
    utime.sleep(5)