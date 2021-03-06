import numpy as np
import time
import operator


class TwoCubeController(object):
    def __init__(self, fst, scd, ratio=0.8):
        self.ratio = ratio
        
        fst_d = tuple(fst.find_plane())
        if fst_d != (0, 0, 1) and fst_d != (0, 0, -1):
            self.driver = fst
            self.steer = scd
        else:
            self.driver = scd
            self.steer = fst

        # ensure steer is oriented correctly
        self.steer.change_plane((0, 0, 1))
        
        center_d = tuple(self.driver.find_plane())
        if center_d == (0, 0, 1) or center_d == (0, 0, -1):
            # both cubes are oriented with MB parallel to ground
            self.driver.change_plane((1, -1, 0))

        # # use light sensor values to check if driver's forward/backward direction is towards steer
        # self.driver.find_config()
        # center_d = tuple(self.driver.find_plane())
        
        # fc, rc = self.driver.config['forward'], self.driver.config['reverse']
        # if self.driver.is_connected(fc) or self.driver.is_connected(rc):
        #     if center_d == (1, 1, 0) or center_d == (-1, -1, 0):
        #         self.driver.change_plane((1, -1, 0))
        #     else:
        #         self.driver.change_plane((1, 1, 0))

        # self.config_driver = self.driver.config
        # self.config_steer = self.steer.config

    def drive(self):
        """Drive the cube towards the light source.

        Sorts the faces based on their light readings. While the strongest source is not 
        from the front or reverse faces on the driving cube, attempt to steer.

        Steering is done by spinning up the motor to 8000 RPM and then braking. This should
        effectively slide the cube along the ground.
        """ 
        direction = None
        while direction != 'forward' and direction != 'reverse':
            sensor_steer = self.steer.read_light_sensors()
            sensor_driver = self.driver.read_light_sensors()

            lvalues_steer = [(f, v) for (f, v) in sensor_steer.items() if f != 'top' and f != 'bottom']
            lvalues_driver = [(f, v) for (f, v) in sensor_driver.items() if f != 'top' and f != 'bottom']

            sorted_steer = sorted(lvalues_steer, key=operator.itemgetter(1), reverse=True)
            sorted_driver = sorted(lvalues_driver, key=operator.itemgetter(1), reverse=True)

            flip = {'forward': 'reverse', 'reverse': 'forward', 'left': 'right', 'right': 'left'}
            face_steer = flip[sorted_steer[-1][0]]
            val_steer = sensor_steer[face_steer]
            val_driver = max(sensor_driver['left'], sensor_driver['right'])
            print face_steer, val_steer
            print val_driver

            if val_steer == sorted_steer[0][1] or val_driver == sorted_driver[0][1]:
                self.steer_cubes()
            elif sensor_driver['forward'] > sensor_driver['reverse']:
                direction = 'forward'
            else:
                direction = 'reverse'

        self.driver.do_action('two_cube_traverse', direction)
        self.driver.do_action('two_cube_traverse', direction)
        time.sleep(2.0)
        
        # We are OK if either both actions completed, or if neither did
        center = self.steer.find_plane()
        while center == []:
            center = self.steer.find_plane()
        center = tuple(center)
        
        while center != (0, 0, 1) and center != (0, 0, -1):
            # only one move successfully completed
            self.driver.do_action('two_cube_traverse', '{}'.format(direction))

            center = self.steer.find_plane()
            while center == []:
                center = self.steer.find_plane()
            center = tuple(center)
        

    def steer_cubes(self, sleep=4):
        # find whether direction is clockwise or counterclockwise to center ring
        light_values = [self.steer.read_light_sensor(face) for face in self.steer.config['ring']]
        min_val = min(light_values)
        id = light_values.index(min_val)
        
        if light_values[id - 1] > light_values[(id + 1) % 4]:  # counterclockwise motion
            self.steer.ser.write('bldcspeed r 6000\n')
        else:                                                  # clockwise motion
            self.steer.ser.write('bldcspeed f 6000\n')
        time.sleep(sleep)
        self.steer.ser.write('bldcstop b\n')
