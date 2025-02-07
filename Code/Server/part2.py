import move as mov
import servo as serv
import Buzzer
# import camera
import solve_maze
import sys
from gpiozero import DistanceSensor
import numpy as np
import Led
import time
from collections.abc import Iterable

GOOD_THRESHOLD = 5

SERVO_ANGLES = [50, 60, 70, 80, 90, 100, 110, 120, 130]

servo = serv.Servo()
servo.setServoPwm('0', 90)

move = mov.Move()
leds = Led.Led()

trigger_pin = 27
echo_pin    = 22
ultrosinic_sensor = DistanceSensor(echo=echo_pin, trigger=trigger_pin ,max_distance=3)

# if len(sys.argv) != 5:
#     print(f"Usage: python {sys.argv[0]} <start x> <start y> <end x> <end y>")
#     exit(-1)

# goal_x = int(sys.argv[3])
# goal_y = int(sys.argv[4])

# cur_x = int(sys.argv[1])
# cur_y = int(sys.argv[2])
cur_angle = 90

grid = np.zeros((200, 200))

if len(sys.argv) != 2:
    exit(-1)

move_1 = [[move.forward, move.right], [move.forward, move.left], [move.forward, move.left], [move.forward, move.right], [move.forward]]
val_1 = [[None, 90], [2, 90], [None, 90], [2, 90], [None]]

move_2 = [[move.left, move.forward],[ move.back, move.right], [move.forward, move.left], [move.forward, leds.ledIndex, time.sleep, leds.ledMode, move.forward], [move.left, move.forward]]
val_2 = [[120, 1.5],[1, 90], [3, 90], [2, (255, 255, 255, 255), 2, 0, 1.5], [90, 2]]


if sys.argv[1] == '1':
    mv = move_1
    val = val_1
else:
    mv = move_2
    val = val_2

# while not (abs(cur_x - goal_x) < GOOD_THRESHOLD and abs(cur_y - goal_y) < GOOD_THRESHOLD):

for cur_move, cur_vals in zip(mv, val):
    """
    scan the room see what is there, update the map

    check the current video feed for the existence of a stop sign
    if there is a stop sign, figure out how close it is to us, if it is within some threshold
    then we need to do a light show

    with the updated map, run A* and do the first 5-10 steps, which should not be that far

    repeat until we are at the destination
    """

    for angle in SERVO_ANGLES:
        print(angle)
        servo.setServoPwm('0', angle)
        cur_dist = ultrosinic_sensor.distance
        time.sleep(0.2)
    

    servo.setServoPwm('0', 90)  

        # update the map with Emma's code
    print("doing")
    for cm, cv in zip(cur_move, cur_vals):
        if cv is not None:
            if isinstance(cv, Iterable):
                cm(*cv)
            else:
                cm(cv)
        else:
            cm()
    
    # directions = solve_maze.a_star_search()

    # for i in directions[:min(len(directions), 5)]:
    #     # turn to correct angle
    #     # move forward
    #     # repeat
    #     cur_dir = directions[i]

    #     match cur_dir:
    #         case solve_maze.DIR.RIGHT:
    #             needed_angle = 90
    #         case solve_maze.DIR.DOWN_RIGHT:
    #             needed_angle = 135
    #         case solve_maze.DIR.DOWN:
    #             needed_angle = 180
    #         case solve_maze.DIR.DOWN_LEFT:
    #             needed_angle = 225
    #         case solve_maze.DIR.LEFT:
    #             needed_angle = 270
    #         case solve_maze.DIR.UP_LEFT:
    #             needed_angle = 315
    #         case solve_maze.DIR.UP:
    #             needed_angle = 0
    #         case solve_maze.DIR.UP_RIGHT:
    #             needed_angle = 45
    #         case _:
    #             needed_angle = 0

        
    #     # if cur_angle < needed_angle:
    #     #     if needed_angle - cur_angle < cur_angle + 360 - needed_angle:
    #     #         move.left(needed_angle - cur_angle)
    #     #     else:
    #     #         move.right(cur_angle + 360 - needed_angle)
    #     # elif cur_angle > needed_angle:
    #     #     if cur_angle - needed_angle < needed_angle + 360 - cur_angle:
    #     #         move.right(cur_angle - needed_angle)
    #     #     else:
    #     #         move.left(needed_angle + 360 - cur_angle)
        
    #     mod_val = (needed_angle - cur_angle) % 360

    #     if mod_val > 180:
    #         move.left(360 - mod_val)
    #         print(f"turning CCW {360 - mod_val:.2f} degrees")
    #     else:
    #         move.right(mod_val)
    #         print(f"turning CW {mod_val:.2f} degrees")
        
    #     cur_angle = needed_angle

