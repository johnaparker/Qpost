import h5py
import numpy as np
import qpost.vec as vec

class simple_material:
    def __init__(self, eps, mu, conduc, material_type = "simple_material", name = None):
        self.eps = eps
        self.mu = mu
        self.conduc = conduc

    def eps(self, freq):
        """Return the complex permitvitty at freq"""
        omega = 2*np.pi*freq
        return self.eps + 1j*self.sigma/omega

class debye:
    def __init__(self, eps_inf, delta_epsilon, tau, material_type = "debye", name = None):
        self.eps_inf = eps_inf
        self.delta_epsilon = delta_epsilon
        self.tau = tau
        self.material_type = material_type
        self.name = name

    def eps(self, freq):
        """Return the complex permitvitty at freq"""
        omega = 2*np.pi*freq
        return self.eps_inf + (self.delta_epsilon/(1 - 1j*omega*self.tau))
        # return self.eps_inf + np.sum(self.delta_epsilon/(1 + 1j*omega*self.tau))


class drude:
    def __init__(self, eps_inf, omega_0, gamma, material_type = "drude", name = None):
        self.eps_inf = eps_inf
        self.omega_0 = omega_0
        self.gamma = gamma
        self.material_type = material_type
        self.name = name

    def eps(self, freq):
        """Return the complex permitvitty at freq"""
        omega = 2*np.pi*freq
        return self.eps_inf - np.sum(self.omega_0[:,np.newaxis]**2/(omega**2 + 1j*omega*self.gamma[:,np.newaxis]), axis=0)

class lorentz:
    def __init__(self, eps_inf, delta_epsilon, omega_0, gamma, material_type = "lorentz", name = None):
        self.eps_inf = eps_inf
        self.delta_epsilon = delta_epsilon
        self.omega_0 = omega_0
        self.gamma = gamma
        self.material_type = material_type
        self.name = name

    def eps(self, freq):
        """Return the complex permitvitty at freq"""
        omega = 2*np.pi*freq
        return self.eps_inf - np.sum(self.delta_epsilon*self.omega_0**2/(self.omega_0**2 - omega**2 + 2j*omega*self.gamma))

def load_material(filename, material_name):
    """Load a material from a file of name material_name"""
    kwargs = {}
    path = "materials/{0}".format(material_name)
    with h5py.File(filename, 'r') as f:
        g = f[path]
        for item in g:
            kwargs[item] = g[item][...]

    mat_type = kwargs["material_type"].tolist().decode()
    mat_map = {"simple_material": simple_material, 
               "lorentz": lorentz,
               "drude":   drude,
               "debye":   debye }

    return mat_map[mat_type](**kwargs)

def load_all_materials(filename):
    """Load all materials in file. Returns a dictionary"""
    materials = {}
    with h5py.File(filename, 'r') as f:
        g = f["materials"]
        for material_name in g:
            materials[material_name] = load_material(filename, material_name)
    return materials



