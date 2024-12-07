import glfw
import random
from OpenGL.GL import *
from OpenGL.GLU import *
from cube import Cube
from sphere import Sphere
import numpy as np
from common import Vector3
import math

ROTATE_SPEED = 0.06
CAMERA_POSITION = (0.0, 0.0, -5)

SPHERE_RADIUS = 0.1
SPHERE_COUNT = 150
SPHERE_SPEED = 0.001

CUBE_SIZE = 2.5
CUBE_POSITION = Vector3(0, 0, 0)


def main():
    # Basic Initialization
    if not glfw.init():
        print("Failed to initialize")
        return

    window = glfw.create_window(1000, 800, "Final", None, None)
    if not window:
        glfw.terminate()
        print("Failed to create window")
        return

    glfw.make_context_current(window)

    glEnable(GL_DEPTH_TEST)
    gluPerspective(45, 1000 / 800, 0.1, 50.0)
    glTranslatef(*CAMERA_POSITION)

    cube = Cube(CUBE_POSITION, CUBE_SIZE)
    spheres = []

    diameter = SPHERE_RADIUS * 2

    cube_x, cube_y, cube_z = *cube.position,

    x_min = cube_x - CUBE_SIZE / 2 + diameter
    x_max = cube_x + CUBE_SIZE / 2 - SPHERE_RADIUS
    y_min = cube_y - CUBE_SIZE / 2 + diameter
    y_max = cube_y + CUBE_SIZE / 2 - SPHERE_RADIUS
    z_min = cube_z - CUBE_SIZE / 2 + diameter
    z_max = cube_z + CUBE_SIZE / 2 - SPHERE_RADIUS

    # Generate all possible positions where spheres can be placed
    possible_positions = []
    for x in np.arange(x_min, x_max, diameter):
        for y in np.arange(y_min, y_max, diameter):
            for z in np.arange(z_min, z_max, diameter):
                possible_positions.append(Vector3(x, y, z))

    if SPHERE_COUNT > len(possible_positions):
        print("Not enough positions")
        return

    # Generate spheres with random positino and velocity
    for _ in range(SPHERE_COUNT):
        random_index = random.randint(0, len(possible_positions) - 1)
        new_position: Vector3 = possible_positions[random_index]
        new_velocity = Vector3(random.choice([-1, 1]) * SPHERE_SPEED, random.choice([-1, 1]) * SPHERE_SPEED, random.choice([-1, 1]) * SPHERE_SPEED)
        spheres.append(Sphere(new_position, SPHERE_RADIUS, new_velocity))
        possible_positions.pop(random_index) 

    # Main render loop
    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
        #     glRotatef(ROTATE, 0, -1, 0)
        # elif glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
        glRotatef(ROTATE_SPEED, 0, 1, 0)

        for sphere in spheres:
            sphere: Sphere
            sphere.draw(cube)

        cube.draw()

        for sphere in spheres:
            sphere: Sphere
            sphere.move(sphere.velocity)
            sphere.rebound(cube)
        
        for i in range(len(spheres)):
            for j in range(i + 1, len(spheres)):
                collision(spheres[i], spheres[j])
        
        glfw.swap_buffers(window)

    # Cleanup and exit
    glfw.terminate()

def collision(sphere_1: Sphere, sphere_2: Sphere):
    # Calculate the vector between the two sphere centers
    normal = Vector3(
        sphere_1.position.x - sphere_2.position.x,
        sphere_1.position.y - sphere_2.position.y,
        sphere_1.position.z - sphere_2.position.z
    )

    distance = math.sqrt(normal.x ** 2 + normal.y ** 2 + normal.z ** 2)
    collision_distance = distance - (sphere_1.radius + sphere_2.radius)

    # If the spheres are colliding
    if collision_distance < 0 and distance > 0.001:
        # Normalize the collision normal
        normal.x /= distance
        normal.y /= distance
        normal.z /= distance

        # Resolve overlap by moving spheres apart
        overlap = -collision_distance / 2
        sphere_1.position.x += normal.x * overlap
        sphere_1.position.y += normal.y * overlap
        sphere_1.position.z += normal.z * overlap

        sphere_2.position.x -= normal.x * overlap
        sphere_2.position.y -= normal.y * overlap
        sphere_2.position.z -= normal.z * overlap

if __name__ == "__main__":
    main()
