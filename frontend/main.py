#!/usr/bin/env python

import flask
import os

WEBSOCKET_URL = os.environ['WEBSOCKET_URL']

app = flask.Flask(__name__)


@app.route('/')
def index():
    args = {'WEBSOCKET_URL': WEBSOCKET_URL}
    return """<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Live Streaming</title>
</head>
<body>
<script>
var connection = new WebSocket('%(WEBSOCKET_URL)s');

document.addEventListener("keyup",
    function(e){ // pressing key
        connection.send("up " + e.keyCode || e.which );
    }
);

document.addEventListener("keydown",
    function(e){ // pressing key
        connection.send("down " + e.keyCode || e.which );
    }
);

</script>
</body>
</html>""" % args


if __name__ == '__main__':
    app.run('0.0.0.0', port=8080)
