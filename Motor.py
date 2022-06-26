import RPi.GPIO as GPIO
from time import time,sleep
import serial
from pydub import AudioSegment
from pydub.playback import play
Sound1 = AudioSegment.from_wav("siren.wav")
Sound2 = AudioSegment.from_wav("alerte2.wav")

def zvuk1():
    for i in range (2):
        play(Sound1)

def zvuk2():
    play(Sound2)

def setup():
  zelena = 22
  echo = 27
  trig =17    
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(zelena, GPIO.OUT)

  GPIO.setup(trig, GPIO.OUT)
  GPIO.setup(echo, GPIO.IN)

  return zelena,echo,trig

def pokreni(zelena):

 
  GPIO.output(zelena,1)

def stop(zelena):

    GPIO.output(zelena,0) 
  
  
def prekini(zelena):
    print("Uredjaj je ugasen")
    GPIO.output(zelena,0)
    #GPIO.cleanup()

def distance(echo,trig):
    # Pusti signal sa trigera, gpio.HIGH/True/1
    GPIO.output(trig, True)
    # postavi Trigger posle 0.01ms na gpio.LOW/False/0
    sleep(0.00001)
    GPIO.output(trig, False)
 
    start_time = time()
    stop_time = time()
 
    # sacuvaj pocetno vreme
    while GPIO.input(echo) == 0:
        start_time= time()
 
    # sacuvaj vreme dolaska signala do ECHO pina
    while GPIO.input(echo) == 1:
        stop_time = time()
 
    # vremenska razlika izmedju pustanja signala do dolaska
    time_elapsed = stop_time - start_time
    # pomnoziti sa brzinom zvuka (34300 cm/s)
    # i podeliti sa 2, jer se racuna polovina predjenog puta (tamo-nazad)
    distance = (time_elapsed * 34300) / 2
 
    return distance

if __name__=="__main__":
  z,e,t=setup()
  print(distance(e,t))
  pokreni(z)
  prekini()
