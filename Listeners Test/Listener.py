import keyboard
class myClass:
    def __init__(self):
        self.__result = 0
        self.connected = {"Pressed": [],"Released": []}

    def pressed(self, Key):
        for listener in self.connected["Pressed"]:
            listener(Key)
    keyboard.on_press(callback=pressed)

    def pressed(self, Key):
        for listener in self.connected["Released"]:
            listener(Key)
    keyboard.on_release(callback=pressed)

    def On_Pressed(self, callback):
        self.connected["Pressed"].append(callback)

    def On_Released(self, callback):
        self.connected["Released"].append(callback)