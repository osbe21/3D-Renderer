from rendering_engine import Engine
from gameobjects import Mesh
import numpy as np


class Game(Engine):
    def start(self):
        # self.camera.position[1] += 2
        self.camera.position[2] -= 3

        self.torus = Mesh.load_from_obj("models/chair.obj")
    
        # self.mesh = Mesh(vertices=[np.array([0, 1, 0]), np.array([1, 0, 0]), np.array([0, 0, 0])], indeces=[0, 1, 2])

    def update(self):
        self.torus.rotation[1] += 0.02
        self.torus.rotation[0] -= 0.01


game = Game(screen_size=(16*60, 9*60))