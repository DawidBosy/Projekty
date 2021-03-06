import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(5,GPIO.OUT)
GPIO.setup(6,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(19,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)

print("LED on")

GPIO.output(5,GPIO.HIGH)
GPIO.output(6,GPIO.HIGH)
GPIO.output(13,GPIO.HIGH)
GPIO.output(19,GPIO.HIGH)
GPIO.output(26,GPIO.HIGH)

time.sleep(1)
print("LED off")

GPIO.output(5,GPIO.LOW)
GPIO.output(6,GPIO.LOW)
GPIO.output(13,GPIO.LOW)
GPIO.output(19,GPIO.LOW)
GPIO.output(26,GPIO.LOW)
