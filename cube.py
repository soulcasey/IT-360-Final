from OpenGL.GL import *
from OpenGL.GLU import *
from common import Vector3

class Cube:
    def __init__(self, position: Vector3, size):
        self.position: Vector3 = position
        self.size = size

        x, y, z = *position,

        self.vertices = [
            Vector3(x - size / 2, y - size / 2, z - size / 2),  # Bottom-left-back
            Vector3(x + size / 2, y - size / 2, z - size / 2),  # Bottom-right-back
            Vector3(x + size / 2, y + size / 2, z - size / 2),  # Top-right-back
            Vector3(x - size / 2, y + size / 2, z - size / 2),  # Top-left-back
            Vector3(x - size / 2, y - size / 2, z + size / 2),  # Bottom-left-front
            Vector3(x + size / 2, y - size / 2, z + size / 2),  # Bottom-right-front
            Vector3(x + size / 2, y + size / 2, z + size / 2),  # Top-right-front
            Vector3(x - size / 2, y + size / 2, z + size / 2),  # Top-left-front
        ]

        self.surfaces = [
            (0, 1, 2, 3),  # Back face
            (4, 5, 6, 7),  # Front face
            (0, 1, 5, 4),  # Bottom face
            (2, 3, 7, 6),  # Top face
            (0, 3, 7, 4),  # Left face
            (1, 2, 6, 5)   # Right face
        ]

    def draw(self):
        glPushMatrix()

        glBegin(GL_LINES)
        
        glColor3f(1.0, 1.0, 1.0)

        edges = set()
        for surface in self.surfaces:
            for i in range(len(surface)):
                edge = (surface[i], surface[(i + 1) % len(surface)])
                edges.add(tuple(sorted(edge)))
        
        # Draw edges
        for edge in edges:
            for vertex_index in edge:
                vertex: Vector3 = self.vertices[vertex_index]
                glVertex3fv(list(vertex))

        glEnd()

        glPopMatrix()

    def move(self, direcion: Vector3):
        self.position.x += direcion.x
        self.position.y += direcion.y
        self.position.z += direcion.z
        self.vertices = [[vertex[0] + direcion.x, vertex[1] + direcion.y, vertex[2] + direcion.z] for vertex in self.vertices]