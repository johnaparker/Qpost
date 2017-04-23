import h5py
import numpy as np
import qpost

class object:
    def __init__(self, filename, group_name, name):
        self.filename = filename
        self.group_name = group_name
        self.name = name
        self.path = "/objects/{0}/{1}".format(group_name, name)

        self.position = qpost.vec.load_vec(filename, self.path, "position")
        self.orientation = qpost.vec.load_vec(filename, self.path, "orientation")
        self.angle =  np.arctan2(self.orientation[1], self.orientation[0]) - np.pi/2

        with h5py.File(filename, 'r') as f:
            ref = f[self.path + "/material"][...].tolist()
            material_path = f[ref].name
            material_name = material_path[material_path.rfind("/")+1:]
            self.material = qpost.materials.load_material(filename, material_name)

class cylinder(object):
    def __init__(self, filename, name):
        super().__init__(filename, "cylinders", name)

        with h5py.File(filename, 'r') as f:
            self.radius = f[self.path]["radius"][...]

class ellipse(object):
    def __init__(self, filename, name):
        super().__init__(filename, "ellipses", name)

        with h5py.File(filename, 'r') as f:
            self.rx = f[self.path]["rx"][...]
            self.ry = f[self.path]["ry"][...]

class block(object):
    def __init__(self, filename, name):
        super().__init__(filename, "blocks", name)

        with h5py.File(filename, 'r') as f:
            self.dimensions = f[self.path]["dimensions"][...]
