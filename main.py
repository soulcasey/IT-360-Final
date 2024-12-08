import glfw
import random
from OpenGL.GL import *
from OpenGL.GLU import *
from cube import Cube
from sphere import Sphere
import numpy as np
from common import Vector3
import math

ROTATE_SPEED = 0.09
CAMERA_POSITION = (0.0, 0.0, -5)

SPHERE_RADIUS_RANGE = (0.1, 0.4)
SPHERE_COUNT = 100
SPHERE_SPEED_RANGE = (0.002, 0.004)

CUBE_SIZE = 2.5
CUBE_POSITION = Vector3(0, 0, 0)

MAX_ATTEMPT = 1000

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

    cube_x, cube_y, cube_z = *cube.position,

    min_radius, max_radius = SPHERE_RADIUS_RANGE

    x_min = cube_x - CUBE_SIZE / 2
    x_max = cube_x + CUBE_SIZE / 2
    y_min = cube_y - CUBE_SIZE / 2
    y_max = cube_y + CUBE_SIZE / 2
    z_min = cube_z - CUBE_SIZE / 2
    z_max = cube_z + CUBE_SIZE / 2

    attempt_count = 0

    while len(spheres) < SPHERE_COUNT:
        random_radius = random.uniform(min_radius, max_radius)
        
        random_position = Vector3(
            random.uniform(x_min + random_radius, x_max - random_radius),
            random.uniform(y_min + random_radius, y_max - random_radius),
            random.uniform(z_min + random_radius, z_max - random_radius)
        )

        is_valid = True
        for sphere in spheres:
            normal = Vector3(
                random_position.x - sphere.position.x,
                random_position.y - sphere.position.y,
                random_position.z - sphere.position.z
            )

            distance = math.sqrt(normal.x ** 2 + normal.y ** 2 + normal.z ** 2)
            if distance < random_radius + sphere.radius:
                is_valid = False
                break

        if is_valid:
            # Generate velocity and add the sphere if no overlap
            random_speed = random.uniform(*SPHERE_SPEED_RANGE)
            new_velocity = Vector3(
                random.choice([-1, 1]) * random_speed,
                random.choice([-1, 1]) * random_speed,
                random.choice([-1, 1]) * random_speed
            )
            spheres.append(Sphere(random_position, random_radius, new_velocity))
        else:
            attempt_count += 1

            if attempt_count > MAX_ATTEMPT:
                print("Max attempt exceeded")
                return
            
            # Try to lower maximum radius if too many attempt are reached
            elif attempt_count > MAX_ATTEMPT / 2:
                max_radius = min_radius

    is_auto = True

    # Main render loop
    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
            break

        if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
            glRotatef(ROTATE_SPEED * 3, 0, -1, 0)
            is_auto = False
        elif glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
            glRotatef(ROTATE_SPEED * 3, 0, 1, 0)
            is_auto = False
        elif glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS:
            is_auto = True
        if is_auto:
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
        overlap_1 = -collision_distance * sphere_2.radius / (sphere_1.radius + sphere_2.radius)
        sphere_1.position.x += normal.x * overlap_1
        sphere_1.position.y += normal.y * overlap_1
        sphere_1.position.z += normal.z * overlap_1

        overlap_2 = -collision_distance * sphere_1.radius / (sphere_1.radius + sphere_2.radius)
        sphere_2.position.x -= normal.x * overlap_2
        sphere_2.position.y -= normal.y * overlap_2
        sphere_2.position.z -= normal.z * overlap_2

if __name__ == "__main__":
    main()
