import RPi.GPIO as GPIO
from random import random
from time import sleep

R = 21
G = 16
B = 20

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN)
GPIO.setwarnings(False)
GPIO.setup(R, GPIO.OUT)
GPIO.setup(G, GPIO.OUT)
GPIO.setup(B, GPIO.OUT)

GPIO.output(R, 0)
GPIO.output(G, 0)
GPIO.output(B, 0)


Colors  = [False,False,False]

try:
    while True:
        if GPIO.input(18) == 0:
            Colors = [
                random() > .5,
                random() > .5,
                random() > .5
            ]
        sleep(.1)
        GPIO.output(R, GPIO.input(18) == 0 and Colors[0] or False)
        GPIO.output(G, GPIO.input(18) == 0 and Colors[1] or False)
        GPIO.output(B, GPIO.input(18) == 0 and Colors[2] or False)
except (EOFError,KeyboardInterrupt):
    GPIO.cleanup()
