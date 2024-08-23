import numpy as np
from math import sin, cos

class MatrixOperation:
    @staticmethod
    def translate(xyz):
        return np.array([
            [1, 0, 0, xyz[0]],
            [0, 1, 0, xyz[1]],
            [0, 0, 1, xyz[2]],
            [0, 0, 0, 1],
        ])
    
    @staticmethod
    def rotate_x(theta):
        return np.array([
            [1, 0, 0, 0],
            [0, cos(theta), -sin(theta), 0],
            [0, sin(theta), cos(theta), 0],
            [0, 0, 0, 1],
        ])
    
    @staticmethod
    def rotate_y(theta):
        return np.array([
            [cos(theta), 0, sin(theta), 0],
            [0, 1, 0, 0],
            [-sin(theta), 0, cos(theta), 0],
            [0, 0, 0, 1],
        ])
    
    @staticmethod
    def rotate_z(theta):
        return np.array([
            [cos(theta), -sin(theta), 0, 0],
            [sin(theta), cos(theta), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ])
    
    @staticmethod
    def scale(xyz):
        return np.array([
            [xyz[1], 0, 0, 0],
            [0, xyz[1], 0, 0],
            [0, 0, xyz[2], 0],
            [0, 0, 0, 1]
        ])
