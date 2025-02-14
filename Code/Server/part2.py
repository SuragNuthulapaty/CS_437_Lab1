import move as mov
import servo as serv
import Buzzer
import camera
import solve_maze
import sys
from gpiozero import DistanceSensor
import numpy as np
import Led
import time
import Scan
import threading
import shared


GOOD_THRESHOLD = 5
servo = serv.Servo()
servo.setServoPwm('0', 90)

move = mov.Move()

s = Scan.Scan()

leds = Led.Led()

trigger_pin = 27
echo_pin    = 22
ultrosinic_sensor = DistanceSensor(echo=echo_pin, trigger=trigger_pin ,max_distance=3)

grid = np.zeros((300, 100))

if len(sys.argv) != 6:
    print(f"Usage: python {sys.argv[0]} <start x> <start y> <end x> <end y> <start angle>")

goal_x = int(sys.argv[3])
goal_y = int(sys.argv[4])
cur_x = int(sys.argv[1])
cur_y = int(sys.argv[2])
cur_angle = int(sys.argv[5])

camera_thread = threading.Thread(target=camera.run)

camera_thread.start()

time.sleep(2)

while not (abs(cur_x - goal_x) < GOOD_THRESHOLD and abs(cur_y - goal_y) < GOOD_THRESHOLD):
    
    """
    scan the room see what is there, update the map
    check the current video feed for the existence of a stop sign
    if there is a stop sign, figure out how close it is to us, if it is within some threshold
    then we need to do a light show
    with the updated map, run A* and do the first 5-10 steps, which should not be that far
    repeat until we are at the destination
    """
    map = s.get_map((cur_x, cur_y), cur_angle)
    
    directions, move_back = solve_maze.a_star_search(map, cur_x, cur_y)

    for i in directions[:min(len(directions), 5)]:
        # turn to correct angle
        # move forward
        # repeat

        # handle the stopping for a stop sign, and turn on the lights
        if shared.should_stop.is_set():
            move.stop()
            leds.ledIndex(255, 255, 255, 255)
            time.sleep(2)
            leds.ledMode('0')
            shared.should_stop.clear()

        cur_dir = directions[i]

        match cur_dir:
            case solve_maze.DIR.RIGHT:
                needed_angle = 90
                dx, dy = 1, 0
            case solve_maze.DIR.DOWN_RIGHT:
                needed_angle = 135
                dx, dy = 1, -1
            case solve_maze.DIR.DOWN:
                needed_angle = 180
                dx, dy = 0, -1
            case solve_maze.DIR.DOWN_LEFT:
                needed_angle = 225
                dx, dy = -1, -1
            case solve_maze.DIR.LEFT:
                needed_angle = 270
                dx, dy = -1, 0
            case solve_maze.DIR.UP_LEFT:
                needed_angle = 315
                dx, dy = -1, 1
            case solve_maze.DIR.UP:
                needed_angle = 0
                dx, dy = 0, 1
            case solve_maze.DIR.UP_RIGHT:
                needed_angle = 45
                dx, dy = 1, 1
            case _:
                needed_angle = 0
        
        if move_back:
            move.back()
            move_back = False

        mod_val = (needed_angle - cur_angle) % 360

        if needed_angle != cur_angle:
            if mod_val > 180:
                move.left(360 - mod_val)
            else:
                move.right(mod_val)
        
        if cur_dir in [solve_maze.DIR.UP, solve_maze.DIR.DOWN, solve_maze.DIR.RIGHT, solve_maze.DIR.LEFT]:
            move.forward()
        else:
            move.forward(1.41)
        

        cur_angle = needed_angle
        cur_x += dx
        cur_y += dy
