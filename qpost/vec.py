import h5py
import numpy as np

def load_vec(filename, path, vec_name):
    with h5py.File(filename, 'r') as f:
        return f[path][vec_name][...]

def load_surface(filename, path):
    D = {}
    with h5py.File(filename, 'r') as f:
        D["p1"] = f[path]["p1"][...]
        D["p2"] = f[path]["p2"][...]
    return D

def load_volume(filename, path):
    return load_surface(filename, path)

def load_cylinder_surface(filename, path):
    D = {}
    with h5py.File(filename, 'r') as f:
        D["center"] = f[path]["center"][...]
        D["radius"] = f[path]["radius"][...]
    return D

def load_grid(filename):
    D = {}
    with h5py.File(filename, 'r') as f:
        g = f['grid']
        for dset_name in g:
            dset = g[dset_name]
            D[dset_name] = dset[...]
    return D

