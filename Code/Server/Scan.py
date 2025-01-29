from Ultrasonic import *
from servo import *
import numpy as np
import math
import matplotlib.pyplot as plt

class Scan:
    def __init__(self, max_dist=200, start=(0, 0), dest=(99,99), angle=0, angle_incr=5, map_size=(100,100)):
        """
        max_dist: maximum distance threshold (eg viewable distance)
        start: starting position on (100, 100) map
        dest: desired end destination on (100, 100) map
        angle: starting angle of car with *zeroed channel 0 servo* relative to map
            0 is towards [0, y]
            90 is towards [x, 99]
            180 is towards [99, y]
            270 is towards [x, 0]
        angle_incr: angle increments at which to scan
        map_size: size of array representing map
        """

        self.ultrasonic = Ultrasonic() # sensor
        self.pwm_S=Servo() # sensor arm

        self.angle = angle
        self.max_dist = max_dist
        self.start = start
        self.dest = dest
        self.angle_incr = angle_incr

        self.map = np.zeros(map_size) # map of obstacles, where 0 represents an emtpy space
        self.x = start[0] # current position is self.map[self.x, self.y], facing self.angle
        self.y = start[1]

        self.pwm_S.setServoPwm("1", 80) # reset servo

    def read(self, angle=90):
        """
        return the distance in cm, or -1 if car cannot read angle

        angle: angle of reading relative to map
        """
        sensor_angle = angle - self.angle
        if 30 <= sensor_angle <= 150: # restrict angle to +- 60 deg
            # take distance reading
            self.pwm_S.setServoPwm("0", sensor_angle)
            time.sleep(0.2)
            return self.ultrasonic.get_distance()

        # angle is out of bounds
        return -1

    def update_map(self):
        """
        perform a 180 degree scan at the current position, and update the map accordingly

        todo add clearance for A*, optionally reset values to 0 on update
        """
        prev = None # distance reading at previous angle
        for angle in range(0, 360, self.angle_incr):
            dist = self.read(angle)
            if 0 < dist < self.max_dist:
                # calculate distance
                x = self.x + round(dist * math.sin(math.radians(angle)))
                y = self.y + round(dist * math.cos(math.radians(angle)))

                # add to map
                if 0 <= x <= self.map.shape[0] and 0 <= y <= self.map.shape[1]:
                    self.map[x][y] = 1

                    print(f"({x}, {y}) <- d={dist}, a={angle}") # debug

                    if prev != None:
                        # interpolate with previous reading
                        i, j = prev
                        curr = x, y # temporarily store x, y
                        i, x, y, j = min(x, i), max(x, i), min(y, j), max(y, j) # set i < x, j < y

                        if (x == i):
                            # special case to handle dividing by 0
                            while j < y:
                                self.map[x][i] = 1
                                j += 1
                        else:
                            m = (y - j) / min(x - i)

                            print(f"  interpolating {prev} - {(x, y)}") # debug

                            while i < x:
                                print(f"    {i, j}")
                                self.map[round(i)][round(j)] = 1
                                i += 1
                                j += m

                        x, y = curr

                    prev = (x, y)
            else:
                prev = None

    def save_map(self, filename="./map.png"):
        """
        save the map to a PNG

        filename: save path
        """
        self.map[self.x][self.y] = 0.5 # car location
        plt.imshow(self.map, cmap='gray', interpolation='nearest')
        plt.axis('off')  # Hide axes
        plt.savefig(filename, bbox_inches='tight', pad_inches=0)
        plt.close()
        self.map[self.x][self.y] = 0 # reset car indicator
