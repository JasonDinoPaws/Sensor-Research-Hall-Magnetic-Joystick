from Listener import myClass
import pyautogui

myclass = myClass()

def Pressed(Key):
    print(Key)
def Released(Key):
    print(Key)

myclass.On_Pressed(callback=Pressed)
myclass.On_Released(callback=Released)