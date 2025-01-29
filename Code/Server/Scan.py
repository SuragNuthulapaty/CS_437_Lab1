from Ultrasonic import *
from servo import *
import numpy as np
import math

class Scan:
    def __init__(self, max_dist=50000, start=(0, 0), dest=(99,99), angle=0, angle_incr=5):
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
        """

        self.ultrasonic = Ultrasonic() # sensor
        self.pwm_S=Servo() # sensor arm

        self.angle = angle
        self.max_dist = max_dist
        self.start = start
        self.dest = dest
        self.angle_incr = angle_incr

        self.map = np.zeros((100, 100)) # map of obstacles, where 0 represents an emtpy space
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

        todo interpolate readings, add clearance
        """
        for angle in range(0, 360, self.angle_incr):
            dist = self.read(angle)
            if 0 < dist < self.max_dist:
                # add obstacle to map
                x = max(0, min(99, self.x + round(dist * math.sin(math.radians(angle)))))
                y = max(0, min(99, self.y + round(dist * math.cos(math.radians(angle)))))

                print(f"({x}, {y}) <- d={dist}, a = {angle}")

                self.map[x][y] = 1
