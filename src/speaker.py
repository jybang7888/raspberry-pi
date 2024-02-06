import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

pwm = GPIO.PWM(18, 262)
pwm.start(50.0)
time.sleep(0.5)

pwm.stop()
GPIO.cleanup()
