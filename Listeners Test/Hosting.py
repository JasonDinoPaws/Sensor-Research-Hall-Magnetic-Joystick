import tkinter as tk
from flask import Flask, render_template, Response, request, send_from_directory
import threading
import cv2


Running = True

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

class DrawableGrid(tk.Frame):
    def __init__(self, parent, width, height, size=5):
        super().__init__(parent, bd=1, relief="sunken")
        self.width = width
        self.height = height
        self.size = size
        canvas_width = width*size
        canvas_height = height*size
        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0, width=canvas_width, height=canvas_height)
        self.canvas.pack(fill="both", expand=True, padx=2, pady=2)

        for row in range(self.height):
            for column in range(self.width):
                x0, y0 = (column * size), (row*size)
                x1, y1 = (x0 + size), (y0 + size)
                self.canvas.create_rectangle(x0, y0, x1, y1,
                                             fill="white", outline="gray",
                                             tags=(self._tag(row, column),"cell" ))
        self.canvas.tag_bind("cell", "<B1-Motion>", self.paint)
        self.canvas.tag_bind("cell", "<1>", self.paint)

    def _tag(self, row, column):
        """Return the tag for a given row and column"""
        tag = f"{row},{column}"
        return tag

    def get_pixels(self):
        while Running:
            row = ""
            for row in range(self.height):
                output = ""
                for column in range(self.width):
                    color = self.canvas.itemcget(self._tag(row, column), "fill")
                    value = "1" if color == "black" else "0"
                    output += value
                yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + cv2.imencode('.png', output)[1].tobytes() + b'\r\n')

    def paint(self, event):
        cell = self.canvas.find_closest(event.x, event.y)
        self.canvas.itemconfigure(cell, fill="black")



def Game():
    global canvas
    root = tk.Tk()
    canvas = DrawableGrid(root, width=20, height=15, size=10)
    b = tk.Button(root, text="Print Data", command=canvas.get_pixels)
    b.pack(side="top")
    canvas.pack(fill="both", expand=True)
    root.mainloop()

@app.route('/video_feed')
def video_feed():
    global canvas
    return Response(canvas.get_pixels(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    threading.Thread(target=Game).start()
    app.run(host='0.0.0.0', debug=False)
    Running = False