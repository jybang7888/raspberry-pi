import RPi.GPIO as GPIO
import time

buzzer = 2
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.setwarnings(False)

while True:
  GPIO.output(2, True)
  time.sleep(1)
  GPIO.OUTPUT(2, False)
  time.sleep(2)
