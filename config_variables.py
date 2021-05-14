import sys
import pygame as py

py.font.init()

#************************* General Constants ***************************************
FPS = 240
WIN_WIDTH = 1600
WIN_HEIGHT = 900
STARTING_POS = (WIN_WIDTH/2, WIN_HEIGHT-100)
SCORE_VEL_MULTIPLE = 0.00                               # Bonus scoring for faster
BAD_GENONE_TRESHOLD = 200                               # Car will be remove if it is too far off the screen
INPUT_NEURONS = 9                                       # Neuron Input node to help for input learning (Car Track Distance from center of the track(8 Node Sensor around the car), Speed)
OUTPUT_NEURONS = 4                                      # Neuron Output for controlling the Car (Acceleration, Brake, Left, Right)

#************************* Car Specs ***************************************
CAR_DBG = False
FRICTION = -0.1                                         # Car Friction, The higher the slower
MAX_VAL = 10                                            # Max Velocity of the Car
MAX_VEL_REDUCTION = 1                                   # Reduce Maximum Velocity during start
ACC_STRENGTH = 0.2                                      # Acceleration Strength
BRAKE_STREGTH = 1                                       # Brake Strength
TURN_VEL = 2                                            # How fast it turn
SENSOR_DISTANCE = 200                                   # How far is the sensor sens
ACTIVATION_TRESHOLD = 0.5                               # When will the sensor triggered

#************************* Road Specs ***************************************

ROAD_DBG = False
MAX_ANGLE = 1
MAX_DEVIATION = 300
SPACING = 200
NUM_POINTS  = 15                #number of points for each segment
SAFE_SPACE = SPACING + 50       #buffer space above the screen
ROAD_WIDTH = 200
