from Ultrasonic import *
from servo import *
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.ndimage import binary_dilation, convolve

"""
cd CS_437_Lab1/Code/Server
git pull
python -i Scan.py
"""

class Scan:
    def __init__(self,
                 max_dist=50,
                 start=(0, 50),
                 dest=(99,99),
                 angle=0,
                 angle_incr=5,
                 map_size=(100,100),
                 padding=(11, 11),
                 filter=(5, 5),
         ):
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
        clearance_size: shape of padding added to map to represent car clearance
        filter_size: shape of denoising filter
        """

        self.ultrasonic = Ultrasonic() # sensor
        self.pwm_S=Servo() # sensor arm

        self.angle = angle
        self.max_dist = max_dist
        self.start = start
        self.dest = dest
        self.angle_incr = angle_incr

        self.padding = np.ones(padding) # shape of added clearance
        self.filter = np.ones(filter) # shape of de-noising convolution kernel

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
        if 50 <= sensor_angle <= 130: # restrict angle to +- 60 deg
            # take distance reading
            self.pwm_S.setServoPwm("0", sensor_angle)
            time.sleep(0.2)
            return self.ultrasonic.get_distance()

        # angle is out of bounds
        return -1

    def run(self):
        self.reset_map()
        self.update_map()
        self.save_map()
        self.denoise_map()
        self.save_map("denoised_map.png")
        self.map = self.padded_map()
        self.save_map("padded_map.png")

    def reset_map(self):
        self.map = np.zeros_like(self.map)

    def update_map(self):
        """
        perform a 180 degree scan at the current position, and update the map accordingly
        """
        x0, y0 = -1, -1 # coordinates at previous angle
        for angle in range(0, 360, self.angle_incr):
            dist = self.read(angle)
            if 0 < dist < self.max_dist:
                # calculate distance
                x = self.x + round(dist * math.sin(math.radians(angle)))
                y = self.y + round(dist * math.cos(math.radians(angle)))

                # add to map
                if 0 <= x < self.map.shape[0] and 0 <= y < self.map.shape[1]:
                    self.map[x][y] = 1

                    print(f"({x}, {y}) <- d={dist}, a={angle}") # debug

                    if 0 <= x0 and 0 <= y0 and ((x - x0) ** 2 + (y - y0) ** 2) < 100:
                        # interpolate with previous reading; uses Bresenham's line algo
                        dx = abs(x - x0)
                        sx = 1 if x0 < x else -1
                        dy = -abs(y - y0)
                        sy = 1 if y0 < y else -1
                        err = dx + dy

                        while True:
                            self.map[x0][y0] = 1
                            e2 = 2 * err
                            if e2 > dy:
                                if x0 == x:
                                    break
                                err += dy
                                x0 += sx
                            if e2 < dx:
                                if y0 == y:
                                    break
                                err += dx
                                y0 += sy

                    x0, y0 = x, y
            else:
                x0, y0 = -1, -1

    def denoise_map(self):
        num_neighbors = convolve(self.map, self.filter, mode='constant', cval=0)
        self.map = np.where(num_neighbors > 1, self.map, 0)

    def padded_map(self):
        """
        returns the map with added clearance
        """
        return binary_dilation(self.map, structure=self.padding).astype(self.map.dtype)

    def save_map(self, filename="./map.png"):
        """
        save the map to a PNG

        filename: save path
        """
        self.map[self.x][self.y] = 0.5 # car location
        plt.imshow(np.rot90(self.map, 2), cmap='gray', interpolation='nearest')
        plt.axis('off')  # Hide axes
        plt.savefig(filename, bbox_inches='tight', pad_inches=0)
        plt.close()
        self.map[self.x][self.y] = 0 # reset car indicator

s = Scan()
s.run()
