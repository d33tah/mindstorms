#!/usr/bin/env python3

import sys
import rpyc
import os

from flask import Flask
from flask_sockets import Sockets


EV3DEV_RPC_HOST = os.environ['EV3DEV_RPC_HOST']
conn = rpyc.classic.connect(EV3DEV_RPC_HOST)
ev3 = conn.modules['ev3dev.ev3']
motor_turn = ev3.MediumMotor('outD')
motor_forward = ev3.LargeMotor('outA')

app = Flask(__name__)
sockets = Sockets(app)


@sockets.route('/')
def echo_socket(ws):
    print('connected')
    last_msg = ''
    while not ws.closed:
        data = ws.receive()
        if data == last_msg:
            continue
        else:
            last_msg = data
        print(data)
        direction, key = data.split()
        current_axes = {
            "UP": key in ('38', '119'),
            "DOWN": key in ('40', '115'),
            "LEFT": key in ('37', '97'),
            "RIGHT": key in ('39', '100'),
        }

        if current_axes["RIGHT"] and direction == 'up':
            motor_turn.run_to_abs_pos(speed_sp=200, position_sp=-20)
        elif current_axes["RIGHT"]:
            motor_turn.run_to_abs_pos(speed_sp=200, position_sp=20)
        elif current_axes["LEFT"] and direction == 'up':
            motor_turn.run_to_abs_pos(speed_sp=200, position_sp=-20)
        elif current_axes["LEFT"]:
            motor_turn.run_to_abs_pos(speed_sp=200, position_sp=-60)

        speed = 0 if direction == 'up' else -600

        if current_axes["UP"]:
            motor_forward.run_forever(speed_sp=speed)
        elif current_axes["DOWN"]:
            motor_forward.run_forever(speed_sp=-speed)

    print('closed')


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 8001), app, handler_class=WebSocketHandler)
    server.serve_forever()
