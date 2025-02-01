import move as mov
import servo as serv
import Buzzer
import camera
import solve_maze
import sys
from gpiozero import DistanceSensor

GOOD_THRESHOLD = 5

SERVO_ANGLES = [50, 60, 70, 80, 90, 100, 110, 120, 130]

servo = serv.Servo()
servo.setServoPwm('0', 90)

move = mov.Move()

trigger_pin = 27
echo_pin    = 22
ultrosinic_sensor = DistanceSensor(echo=echo_pin, trigger=trigger_pin ,max_distance=3)

if len(sys.argv) != 5:
    print(f"Usage: python {sys.argv[0]} <start x> <start y> <end x> <end y>")

goal_x = int(sys.argv[3])
goal_y = int(sys.argv[4])

cur_x = int(sys.argv[1])
cur_y = int(sys.argv[2])
cur_angle = 90

while not (abs(cur_x - goal_x) < GOOD_THRESHOLD and abs(cur_y - goal_y) < GOOD_THRESHOLD):
    
    """
    scan the room see what is there, update the map

    check the current video feed for the existence of a stop sign
    if there is a stop sign, figure out how close it is to us, if it is within some threshold
    then we need to do a light show

    with the updated map, run A* and do the first 5-10 steps, which should not be that far

    repeat until we are at the destination
    """

    for angle in SERVO_ANGLES:
        servo.setServoPwm('0', angle)
        cur_dist = ultrosinic_sensor.distance

        # update the map with Emma's code


    
    pass
