import h5py
import numpy as np
import matplotlib.pyplot as plt
import qpost

def make_flux_plot(filename, in_group = None, in_name = None):
    with h5py.File(filename, 'r') as h5file:
        for group_name in h5file["monitors"].keys():
            h5group = h5file["monitors/{}".format(group_name)]

            if in_group and group_name not in in_group:
                continue

            for monitor_name in h5group.keys():
                if in_name and monitor_name not in in_name:
                    continue
                mon = qpost.monitors.monitor(filename, group_name, monitor_name)

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




def box_inside_box(v1, v2):
    """return true if v1 is inside v2"""
    return (v1['p1'] > v2['p1']).all() and (v1['p2'] < v2['p2']).all()

def box_outside_box(v1, v2):
    """return true if v1 is outside v2"""
    return (v1['p1'] < v2['p1']).all() and (v1['p2'] > v2['p2']).all()

def cyl_inside_box(s1, v2):
    """return true if s1 is inside v2"""
    b1 = s1["center"][1] + s1["radius"] < v2["p2"][1]
    b2 = s1["center"][1] - s1["radius"] > v2["p1"][1]
    b3 = s1["center"][0] + s1["radius"] < v2["p2"][0]
    b4 = s1["center"][0] - s1["radius"] > v2["p1"][0]
    return (b1 and b2 and b3 and b4)

def cyl_outside_box(s1, v2):
    """return true if v1 is outside v2
    This is not exactly accurate      """

    b1 = s1["center"][1] + s1["radius"] > v2["p2"][1]
    b2 = s1["center"][1] - s1["radius"] < v2["p1"][1]
    b3 = s1["center"][0] + s1["radius"] > v2["p2"][0]
    b4 = s1["center"][0] - s1["radius"] < v2["p1"][0]
    return (b1 and b2 and b3 and b4)


def cross_sections(filename):
    tfsf = qpost.sources.tfsf(filename)

    plt.figure()

    absorb = None
    scat = None
    with h5py.File(filename, 'r') as h5file:
        g = h5file["monitors"]

        if "box_monitor" in g:
            for box_name in g["box_monitor"]:
                mon = qpost.monitors.box_monitor(filename, box_name)
                if box_inside_box(mon.volume, tfsf.volume):
                    absorb = mon.flux()/tfsf.flux
                if box_outside_box(mon.volume, tfsf.volume):
                    scat = mon.flux()/tfsf.flux

        if "cylinder_monitor" in g:
            for cyl_name in g["cylinder_monitor"]:
                mon = qpost.monitors.cylinder_monitor(filename, cyl_name)
                if cyl_inside_box(mon.surface, tfsf.volume):
                    absorb = mon.flux()/tfsf.flux
                if cyl_outside_box(mon.surface, tfsf.volume):
                    scat = mon.flux()/tfsf.flux

    if absorb is not None:
        plt.plot(tfsf.frequency, absorb, label = "absoprtion")
    if scat is not None:
        plt.plot(tfsf.frequency, scat, label = "scattering")
    if absorb is not None and scat is not None:
        plt.plot(tfsf.frequency, scat+absorb, label = "extinction")

    plt.legend()
    plt.xlabel("frequency")
    plt.ylabel("cross-section")
    plt.show()
