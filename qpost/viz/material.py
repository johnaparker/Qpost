import matplotlib.pyplot as plt
import numpy as np
import qpost

def plot_materials(h5file):
    materials = qpost.materials.load_all_materials(h5file) 
    f_min, f_max = qpost.monitors.get_freq_range(h5file)

    freq = np.linspace(f_min, f_max, 1000)
    for name,material in materials.items():
        eps = material.perimitivitty(freq)
        plt.figure()
        plt.plot(freq, eps.real, label = r'Re($\varepsilon_r$)')
        plt.plot(freq, eps.imag, label = r'Im($\varepsilon_r$)')

        plt.title(name)
        plt.xlabel("frequency")
        plt.ylabel("permitvitty")
        plt.legend()

    plt.show()
