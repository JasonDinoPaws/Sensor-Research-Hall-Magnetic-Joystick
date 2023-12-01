from tkinter import *
from time import sleep
from random import *
from flask import Flask, render_template, Response, request, send_from_directory
import threading


Running = True

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

X,Y = 0,0
Size = 25
VideoFeed = ""

def Movement():
    global X,Y,IsShift
    IsShift = False
    X += 1
    Y += 1

def Game():
    global X,Y,VideoFeed

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


    buttons = []
    snake = []

    def createText(txt,X,Y):
        lab = Label(c, text=txt, font=('Helvetica 15 bold'),bg = "grey56",bd=1)
        lab.pack(anchor="w")
        lab.place(x = X,y = Y)
        return lab

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
        while Running:
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
            VideoFeed = window.frame()
            print(bytes(en))
    except (EOFError,KeyboardInterrupt):
        print()

@app.route('/video_feed')
def video_feed():
    global VideoFeed
    return Response(VideoFeed,mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    threading.Thread(target=Game).start()
    app.run(host='0.0.0.0', debug=False)
    Running = False