import h5py
import numpy as np
import qpost.vec as vec

class material:
    def __init__(self, filename, path):
        with h5py.File(filename, 'r') as f:
            g = f[path]
            self.eps = g["eps"][0]
            self.mu = g["mu"][0]
            self.conduc = g["conduc"][0]

class object:
    def __init__(self, filename, group_name, name):
        self.filename = filename
        self.group_name = group_name
        self.name = name
        self.path = "/objects/{0}/{1}".format(group_name, name)

        self.position = vec.load_vec(filename, self.path, "position")
        self.orientation = vec.load_vec(filename, self.path, "orientation")
        self.angle =  np.arctan2(self.orientation[1], self.orientation[0]) - np.pi/2
        self.material = material(filename, self.path)

class cylinder(object):
    def __init__(self, filename, name):
        super().__init__(filename, "cylinders", name)

        with h5py.File(filename, 'r') as f:
            self.radius = f[self.path]["radius"][0]

class ellipse(object):
    def __init__(self, filename, name):
        super().__init__(filename, "ellipses", name)

        with h5py.File(filename, 'r') as f:
            self.rx = f[self.path]["rx"][0]
            self.ry = f[self.path]["ry"][0]

class block(object):
    def __init__(self, filename, name):
        super().__init__(filename, "blocks", name)

        with h5py.File(filename, 'r') as f:
            self.dimensions = f[self.path]["dimensions"][...]
