import numpy as np
from dataclasses import dataclass, field
from matrix_operation import MatrixOperation
from typing import ClassVar


@dataclass
class GameObject:
    position: np.array = field(default_factory=lambda: np.zeros(3))
    rotation: np.array = field(default_factory=lambda: np.zeros(3))
    scale: np.array = field(default_factory=lambda: np.ones(3))

    @property
    def transformation_matrix(self) -> np.array:

        # SRT
        matrix = MatrixOperation.scale(self.scale)
        matrix = np.dot(MatrixOperation.rotate_z(self.rotation[2]), matrix)
        matrix = np.dot(MatrixOperation.rotate_y(self.rotation[1]), matrix)
        matrix = np.dot(MatrixOperation.rotate_x(self.rotation[0]), matrix)
        matrix = np.dot(MatrixOperation.translate(self.position), matrix)

        return matrix


@dataclass
class Camera(GameObject):
    instances: ClassVar[list] = []

    def __post_init__(self):
        self.instances.append(self)


@dataclass
class Mesh(GameObject):
    instances: ClassVar[list] = []

    vertices: list[np.array] = field(default_factory=list)
    uvs: list[np.array] = field(default_factory=list)
    normals: list[np.array] = field(default_factory=list)
    indeces: list[int] = field(default_factory=list)

    def __post_init__(self):
        self.instances.append(self)
    
    @staticmethod
    def load_from_obj(path: str):
        mesh = Mesh()

        with open(path, 'r') as file:
            vertices = []
            uvs = []
            normals = []
            indeces = []

            for line in file.readlines():

                # Linje med vertex-data
                if line.startswith('v'):
                    vertex_type = line[1]

                    if vertex_type == ' ':
                        vertex = line.split(' ')[1:4]
                        vertex = np.array([float(i) for i in vertex])
                        vertices.append(vertex)

                    # UV-koordinat
                    elif vertex_type == 't':
                        uv = line.split(' ')[1:3]
                        uv = np.array([float(i) for i in uv])
                        uvs.append(uv)

                    # Normal-vektor
                    elif vertex_type == 'n':
                        normal = line.split(' ')[1:4]
                        normal = np.array([float(i) for i in normal])
                        normals.append(normal)
                    
                # Face
                elif line.startswith('f'):
                    face = line.split(' ')[1:4]
                    face = [int(i.split('/')[0])-1 for i in face]
                    indeces.extend(face)

            file.close()
        
        mesh.vertices = vertices
        mesh.uvs = uvs
        mesh.normals = normals
        mesh.indeces = indeces

        return mesh
