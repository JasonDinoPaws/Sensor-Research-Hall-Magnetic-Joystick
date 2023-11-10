import RPi.GPIO as GPIO
from gpiozero import MCP3008
import pyautogui

screenWidth, screenHeight = pyautogui.size()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

PX = MCP3008(channel=1, clock_pin=11, mosi_pin=10, miso_pin=9, select_pin=8)
PP = 17
PY = MCP3008(channel=0, clock_pin=11, mosi_pin=10, miso_pin=9, select_pin=8)

R = 21
G = 16
B = 20

GPIO.setup(PP, GPIO.IN, pull_up_down = GPIO.PUD_UP)

GPIO.setup(R, GPIO.OUT)
GPIO.setup(G, GPIO.OUT)
GPIO.setup(B, GPIO.OUT)

GPIO.output(R, 0)
GPIO.output(G, 0)
GPIO.output(B, 0)

try:
    while True:
        X = PX.value > .6 and 1 or PX.value < .4 and -1 or 0
        Y = PY.value > .6 and -1 or PY.value < .4 and 1 or 0

        pyautogui.move(X*15, Y*15)
        if GPIO.input(PP) == 1:
            pyautogui.click() 
        print("X: ",X,"Y: ",Y,"Presed: ",GPIO.input(PP))
except (EOFError,KeyboardInterrupt):
    GPIO.cleanup()