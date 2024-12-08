from OpenGL.GL import *
from OpenGL.GLU import *
from cube import Cube
from common import Vector3
import random

class Sphere:
    def __init__(self, position: Vector3, radius: float, velocity: Vector3):
        self.velocity = velocity
        self.position = position
        self.radius = radius

        self.quadric = gluNewQuadric()
        gluQuadricDrawStyle(self.quadric, GLU_FILL)
        gluQuadricNormals(self.quadric, GLU_SMOOTH)

        self.color = (random.randrange(1, 100) / 100, random.randrange(1, 100) / 100, random.randrange(1, 100) / 100)

    def draw(self, cube: Cube = None):

        glColor3f(*self.color)

        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)

        gluSphere(self.quadric, self.radius, 16, 16)

        glPopMatrix()

    def is_inside(self, cube: Cube):

        cube_x, cube_y, cube_z = *cube.position,
        # Get the cube's bounds
        x_min = cube_x - cube.size / 2 + self.radius
        x_max = cube_x + cube.size / 2 - self.radius
        y_min = cube_y - cube.size / 2 + self.radius
        y_max = cube_y + cube.size / 2 - self.radius
        z_min = cube_z - cube.size / 2 + self.radius
        z_max = cube_z + cube.size / 2 - self.radius

        # Check if the sphere is inside the cube considering its radius
        return (x_min <= self.position.x <= x_max) and \
               (y_min <= self.position.y <= y_max) and \
               (z_min <= self.position.z <= z_max)

    def rebound(self, cube: Cube):

        cube_x, cube_y, cube_z = *cube.position,
        # Get the cube's bounds
        x_min = cube_x - cube.size / 2 + self.radius
        x_max = cube_x + cube.size / 2 - self.radius
        y_min = cube_y - cube.size / 2 + self.radius
        y_max = cube_y + cube.size / 2 - self.radius
        z_min = cube_z - cube.size / 2 + self.radius
        z_max = cube_z + cube.size / 2 - self.radius

        if x_min >= self.position.x:
            self.position.x = x_min
            self.velocity.x = abs(self.velocity.x)
        elif x_max <= self.position.x:
            self.position.x = x_max
            self.velocity.x = -abs(self.velocity.x)
        
        if y_min >= self.position.y:
            self.position.y = y_min
            self.velocity.y = abs(self.velocity.y)
        elif y_max <= self.position.y:
            self.position.y = y_max
            self.velocity.y = -abs(self.velocity.y)
        
        if z_min >= self.position.z:
            self.position.z = z_min
            self.velocity.z = abs(self.velocity.z)
        elif z_max <= self.position.z:
            self.position.z = z_max
            self.velocity.z = -abs(self.velocity.z)


    def move(self, direcion: Vector3):
        self.position.x += direcion.x
        self.position.y += direcion.y
        self.position.z += direcion.z
