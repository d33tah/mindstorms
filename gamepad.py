#!/usr/bin/env python

import pygame
import rpyc
import sys
conn = rpyc.classic.connect(sys.argv[1])
ev3 = conn.modules['ev3dev.ev3']
motor_turn = ev3.LargeMotor('outA')
motor_forward = ev3.MediumMotor('outD')

pygame.init()

clock = pygame.time.Clock()

pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

def get_axes():
    return {n: joystick.get_axis(n) for n in range(joystick.get_numaxes())}

def axes_to_directions(d):
    return {
        "LEFT": d[0] < 0,
        "RIGHT": d[0] > 0,
        "UP": d[1] < 0,
        "DOWN": d[1] > 0,
    }

#old_axes = axes_to_directions(get_axes())

keep_going = True
while keep_going:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keep_going = False

    current_axes = axes_to_directions(get_axes())
    if current_axes["UP"]:
        motor_forward.run_timed(time_sp=100, speed_sp=600)
    elif current_axes["DOWN"]:
        motor_forward.run_timed(time_sp=100, speed_sp=-600)

    if current_axes["RIGHT"]:
        motor_turn.run_timed(time_sp=100, speed_sp=60)
    elif current_axes["LEFT"]:
        motor_turn.run_timed(time_sp=100, speed_sp=-60)

    #old_axes = current_axes

    clock.tick(20)

pygame.quit()
