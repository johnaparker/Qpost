import numpy as np
import h5py
import qpost.vec as vec

class source:
    def __init__(self, filename, group_name, source_name):
        self.filename = filename
        self.group_name = group_name
        self.path = "/sources/{0}/{1}".format(group_name, source_name)

class point_source(source):
    def __init__(self, filename, name):
        super().__init__(filename, "point", name)
        self.position = vec.load_vec(filename, self.path, "position")

class line_source(source):
    def __init__(self, filename, name):
        super().__init__(filename, "line", name)
        self.surface = vec.load_surface(filename, self.path)



class tfsf:
    def __init__(self, filename):
        self.path = "/sources/tfsf"
        self.volume = vec.load_volume(filename, self.path)
