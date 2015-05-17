from MBlocks.controller import Cube

from itertools import chain, combinations
import random
import thread
import time

do_change = True


def change_color(cube):
    colors = list(chain(combinations('rgb', 1), combinations('rgb', 2)))
    for i in range(60):
        for face in range(1, 7):
            color = ''.join(random.sample(colors, 1)[0])
            cube.ser.write(' '.join(('fbrgbled', color, 't', str(face))) + '\n')

            color = ''.join(random.sample(colors, 1)[0])
            cube.ser.write(' '.join(('fbrgbled', color, 'b', str(face))) + '\n')

        time.sleep(2)
    stop_color(cube)
    cube.disconnect()


def stop_color(cube):
    cube.ser.write('fbrgbled off tb 1 2 3 4 5 6\n')


def ceo_demo_temp(ports):
    cubes = [Cube(port) for port in ports]

    time.sleep(5)
    for i in range(3):
        for j in range(2):
            for cube in cubes:
                cube.ser.write('ia f 6000 1800 20\n')
            time.sleep(5)
        for j in range(2):
            for cube in cubes:
                cube.ser.write('ia r 6000 1900 20\n')
            time.sleep(5)

    for cube in cubes:
        cube.disconnect()


def ceo_demo_colors(ports):
    cubes = [Cube(port) for port in ports]
    for cube in cubes:
        thread.start_new_thread(change_color, (cube,))


def ceo_demo(ports):
    """
    The MAC addresses of the cubes are:
       - 1: E2:8A:4C:9A:6F:9C   (mostly blue screws)
       - 2: D8:9C:00:41:E4:19   (mostly black screws)
    """
    cubes = [Cube(port) for port in ports]
    for cube in cubes:
        thread.start_new_thread(change_color, (cube,))

    for i in range(3):
        for j in range(2):
            for cube in cubes:
                cube.ser.write('ia f 6000 1300 20\n')
            time.sleep(3)
        for j in range(2):
            for cube in cubes:
                cube.ser.write('ia f 6000 1500 20\n')
            time.sleep(3)


def csail_demo(ports):
    cubes = [Cube(port) for port in ports]

    # Red cloudy moves back and forth using horizontal convex moves
    for cube in cubes:
        if cube.mac_address == 'C6:27:2E:44:13:82':
            traverse_cube = cube
            break
    while True:
        for i in xrange(3):
            traverse_cube.do_action('horizontal_traverse', 'forward')
        for i in xrange(3):
            traverse_cube.do_action('horizontal_traverse', 'reverse')

    # Black moves along lattice in cycle
    # TODO

    for cube in cubes:
        cube.disconnect()
