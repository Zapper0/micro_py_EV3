#!/usr/bin/env pybricks-micropython

import struct, math

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
from pybricks.tools import wait, StopWatch


ev3 = EV3Brick()

# Controller codes
# Buttons type 1
# X = 304
# Circle = 305
# Triangle = 307
# Square = 308

# Declare motors
left_motor = Motor(Port.A)
right_motor = Motor(Port.D)
left_arm = Motor(Port.B)

def scale(val, src, dst):
    value = int((float(val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0])
    return value


infile_path = "/dev/input/event4"

"""
FORMAT represents the format used by linux kernel input event struct
See https://github.com/torvalds/linux/blob/v5.5-rc5/include/uapi/linux/input.h#L28
Stands for: long int, long int, unsigned short, unsigned short, unsigned int
"""
FORMAT = "llHHI"
EVENT_SIZE = struct.calcsize(FORMAT)

# open file in binary mode
in_file = open(infile_path, "rb")

event = in_file.read(EVENT_SIZE)


lstick = [0, 0]
rstick = [0, 0]

multiplier = 3

arm_closed = False

while event:
    (tv_sec, tv_usec, type, code, value) = struct.unpack(FORMAT, event)

    if type != 0 or code != 0 or value != 0:
        
        if type == 3:
            if code == 0:
                lstick[0] = value
            elif code == 1:
                lstick[1] = value
            elif code == 3:
                rstick[0] = value
            elif code == 4:
                rstick[1] = value

            x = scale(lstick[0], [0, 255], [-100, 100])
            y = scale(lstick[1], [0, 255], [100, -100])

            lowerSpeed = (y - abs(x))*multiplier

            if x > 0:
                leftSpeed = y *multiplier
                rightSpeed = lowerSpeed
            elif x < 0:
                leftSpeed = lowerSpeed
                rightSpeed = y *multiplier
            else:
                leftSpeed = y *multiplier
                rightSpeed = y *multiplier

            if y < 0:
                leftSpeed = rightSpeed
                rightSpeed = leftSpeed

            # print("Left: " + str(leftSpeed) + " Right: " + str(rightSpeed) + ' (' + str(x) + ', ' + str(y) + ')' )

            # move motors
            left_motor.run(leftSpeed)
            right_motor.run(rightSpeed)
            
            if code == 2:
                left_arm.run(value*2)

            elif code == 5:
                left_arm.run(-value*2)

        elif type == 1:
            if code == 315:
                break
            elif code == 304:
                multiplier = 6
                # print("Turbo mode activated")
            elif code == 305:
                multiplier = 3
                # print("Turbo mode deactivated")
            elif code == 308:
                multiplier = 1
                # print("Precision mode deactivated")
            # print("Event type %u, code %u, value %u at %d.%d" % (type, code, value, tv_sec, tv_usec))
        
    event = in_file.read(EVENT_SIZE)

in_file.close()
