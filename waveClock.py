import sys

from time import strftime

import math

import pygame
from pygame.locals import *

'''waveClock.py
same thing as main but now with sine wave bullshit
'''

SCREEN_LENGTH = 250
CENTER_TO_EDGE = SCREEN_LENGTH / 2  # distance of center from top left edge
DEFAULT_HAND_LENGTH = 100
SIN_WAVE_VAL = 0 # rads


def getAngle():
    """returns angle of clock minute hand in radians"""
    # get current time in (float) minutes
    ans = int(strftime("%M"))
    # ans += int(strftime("%S")) / 60 # optional - uncomment for more precision. tbh this just distracts me more

    # radians moves counterclockwise but clock moves clockwise; fix that
    ans = 60 - ans

    # convert to radians
    # current range of time = [0,60), want [0,2pi)
    ans *= math.pi / 30

    # 0 rad faces right. 0 min faces up. fix that.
    ans += math.pi / 2

    return ans


def getdX(theta=None, handLength=DEFAULT_HAND_LENGTH):
    """returns change in x value for a clock hand in pixels
    param theta uses radians and is set to getAngle() by default
    param handLength is length of the hand
    """
    if theta is None:
        theta = getAngle()
    return handLength * math.cos(theta)


def getdY(theta=None, handLength=DEFAULT_HAND_LENGTH):
    """returns change in y value for a clock hand in pixels
    param theta uses radians and is set to getAngle() by default
    param handLength is length of the hand
    """
    if theta is None:
        theta = getAngle()
    return -1 * handLength * math.sin(theta)


def getStart():
    """returns position of the start of the hand as a tuple"""
    return (CENTER_TO_EDGE, CENTER_TO_EDGE)


def getEnd():
    """returns position of the end of the hand as a tuple"""
    return (CENTER_TO_EDGE + getdX(None, (math.sin(SIN_WAVE_VAL) + 1) * 50), CENTER_TO_EDGE + getdY(None, (math.sin(SIN_WAVE_VAL) + 1) * 50))


if __name__ == "__main__":
    pygame.init()

    fps = 20 # how often do we need to check red X exit button
    fpsClock = pygame.time.Clock()

    width, height = SCREEN_LENGTH, SCREEN_LENGTH
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("")
    
    # Game loop.
    while True:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.draw.line(screen, (255, 255, 255), getStart(), getEnd(), 5)

        pygame.display.flip()
        fpsClock.tick(fps)
        
        SIN_WAVE_VAL += 0.1
        print((math.sin(SIN_WAVE_VAL) + 1) / 2)

