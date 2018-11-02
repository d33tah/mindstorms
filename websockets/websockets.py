#!/usr/bin/env python3

import sys
import rpyc
from flask import Flask
from flask_sockets import Sockets


conn = rpyc.classic.connect(sys.argv[1])
ev3 = conn.modules['ev3dev.ev3']
motor_turn = ev3.LargeMotor('outA')
motor_forward = ev3.MediumMotor('outD')

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

        speed = 0 if direction == 'up' else 600

        if current_axes["UP"]:
            motor_forward.run_forever(speed_sp=speed)
        elif current_axes["DOWN"]:
            motor_forward.run_forever(speed_sp=-speed)

        if current_axes["RIGHT"]:
            motor_turn.run_forever(speed_sp=speed / 10)
        elif current_axes["LEFT"]:
            motor_turn.run_forever(speed_sp=-speed / 10)
    print('closed')


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 8001), app, handler_class=WebSocketHandler)
    server.serve_forever()
