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
FORMAT = "llHHI"
EVENT_SIZE = struct.calcsize(FORMAT)

# open file in binary mode
in_file = open(infile_path, "rb")

event = in_file.read(EVENT_SIZE)



multiplier = 3

arm_closed = False

commands = {
    3: [0, 0, 0, 0, 0, 0],
    1: {
        304: 6,
        305: 3,
        308: 1,
        312: 0,
        313: 0,
        315: 'break',
    },
}
while event:
    (tv_sec, tv_usec, type, code, value) = struct.unpack(FORMAT, event)

    if type != 0 or code != 0 or value != 0:
        if type == 1:
            if code == 315:
                break
            else:
                multiplier = commands[type][code]
        elif type == 3:
            commands[type][code] = scale(value, [0, 255], [100, -100])

            # print(commands[type])

            x = commands[type][0]
            y = commands[type][1]

            if code == 2 or code == 5:
                left_arm.run((commands[type][2] - commands[type][5])*5)


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
            
            left_motor.run(leftSpeed)
            right_motor.run(rightSpeed)

        


    event = in_file.read(EVENT_SIZE)

in_file.close()
