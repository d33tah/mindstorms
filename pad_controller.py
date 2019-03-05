#!/usr/bin/env python

import logging

import pygame
import rpyc


_logging_format = \
    '[%(levelname)s][%(asctime)s][%(pathname)s:%(lineno)d]: %(message)s'
logging.basicConfig(format=_logging_format)
_logger = logging.getLogger()
_logger.setLevel(logging.DEBUG)
_file_handler = logging.FileHandler('/tmp/pad_controller.log')
_file_handler.setFormatter(logging.Formatter(_logging_format))
_logger.addHandler(_file_handler)

conn = rpyc.classic.connect('10.42.0.3')
ev3 = conn.modules['ev3dev.ev3']
motor_turn = ev3.MediumMotor('outA')
motor_forward = ev3.LargeMotor('outD')


def main():
    try:
        _logger.info('Starting pad controller.')
        pygame.init()
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        speed = 250
        while True:
            for event in pygame.event.get():
                if event.type == 10:
                    if event.button == 1:
                        motor_forward.run_forever(speed_sp=-speed * 4)
                    elif event.button == 7:
                        motor_forward.run_forever(speed_sp=-speed)
                    elif event.button == 6:
                        motor_forward.run_forever(speed_sp=speed)
                elif event.type == 11:
                    if event.button in [1, 6, 7]:
                        motor_forward.run_forever(speed_sp=0)
                elif 'axis' in event.__dict__ and event.axis == 0:
                    motor_turn.run_to_abs_pos(
                        speed_sp=200, position_sp=-30 * event.value
                    )
                _logger.info(str(event))
    except Exception:
        _logger.exception('Exception occurred in main function.')


if __name__ == '__main__':
    main()
