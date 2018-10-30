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
    while not ws.closed:
        data = ws.receive()
        current_axes = {
            "UP": data in ('38', '119'),
            "DOWN": data in ('40', '115'),
            "LEFT": data in ('37', '97'),
            "RIGHT": data in ('39', '100'),
        }

        if current_axes["UP"]:
            motor_forward.run_timed(time_sp=100, speed_sp=600)
        elif current_axes["DOWN"]:
            motor_forward.run_timed(time_sp=100, speed_sp=-600)

        if current_axes["RIGHT"]:
            motor_turn.run_timed(time_sp=100, speed_sp=60)
        elif current_axes["LEFT"]:
            motor_turn.run_timed(time_sp=100, speed_sp=-60)
    print('closed')


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 8001), app, handler_class=WebSocketHandler)
    server.serve_forever()
