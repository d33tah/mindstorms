#!/usr/bin/env python

import flask

app = flask.Flask(__name__)

@app.route('/')
def index():
    return """<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Live Streaming</title>
</head>
<body>
<style>
html,body{
    margin:0;
    height:100%;
}
img{
  display:block;
  width:100%; height:100%;
  object-fit: cover;
}
</style>
<script>
var connection = new WebSocket('ws://85.89.184.221:8001');

document.addEventListener("keypress",
//$(document).keypress(
    function(e){ // pressing key
        connection.send(e.keyCode || e.which );
    }
);

</script>
<img src="http://85.89.184.221:8080/video" autoplay="autoplay"></img>
</body>
</html>"""

if __name__ == '__main__':
    app.run('0.0.0.0', port=8080)
