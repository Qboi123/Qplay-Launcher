from inputs import get_gamepad, devices
import math
import threading


class XboxController(object):
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):

        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0

        self._monitor_thread = threading.Thread(target=self.update, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()
        self.root2 = Tk()
        self.label2 = Label(self.root2)
        self.label2.pack()


    def read(self):
        x = self.LeftJoystickX
        y = self.LeftJoystickY
        a = self.A
        b = self.X # b=1, x=2
        rb = self.RightBumper
        return [x, y, a, b, rb]


    def update(self):
        a = devices.gamepads[0]
        print(a.__dict__)
        print(a.__dict__.keys())
        self.label2.config(text=str(a.__dict__.keys()))
        self.root2.update()
        self.root2.update_idletasks()
        events = get_gamepad()
        for event in events:
            if event.code == 'ABS_Y':
                self.LeftJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
            elif event.code == 'ABS_X':
                self.LeftJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
            elif event.code == 'ABS_RY':
                self.RightJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
            elif event.code == 'ABS_RX':
                self.RightJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
            elif event.code == 'ABS_Z':
                self.LeftTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
            elif event.code == 'ABS_RZ':
                self.RightTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
            elif event.code == 'BTN_TL':
                self.LeftBumper = event.state
            elif event.code == 'BTN_TR':
                self.RightBumper = event.state
            elif event.code == 'BTN_SOUTH':
                self.A = event.state
            elif event.code == 'BTN_NORTH':
                self.X = event.state
            elif event.code == 'BTN_WEST':
                self.Y = event.state
            elif event.code == 'BTN_EAST':
                self.B = event.state
            elif event.code == 'BTN_THUMBL':
                self.LeftThumb = event.state
            elif event.code == 'BTN_THUMBR':
                self.RightThumb = event.state
            elif event.code == 'BTN_SELECT':
                self.Back = event.state
            elif event.code == 'BTN_START':
                self.Start = event.state
            elif event.code == 'BTN_TRIGGER_HAPPY1':
                self.LeftDPad = event.state
            elif event.code == 'BTN_TRIGGER_HAPPY2':
                self.RightDPad = event.state
            elif event.code == 'BTN_TRIGGER_HAPPY3':
                self.UpDPad = event.state
            elif event.code == 'BTN_TRIGGER_HAPPY4':
                self.DownDPad = event.state


from tkinter import *

root = Tk()
label = Label(root)
label.pack()

xbox = XboxController()

while True:

    xbox.update()
    a = [int(xbox.LeftJoystickX * 7), int(xbox.LeftJoystickY * 7)]
    b = [int(xbox.RightJoystickX* 7), int(xbox.RightJoystickY * 7)]
    
    c = """====================================
    Left Joystick Position:"""+str(a)+"""
    Right Joystick Position:"""+str(b)+""")
    
    A Button:"""+str(bool(xbox.A))+"""
    B Button:"""+str(bool(xbox.B))+"""
    X Button:"""+str(bool(xbox.X))+"""
    Y Button:"""+str(bool(xbox.Y))+"""
    
    UP Button:"""+str(bool(xbox.UpDPad))+ """
    DOWN Button:"""+str(bool(xbox.DownDPad))+ """
    LEFT Button:"""+str(bool(xbox.LeftDPad))+ """
    RIGHT Button:"""+str(bool(xbox.RightDPad))+ """
    
    START Button:"""+str(bool(xbox.Start))+ """
    BACK Button:"""+str(bool(xbox.Back))

    label.config(text=c)
    root.update()
    root.update_idletasks()
