from dataclasses import InitVar, dataclass, field
from gameobjects import *
import numpy     as np
import pygame    as pg

@dataclass
class Engine:
    background_color: tuple[int, int, int] = (40, 40, 40)

    screen_size: InitVar[tuple[int, int]] = (640, 360) # 16:9

    camera: Camera = Camera.instances[0] if Camera.instances else Camera()

    projection_matrix: np.array = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0], 
        [0, 0, 1, 0]
    ])

    _window: pg.Surface = field(init=False)

    def __post_init__(self, screen_size):
        self.SCREEN_SIZE = screen_size

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
        self._window = pg.display.set_mode(self.SCREEN_SIZE)
        pg.display.set_caption(self.__class__.__name__)
        

    def _render(self):
        # Fjern alt fra skjermen
        self._window.fill(self.background_color)

        for mesh in Mesh.instances:
            vertices = mesh.vertices.copy()
            
            # Regn ut MVP matrise (model, view, projection)
            MVPmatrix = np.dot(self.projection_matrix, 
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
                
                vertex[0] *= 0.5 * self.SCREEN_SIZE[0]
                vertex[1] *= 0.5 * self.SCREEN_SIZE[1]

                # Fordi pygame er lame
                vertex[1] *= -1
                vertex[1] += self.SCREEN_SIZE[1]

                # Lagre før rendering
                vertices[idx] = vertex[:2]
            
            # Render
            for tri_idx in np.reshape(mesh.indeces, (-1, 3)):
                tri = [vertices[idx] for idx in tri_idx]

                pg.draw.polygon(self._window, (0, 200, 0), tri, 1)
