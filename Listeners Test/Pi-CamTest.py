from flask import Flask, render_template, Response, request, send_from_directory
import cv2
import threading
from tkinter import *
import PIL.ImageGrab
from numpy import asarray


Running = True

pi_camera = cv2.VideoCapture(1)
#pi_camera = VideoCamera(flip=False) # flip pi camera if upside down.

# App Globals (do not edit)
app = Flask(__name__)
VideoFeed = None
Connected,Controlling = 0,0

@app.route('/')
def index():
    return render_template('index.html') #you can customze index.html here

def gen(camera):
        global VideoFeed
        while True:
            frame = cv2.imencode('.png', VideoFeed)[1].tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(cv2.VideoCapture(0)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def move(NX,NY):
     global X,Y
     X += NX*15
     Y += NY*15

@app.route('/L')
def L(): move(-1,0); return "None"

@app.route('/R')
def R(): move(1,0); return "None"

@app.route('/D')
def D(): move(0,1); return "None"

@app.route('/U')
def U(): move(0,-1); return "None"

def Game():
    global X,Y,VideoFeed,Connected,Controlling
    window = Tk()
    window.configure(background='black')
    window.attributes("-fullscreen",True)
    window.wm_title("Game")

    c = Canvas(window,width=window.winfo_screenwidth(),height=window.winfo_screenheight(),bg='grey56',borderwidth=0,highlightthickness=0)
    c.pack()

    def createText(txt,X,Y,An):
        lab = Label(c, text=txt, font=('Helvetica 15 bold'),bg = "grey56",bd=1)
        lab.pack(anchor="nw")
        lab.place(x = X,y = Y)
        return lab

    XT = createText("X: "+str(X),5,5,"nw")

    YT = createText("Y: "+str(Y),5,35,"nw")

    X,Y = c.winfo_reqwidth()/2,c.winfo_reqheight()/2
    Size = 25
    plr = c.create_rectangle(X,Y, X+Size,Y+Size, fill= "black", outline="")
    while Running:
        XT["text"] = "X: "+str(X)
        YT["text"] = "Y: "+str(Y)
        c.moveto(plr,X,Y)
        window.update()
        VideoFeed = asarray(PIL.ImageGrab.grab())
          
if __name__ == '__main__':
    threading.Thread(target=Game).start()
    app.run(host='0.0.0.0', debug=False)
    Running = False