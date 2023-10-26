#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick

from pybricks.ev3devices import (
    Motor,
    TouchSensor,
    ColorSensor,
    InfraredSensor,
    UltrasonicSensor,
    GyroSensor,
)
from pybricks.parameters import (
    Port,
    Stop,
    Direction,
    Button,
    Color,
    SoundFile,
    ImageFile,
    Align,
)
from pybricks.tools import print, wait, StopWatch

import struct

ev3 = EV3Brick()

# Declare motors
left_motor = Motor(Port.A)
right_motor = Motor(Port.D)
left_arm = Motor(Port.B)

arm = 0


# A helper function for converting stick values (0 - 255)
# to more usable numbers (-100 - 100)
def scale(val, src, dst):
    value = int((float(val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0])
    return value


# Open the Gamepad event file:
# /dev/input/event3 is for PS3 gamepad
# /dev/input/event4 is for PS4 gamepad
# look at contents of /proc/bus/input/devices if either one of them doesn't work.
# use 'cat /proc/bus/input/devices' and look for the event file.
infile_path = "/dev/input/event4"

# open file in binary mode
in_file = open(infile_path, "rb")

# Read from the file
# long int, long int, unsigned short, unsigned short, unsigned int
FORMAT = "llHHI"
EVENT_SIZE = struct.calcsize(FORMAT)
event = in_file.read(EVENT_SIZE)

v = 0
h = 0

cont = 0

l_state = 0
r_state = 0
while event:
    (tv_sec, tv_usec, ev_type, code, value) = struct.unpack(FORMAT, event)

    if cont > 700:
        v, h = 0, 0

    if ev_type == 3:
        print(code, value)
        if code == 0: 
            h = scale(value, (0, 255), (-800, 800)) # horizontal
        elif code == 1:
            v = scale(value, (0, 255), (800, -800)) # vertical

    # if ev_type == 1:  # A button was pressed or released.
    #     if code == 307 and value == 0:
    #         if l_state == 0:
    #             l_state = 1
    #             print("open")
    #             # left_arm.run_angle(100, 360, Stop.HOLD,False)
    #             wait(100)
    #             # left_arm.stop()
    #         else:
    #             l_state = 0
    #             print("close")
    #             # left_arm.run_angle(-100, 360, Stop.HOLD,False)
    #             wait(100)
    #             # left_arm.stop()

    #     if code == 312 and value == 0:
    #         if r_state == 0:
    #             r_state = 1
    #             # right_arm.run_angle(100, 360, Stop.HOLD,False)
    #             wait(10)
    #         else:
    #             r_state = 0
    #             # right_arm.run_angle(-100, 360, Stop.HOLD,False)
    #             wait(10)

    # elif ev_type == 3:  # Stick was moved
    #     if code == 0:
    #         left = scale(value, (0, 255), (-100, 100))
    #     if code == 1:  # Righ stick vertical
    #         forward = scale(value, (0, 255), (100, -100))
    #     if code == 2:
    #         arm = scale(value, (0, 255), (0, 100))
    #     if code == 5:
    #         arm = scale(value, (0, 255), (0, -100))
    # # Set motor voltages.

    print((v-h), (v+h))

    left_motor.run(v)
    right_motor.run(v)

    # left_arm.run(arm)
    # Finally, read another event
    cont+=1
    event = in_file.read(EVENT_SIZE)

in_file.close()
