import h5py
import numpy as np
import matplotlib.pyplot as plt
from qpost.monitors import monitor

def make_flux_plot(filename, in_group = None, in_name = None):
    with h5py.File(filename, 'r') as h5file:
        for group_name in h5file["monitors"].keys():
            h5group = h5file["monitors/{}".format(group_name)]

            if in_group and group_name not in in_group:
                continue

            for monitor_name in h5group.keys():
                if in_name and monitor_name not in in_name:
                    continue
                mon = monitor(filename, group_name, monitor_name)

                try:
                    flux = mon.flux()
                except:
                    continue

                freq = mon.freq
                plt.plot(freq, flux, '.-', label=monitor_name)

    plt.xlabel("frequency")
    plt.ylabel("flux")
    plt.legend()
    plt.show()
