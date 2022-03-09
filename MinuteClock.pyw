# clock imports
from time import strftime
import math

# pygame imports
import sys
import pygame
from pygame.locals import *

# transparency imports
import os
import win32api
import win32con
import win32gui

"""MinuteClock.pyw
application that makes a clock with only a minute hand
for windows

* TODO
  + hour hand is broken [will fix once i feel like doing more math]
  + move configs to a config file (that means most or all of the constants)
  + implement transparency to make this a widget [working on it]
    + https://youtu.be/q0Hq5YgwSGU
    + also: https://www.reddit.com/r/pygame/comments/pgo6l8/transparent_window_using_pygame/
    + pygame.display.set_mode((640, 480), pygame.NOFRAME)
    + https://www.howtogeek.com/208224/how-to-add-programs-files-and-folders-to-system-startup-in-windows-8.1/#:~:text=Press%20Windows%2BR%20to%20open,the%20next%20time%20you%20boot.
"""

SCREEN_LENGTH = 250
CENTER_TO_EDGE = SCREEN_LENGTH / 2  # distance of center from top left edge
DEFAULT_HAND_LENGTH = 100


def setupTransparency():
    """idk how this works tbh but it makes the screen transparent"""
    hwnd = pygame.display.get_wm_info()["window"]
    win32gui.SetWindowLong(
        hwnd,
        win32con.GWL_EXSTYLE,
        win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED,
    )
    win32gui.SetLayeredWindowAttributes(
        hwnd, win32api.RGB(255, 0, 128), 0, win32con.LWA_COLORKEY
    )


def getMinAngle():
    """:returns: angle of clock minute hand in radians"""
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


def getHrAngle():
    """:returns: angle of clock hour hand in radians"""
    # TODO i think this is broekn
    # get current time in (float) minutes
    ans = int(strftime("%H"))

    if ans > 12:
        ans -= 12
    ans += int(strftime("%M")) / 60  # optional - uncomment for more precision.

    # radians moves counterclockwise but clock moves clockwise; fix that
    ans = 12 - ans

    # convert to radians
    # current range of time = [0,60), want [0,2pi)
    ans *= math.pi / 30

    # 0 rad faces right. 0 min faces up. fix that.
    ans += math.pi / 2

    return ans


def getdX(theta, handLength=DEFAULT_HAND_LENGTH):
    """Gets the change in x value for a hand from its center point

    :param theta: uses radians
    :param handLength: is length of the hand
    :returns: change in x value for a clock hand in pixels
    """
    return handLength * math.cos(theta)


def getdY(theta, handLength=DEFAULT_HAND_LENGTH):
    """Gets the change in y value for a hand from its center point

    :param theta: uses radians
    :param handLength: is length of the hand
    :returns: change in y value for a clock hand in pixels
    """
    return -1 * handLength * math.sin(theta)


def getStart(center=None):
    """Gets the start coordinates of a hand

    :param center: coordinates of center of hand
    :returns: coordinates of the start of a hand
    """
    if center is None:
        center = CENTER_TO_EDGE
    return center, center


def getEnd(theta, handLength=DEFAULT_HAND_LENGTH, center=None):
    """Gets the end coordinates of a hand

    :param center: coordinates of center of hand
    :param theta: uses radians and is set to getAngle() by default
    :param handLength: length of hand
    :returns: coordinates of the end of a hand
    """
    if center is None:
        center = CENTER_TO_EDGE
    return center + getdX(theta, handLength), center + getdY(theta, handLength)


def drawHand(theta, handLength, center=None):
    """draws a hand"""
    pygame.draw.line(screen, (255, 255, 255), getStart(center), getEnd(theta, handLength, center), 5)


if __name__ == "__main__":
    pygame.init()

    fps = 20  # how often do we need to check red X exit button
    fpsClock = pygame.time.Clock()

    width, height = SCREEN_LENGTH, SCREEN_LENGTH
    screen = pygame.display.set_mode((width, height))  # , pygame.NOFRAME)
    pygame.display.set_caption("")

    setupTransparency()

    # Game loop.
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((255, 0, 128))
        drawHand(getMinAngle(), DEFAULT_HAND_LENGTH)
        # drawHand(getHrAngle(), DEFAULT_HAND_LENGTH-20)

        pygame.display.update()
        fpsClock.tick(fps)
