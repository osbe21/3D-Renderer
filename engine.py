from dataclasses import dataclass, field
from gameobjects import *
from math import tan, radians
import numpy as np
import pygame as pg

@dataclass
class Engine:
    fov: float = radians(75)
    background_color: tuple[int, int, int] = (40, 40, 40)
    screen_size: tuple[int, int] = (640, 360) # 16:9
    camera: Camera = Camera.instances[0] if Camera.instances else Camera()
    near_clip: float = 0.1
    far_clip: float = 1000

    _window: pg.Surface = field(init=False)

    def __post_init__(self):
        self._projection_matrix: np.array = np.array([
            [1/(self.aspect_ratio * tan(self.fov/2)), 0, 0, 0],
            [0, 1/tan(self.fov/2), 0, 0],
            [0, 0, (self.near_clip + self.far_clip) / (self.near_clip - self.far_clip), 2 * self.far_clip * self.near_clip / (self.near_clip - self.far_clip)], 
            [0, 0, 1, 0]
        ])

        self._init_window()

        clock = pg.time.Clock()
        running = True

        if hasattr(self, 'start'):
            getattr(self, 'start')()

        while running:
            clock.tick(60)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            if hasattr(self, 'update'):
                getattr(self, 'update')()
            
            self._render()

            pg.display.update()
        
        pg.quit()

    def _init_window(self):
        self._window = pg.display.set_mode(self.screen_size)
        pg.display.set_caption(self.__class__.__name__)
        
    @property
    def aspect_ratio(self): 
        return self.screen_size[0] / self.screen_size[1]

    def _render(self):
        # Fjern alt fra skjermen
        self._window.fill(self.background_color)

        for mesh in Mesh.instances:
            vertices = mesh.vertices.copy()
            
            # Regn ut MVP matrise (model, view, projection)
            MVPmatrix = np.dot(self._projection_matrix, 
                            np.dot(np.linalg.inv(self.camera.transformation_matrix),
                                mesh.transformation_matrix))

            for idx, vertex in enumerate(vertices):

                # Konverter til homogene koordinater
                vertex = np.array([*vertex, 1])
                
                vertex = np.dot(MVPmatrix, vertex)

                # Del på homogen komponent
                if vertex[3] != 0:
                    vertex /= vertex[3]
                
                # Gjør om til screen space
                vertex[0] += 1
                vertex[1] += 1
                
                vertex[0] *= 0.5 * self.screen_size[0]
                vertex[1] *= 0.5 * self.screen_size[1]

                # Fordi pygame er lame
                vertex[1] *= -1
                vertex[1] += self.screen_size[1]

                # Lagre før rendering
                vertices[idx] = vertex[:2]
            
            # Render
            for tri_idx in np.reshape(mesh.indeces, (-1, 3)):
                tri = [vertices[idx] for idx in tri_idx]

                pg.draw.polygon(self._window, (255, 255, 255), tri, 1)
