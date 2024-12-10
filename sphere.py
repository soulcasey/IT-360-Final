from OpenGL.GL import *
from OpenGL.GLU import *
from cube import Cube
from common import Vector3
import random

RECOVERY_RATE = 0.005

class Sphere:
    def __init__(self, position: Vector3, radius: float, direction: Vector3, speed: float):
        self.position = position
        self.radius = radius
        self.direction = direction 
        self.original_speed = speed
        self.current_speed = speed

        self.quadric = gluNewQuadric()
        gluQuadricDrawStyle(self.quadric, GLU_FILL)
        gluQuadricNormals(self.quadric, GLU_SMOOTH)

        self.color = (random.random(), random.random(), random.random())

    def draw(self):
        glColor3f(*self.color)

        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
        gluSphere(self.quadric, self.radius, 16, 16)
        glPopMatrix()

    def is_inside(self, cube: Cube):
        # Get the cube's bounds
        x_min = cube.position.x - cube.size / 2 + self.radius
        x_max = cube.position.x + cube.size / 2 - self.radius
        y_min = cube.position.y - cube.size / 2 + self.radius
        y_max = cube.position.y + cube.size / 2 - self.radius
        z_min = cube.position.z - cube.size / 2 + self.radius
        z_max = cube.position.z + cube.size / 2 - self.radius

        # Check if the sphere is inside the cube considering its radius
        return (x_min <= self.position.x <= x_max) and \
               (y_min <= self.position.y <= y_max) and \
               (z_min <= self.position.z <= z_max)

    def rebound(self, cube: Cube):
        # Get the cube's bounds
        x_min = cube.position.x - cube.size / 2 + self.radius
        x_max = cube.position.x + cube.size / 2 - self.radius
        y_min = cube.position.y - cube.size / 2 + self.radius
        y_max = cube.position.y + cube.size / 2 - self.radius
        z_min = cube.position.z - cube.size / 2 + self.radius
        z_max = cube.position.z + cube.size / 2 - self.radius

        # Handle collisions with cube boundaries
        if self.position.x < x_min:
            self.position.x = x_min
            self.direction.x = abs(self.direction.x)
        elif self.position.x > x_max:
            self.position.x = x_max
            self.direction.x = -abs(self.direction.x)

        if self.position.y < y_min:
            self.position.y = y_min
            self.direction.y = abs(self.direction.y)
        elif self.position.y > y_max:
            self.position.y = y_max
            self.direction.y = -abs(self.direction.y)

        if self.position.z < z_min:
            self.position.z = z_min
            self.direction.z = abs(self.direction.z)
        elif self.position.z > z_max:
            self.position.z = z_max
            self.direction.z = -abs(self.direction.z)

    def move(self, move_by: Vector3 = None):

        if move_by is None:
            move_by = Vector3(  self.direction.x * self.current_speed,
                                self.direction.y * self.current_speed,
                                self.direction.z * self.current_speed)

        # Update position based on direction and speed
        self.position.x += move_by.x
        self.position.y += move_by.y
        self.position.z += move_by.z

        # Gradually restore speed to original
        if self.current_speed != self.original_speed:
            speed_diff = self.original_speed - self.current_speed
            self.current_speed += speed_diff * RECOVERY_RATE
