from tkinter import *
from time import sleep
from random import *
import RPi.GPIO as GPIO
from gpiozero import MCP3008, DigitalInputDevice

window = Tk()
window.configure(background='black')
window.attributes("-fullscreen",True)
window.wm_title("Game")

c = Canvas(window,width=window.winfo_screenwidth(),height=window.winfo_screenheight(),bg='grey56',borderwidth=0,highlightthickness=0)
c.pack()

X,Y = c.winfo_reqwidth()/2,c.winfo_reqheight()/2
LX,LY = 0,0
Size = 25
MLan = 25
IsShift = False
NS,SS = 2,5



PX = MCP3008(channel=1, clock_pin=11, mosi_pin=10, miso_pin=9, select_pin=8)
PP = 17
PY = MCP3008(channel=0, clock_pin=11, mosi_pin=10, miso_pin=9, select_pin=8)


GPIO.setup(PP, GPIO.IN, pull_up_down = GPIO.PUD_UP)

buttons = []
snake = []

def CreateButton(t,fun,X,Y,BG,W):
    butoo = Button(c, text = t, font=('Helvetica 15 bold'), command = fun,anchor="center",bg=BG or "grey56",width= W or 0)
    butoo.place(x = X,y = Y)
    buttons.append(butoo)
    
def XMove():
    X = PX.value > .6 and "r" or PX.value < .4 and "l" or "n"
    return  X #or (keyboard.is_pressed("a") or keyboard.is_pressed("Left")) and "l" or (keyboard.is_pressed("d") or keyboard.is_pressed("Right")) and "r" or "n"

def YMove():
    Y = PY.value > .6 and "d" or PY.value < .4 and "u" or "n"
    return Y #or (keyboard.is_pressed("w") or keyboard.is_pressed("UP")) and "d" or (keyboard.is_pressed("s") or keyboard.is_pressed("Down")) and "u" or "n"

def Close():
    window.destroy()

def createText(txt,X,Y):
    lab = Label(c, text=txt, font=('Helvetica 15 bold'),bg = "grey56",bd=1)
    lab.pack(anchor="w")
    lab.place(x = X,y = Y)
    return lab

CreateButton("X",Close,c.winfo_reqwidth()-55,5,"red",3)

XT = createText("X: "+str(X),5,c.winfo_reqheight()-75)

YT = createText("Y: "+str(Y),5,c.winfo_reqheight()-45)

Spint = createText("Move Faster: Shift,Center",5,15)


def invert():
    for i in snake:
        c.itemconfig(i, fill= IsShift and "grey56" or "black")
    c.configure(bg= IsShift and "black" or "grey56")
    XT.config(bg = IsShift and "black" or "grey56",fg = IsShift and "grey56" or "black")
    YT.config(bg = IsShift and "black" or "grey56",fg = IsShift and "grey56" or "black")
    Spint.config(bg= IsShift and "black" or "grey56",fg = IsShift and "green2" or "red2")
        

try:
    while True:
        IsShift = GPIO.input(PP) == 1 #or keyboard.is_pressed("Shift")
        X += (X > Size and XMove() == "l" and (IsShift and  -SS or -NS)) or (X < (c.winfo_reqwidth()-Size) and XMove() == "r" and (IsShift and  SS or NS)) or 0
        Y += (Y > Size and YMove() == "d" and (IsShift and  -SS or -NS)) or (Y < (c.winfo_height()-Size) and YMove() == "u" and (IsShift and  SS or NS)) or 0

        XT["text"] = "X: "+str(X)
        YT["text"] = "Y: "+str(Y)
        invert()

        if LX != X or LY != Y:
            snake.append(c.create_rectangle(X-Size,Y-Size, X+Size,Y+Size, fill= IsShift and "grey56" or "black", outline=""))
            LX = X
            LY = Y
            if len(snake) > MLan:
                c.delete(snake[0])
                snake.pop(0)
        elif len(snake) > 1:
            c.delete(snake[0])
            snake.pop(0)
        
        window.update()
except (EOFError,KeyboardInterrupt):
    window.destroy()
