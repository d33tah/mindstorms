#!/usr/bin/env python3

import sys
import rpyc
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

conn = rpyc.classic.connect(sys.argv[1])
ev3 = conn.modules['ev3dev.ev3']
motor_turn = ev3.LargeMotor('outA')
motor_forward = ev3.MediumMotor('outD')


class SimpleEcho(WebSocket):

    def handleMessage(self):
        # echo message back to client

        current_axes = {
            "UP": self.data in ('38', '119'),
            "DOWN": self.data in ('40', '115'),
            "LEFT": self.data in ('37', '97'),
            "RIGHT": self.data in ('39', '100'),
        }

        if current_axes["UP"]:
            motor_forward.run_timed(time_sp=100, speed_sp=600)
        elif current_axes["DOWN"]:
            motor_forward.run_timed(time_sp=100, speed_sp=-600)

        if current_axes["RIGHT"]:
            motor_turn.run_timed(time_sp=100, speed_sp=60)
        elif current_axes["LEFT"]:
            motor_turn.run_timed(time_sp=100, speed_sp=-60)

        self.sendMessage(self.data)

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')


if __name__ == '__main__':
    SimpleWebSocketServer('', 8001, SimpleEcho).serveforever()
