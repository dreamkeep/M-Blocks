from MBlocks.controller import Cube

import time


def connect(ports):
    cubes = []
    for port in ports:
        cubes.append(Cube(port))

    return cubes


def accel(cubes, dirs, rpms):
    for cube, d, rpm in zip(cubes, dirs, rpms):
        cube.ser.write('bldcspeed {0} {1}\n'.format(d, rpm))

    time.sleep(3)


def brake(cubes, dirs, amps, ts, delay):
    for cube, d, amp, t in zip(cubes, dirs, amps, ts):
        cube.ser.write('brake {0} {1} {2}\n'.format(d, amp, t))
        time.sleep(delay)

    time.sleep(3)


def disconnect(cubes):
    for cube in cubes:
        cube.disconnect()
