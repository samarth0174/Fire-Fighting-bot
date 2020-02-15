import RPi.GPIO as IO
from time import sleep

left_ir = 16
right_ir = 20
center_ir = 21
mo_px = 6
mo_py = 13
mt_px = 19
mt_py = 26
p_enable = 10
mo_x = 27 
mo_y = 22

IO.setmode(IO.BCM)
IO.setwarnings(False)
IO.setup(left_ir, IO.IN)
IO.setup(right_ir,IO.IN)
IO.setup(center_ir,IO.IN)
IO.setup(mo_px, IO.OUT)
IO.setup(mo_py, IO.OUT)
IO.setup(mt_px, IO.OUT)
IO.setup(mt_py, IO.OUT)
IO.setup(p_enable, IO.OUT)
IO.setup(mo_x, IO.OUT)
IO.setup(mo_y, IO.OUT)

pwm = IO.PWM(p_enable, 100)

def forward():
    IO.output(mo_px, True)
    IO.output(mo_py, False)
    IO.output(mt_px, True)
    IO.output(mt_py, False)
    print("Forward")
    
def reverse():
    IO.output(mo_px, False)
    IO.output(mo_py, True)
    IO.output(mt_px, False)
    IO.output(mt_py, True)
    print("Reverse")

def left():
    IO.output(mo_px, True)
    IO.output(mo_py, False)
    IO.output(mt_px, False)
    IO.output(mt_py, True)
    print("Left")
    
def right():
    IO.output(mo_px, False)
    IO.output(mo_py, True)
    IO.output(mt_px, True)
    IO.output(mt_py, False)
    print("Right")

def stop():
    IO.output(mo_px, False)
    IO.output(mo_py, False)
    IO.output(mt_px, False)
    IO.output(mt_py, False)
    print("Stop")

def pump_start():
    pwm.start(0)
    IO.output(mo_x, True)
    IO.output(mo_y, False)

def pump_stop():
    pwm.stop()
    IO.output(mo_x, False)
    IO.output(mo_y, False)


while True:
    if (IO.input(center_ir) == True and IO.input(left_ir) == True and IO.input(right_ir)== True):
        stop()
        print("No Fire")
        pump_stop()
    if (IO.input(center_ir)==False):
        forward()
        pump_start()
        print("Fire in Front")
    elif (IO.input(left_ir) == False):
        left()
        pump_start()
        print("Fire in Left")
    elif (IO.input(right_ir) == False):
        right()
        pump_start()
        print("Fire in Right")
    sleep(0.3)
    
IO.cleanup()
