#!/usr/bin/env python3

import sys
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import PIL.Image
import io

import threading
import mjpeg_server
import queue

q = queue.Queue()

TRIANGLES = []
im = 0
CAMERA_X, CAMERA_Y, CAMERA_Z = (-0.5, 0.5, 0.5)

def yield_images():
    while True:
        yield q.get()


def append_node(x, z, c):
    global TRIANGLES
    TRIANGLES.append(
        [{'u': 0.0, 'v': 0.0, 'x': x, 'y': 0.0, 'z': z},
         {'u': 0.0, 'v': 0.0, 'x': x + 1.0, 'y': 0.0, 'z': z},
         {'u': 0.0, 'v': 0.0, 'x': x + 1.0, 'y': 0.0, 'z': z + 1.0}
         ])

    TRIANGLES.append(
        [{'u': 0.0, 'v': 0.0, 'x': x, 'y': 0.0, 'z': z},
         {'u': 0.0, 'v': 0.0, 'x': x, 'y': 0.0, 'z': z + 1.0},
         {'u': 0.0, 'v': 0.0, 'x': x + 1.0, 'y': 0.0, 'z': z + 1.0}
         ]
    )

    TRIANGLES.append(
        [{'u': 0.0, 'v': 0.0, 'x': x, 'y': 1.0, 'z': z},
         {'u': 0.0, 'v': 0.0, 'x': x + 1.0, 'y': 1.0, 'z': z},
         {'u': 0.0, 'v': 0.0, 'x': x + 1.0, 'y': 1.0, 'z': z + 1.0}
         ])

    TRIANGLES.append(
        [{'u': 0.0, 'v': 0.0, 'x': x, 'y': 1.0, 'z': z},
         {'u': 0.0, 'v': 0.0, 'x': x, 'y': 1.0, 'z': z + 1.0},
         {'u': 0.0, 'v': 0.0, 'x': x + 1.0, 'y': 1.0, 'z': z + 1.0}
         ])

    if c == ' ':
        return

    TRIANGLES.append(
        [{'x': x + 1.0, 'y': 1.0, 'z': z, 'u': 0.0, 'v': 1.0},
         {'x': x + 1.0, 'y': 0.0, 'z': z, 'u': 0.0, 'v': 0.0},
         {'x': x, 'y': 0.0, 'z': z, 'u': 1.5, 'v': 0.0}
         ])

    TRIANGLES.append(
        [{'x': x + 1.0, 'y': 1.0, 'z': z, 'u': 0.0, 'v': 1.0},
         {'x': x, 'y': 1.0, 'z': z, 'u': 1.5, 'v': 1.0},
         {'x': x, 'y': 0.0, 'z': z, 'u': 1.5, 'v': 0.0}
         ])

    TRIANGLES.append(
        [{'x': x + 1.0, 'y': 1.0, 'z': z + 1.0, 'u': 0.0, 'v': 1.0},
         {'x': x + 1.0, 'y': 0.0, 'z': z + 1.0, 'u': 0.0, 'v': 0.0},
         {'x': x + 1.0, 'y': 0.0, 'z': z, 'u': 1.5, 'v': 0.0}
         ])

    TRIANGLES.append(
        [{'x': x + 1.0, 'y': 1.0, 'z': z + 1.0, 'u': 0.0, 'v': 1.0},
         {'x': x + 1.0, 'y': 1.0, 'z': z, 'u': 1.5, 'v': 1.0},
         {'x': x + 1.0, 'y': 0.0, 'z': z, 'u': 1.5, 'v': 0.0}
         ])

    TRIANGLES.append(
        [{'x': x, 'y': 1.0, 'z': z + 1.0, 'u': 0.0, 'v': 1.0},
         {'x': x, 'y': 0.0, 'z': z + 1.0, 'u': 0.0, 'v': 0.0},
         {'x': x, 'y': 0.0, 'z': z, 'u': 1.5, 'v': 0.0}
         ])

    TRIANGLES.append(
        [{'x': x, 'y': 1.0, 'z': z + 1.0, 'u': 0.0, 'v': 1.0},
         {'x': x, 'y': 1.0, 'z': z, 'u': 1.5, 'v': 1.0},
         {'x': x, 'y': 0.0, 'z': z, 'u': 1.5, 'v': 0.0}
         ])

    TRIANGLES.append(
        [{'x': x + 1.0, 'y': 1.0, 'z': z + 1.0, 'u': 0.0, 'v': 1.0},
         {'x': x + 1.0, 'y': 0.0, 'z': z + 1.0, 'u': 0.0, 'v': 0.0},
         {'x': x, 'y': 0.0, 'z': z + 1.0, 'u': 1.5, 'v': 0.0}
         ])

    TRIANGLES.append(
        [{'x': x + 1.0, 'y': 1.0, 'z': z + 1.0, 'u': 0.0, 'v': 1.0},
         {'x': x, 'y': 1.0, 'z': z + 1.0, 'u': 1.5, 'v': 1.0},
         {'x': x, 'y': 0.0, 'z': z + 1.0, 'u': 1.5, 'v': 0.0}
         ])


def load_maze():
    with open('data/maze.txt') as f:
        for x, line in enumerate(f):
            for z, c in enumerate(line.rstrip()):
                append_node(x, z, c)


def setup_textures():
    global im
    img = pygame.image.load('data/texture.bmp')
    textureData = pygame.image.tostring(img, "RGB", 1)
    width = img.get_width()
    height = img.get_height()

    im = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, im)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB,
                 GL_UNSIGNED_BYTE, textureData)

def save_buffer():
    width, height = (600, 600)
    data = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)
    bio = io.BytesIO()
    PIL.Image.frombytes("RGB", (width, height), data).save(bio, "PNG")
    q.put(bio.getvalue())


def display():
    global CAMERA_Z

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()


    CAMERA_Z -= 0.01

    xtrans, ytrans, ztrans = -CAMERA_X, -CAMERA_Y, -CAMERA_Z
    glTranslatef(xtrans, ytrans, ztrans)

    rotateX = 0
    rotateY = 180
    glRotatef(rotateX, 1.0, 0, 0)
    glRotatef(rotateY, 0, 1.0, 0)

    glBindTexture(GL_TEXTURE_2D, im)

    glBegin(GL_TRIANGLES)
    glNormal3f(0.0, 0.0, 1.0)
    for triangle in TRIANGLES:

        for i in range(3):
            t = triangle[i]
            glTexCoord2f(t['u'], t['v'])
            glVertex3f(t['x'], t['y'], t['z'])

    glEnd()
    glutSwapBuffers()
    save_buffer()


def initGL():
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 0.05, 100)

    glMatrixMode(GL_MODELVIEW)


def main():

    threading.Thread(target=mjpeg_server.server_thread,
                     args=(yield_images(),)).start()

    load_maze()
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutCreateWindow('interactive')
    glutDisplayFunc(display)
    setup_textures()
    initGL()
    glutIdleFunc(display)
    glutMainLoop()


if __name__ == '__main__':
    main()
