#!/usr/bin/env python

import io
import socket
from PIL import Image
from PIL import ImageDraw

HTTP_HEADER = b'''HTTP/1.1 200 OK
Connection: close
Server: IP Webcam Server 0.4
Cache-Control: no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0
Pragma: no-cache
Expires: -1
Access-Control-Allow-Origin: *
Content-Type: multipart/x-mixed-replace;boundary=Ba4oTvQMY8ew04N8dcnM

'''


def read_image_size(f):
    while True:
        line = f.readline()
        if line == b'\r\n':
            break
        to_find = b"Content-Length: "
        idx = line.find(to_find)
        if idx != -1:
            content_length = int(line[len(to_find):-2])
    return content_length


def yield_images(f):
    while True:
        # skip boundary:
        f.read(2)
        f.readline()

        content_length = read_image_size(f)
        yield f.read(content_length)


def append_text(img_b, text):
    bio_r = io.BytesIO(img_b)
    img = Image.open(bio_r)
    imgd = ImageDraw.Draw(img)
    imgd.text((0, 0), text, (255, 0, 0))

    bio_w = io.BytesIO()
    img.save(bio_w, format="JPEG")
    img_b_out = bio_w.getvalue()
    return img_b_out


def main(images):
        yield HTTP_HEADER
        n = 0
        for img_b in images:
            n += 1
            img_b_out = append_text(img_b, str(n))
            yield (b'\r\n--Ba4oTvQMY8ew04N8dcnM\r\n' +
                   b'Content-Type: image/jpeg\r\n' +
                   b'Content-Length: %d\r\n\r\n' % len(img_b_out) +
                   img_b_out)


def server_thread(images, port):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', port))


    while True:
        s.listen()
        sock, address = s.accept()
        for msg in main(images):
            try:
                sock.send(msg)
            except (BrokenPipeError, ConnectionResetError):
                break


if __name__ == '__main__':
    fout = open('/dev/stdout', 'wb')
    with open('/dev/stdin', 'rb') as f:
        for msg in main(yield_images(f)):
            fout.write(msg)
