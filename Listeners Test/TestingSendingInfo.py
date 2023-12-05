from flask import Flask, render_template, Response, request, send_from_directory
import cv2
import threading
from tkinter import *
import PIL.ImageGrab
from numpy import asarray
import psycopg2
import time


Running = True

pi_camera = cv2.VideoCapture(1)
#pi_camera = VideoCamera(flip=False) # flip pi camera if upside down.

# App Globals (do not edit)
app = Flask(__name__)
Title = ""

@app.route('/')
def index():
    return render_template('test.html')
          
@app.route("/Dy_update")
def Dy_update():
     global Title
     return {
        "TitleChange": Title,
        "time": time.time()
     }

@app.route('/T1')
def T1(): global Title; Title += "Hello "; return "None"

@app.route('/T2')
def T2():global Title; Title += "World "; return "None"

@app.route('/T3')
def T3():global Title; Title += "Test "; return "None"

@app.route('/T4')
def T4():global Title; Title += "Test 2 "; return "None"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)