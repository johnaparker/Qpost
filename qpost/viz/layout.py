import h5py
import matplotlib.pyplot as plt
import numpy as np
import qpost
from . import draw

def make_layout(h5file):
    grid = qpost.vec.load_grid(h5file)
    x = np.linspace(0, grid['Lx'], grid["Nx"])
    y = np.linspace(0, grid['Ly'], grid["Ny"])
    pml = int(grid["pml_thickness"])

    c1 = np.array([x[0], y[0]])
    c2 = np.array([x[-1], y[-1]])


    #*** draw collection using patch_collection here
    kwargs = {"alpha": 0.5, "facecolor": 'orange', "linewidth": 0}
    patch = draw.draw_box(c1,c1 + np.array([grid['Lx'], pml*grid['dx']]), **kwargs)
    patch = draw.draw_box(c1 + np.array([0,pml*grid['dx']]),c1 + np.array([pml*grid['dx'], grid['Ly']]), **kwargs)
    patch = draw.draw_box(c2 + np.array([-pml*grid['dx'],-grid['Ly']+pml*grid['dx']]), c2, **kwargs)
    patch = draw.draw_box(c1 + np.array([pml*grid['dx'],grid['Ly']-pml*grid['dx']]), 
            c2 - np.array([pml*grid['dx'],0]), **kwargs)



    with h5py.File(h5file, 'r') as f:

        if "monitors" in f:
            kwargs = {"linewidth": 1, "linestyle": '--', "fill": False}
            for monitor_group in f["monitors"]:
                sub_group = f["monitors/{}".format(monitor_group)]
                for monitor in sub_group:

                    if monitor_group == "box_monitor": 
                        mon = qpost.monitors.box_monitor(h5file, monitor)
                        patch = draw.draw_box(mon.volume['p1'], mon.volume['p2'], **kwargs)

                    if monitor_group == "surface_monitor": 
                        mon = qpost.monitors.surface_monitor(h5file, monitor)
                        patch = draw.draw_box(mon.surface['p1'], mon.surface['p2'], **kwargs)

                    if monitor_group == "cylinder_monitor": 
                        mon = qpost.monitors.cylinder_monitor(h5file, monitor)
                        patch = draw.draw_circle(mon.surface['center'], mon.surface['radius'], **kwargs)

        if "objects" in f:
            kwargs = {"alpha": 0.75, "color": 'dodgerblue'}
            for object_group in f["objects"]:
                sub_group = f["objects/{}".format(object_group)]
                for obj in sub_group:

                    if object_group == "cylinders": 
                        cyl = qpost.objects.cylinder(h5file, obj)
                        patch = draw.draw_circle(cyl.position, cyl.radius, **kwargs)

                    if object_group == "blocks": 
                        b = qpost.objects.block(h5file, obj)
                        p1 = b.position - b.dimensions/2
                        p2 = b.position + b.dimensions/2
                        patch = draw.draw_box(p1, p2, angle=b.angle, **kwargs)

                    if object_group == "ellipses": 
                        ell = qpost.objects.ellipse(h5file, obj)
                        patch = draw.draw_ellipse(ell.position, ell.rx, ell.ry, angle=ell.angle, **kwargs)

        if "sources" in f:
            kwargs = {"linewidth": 1, "linestyle": '-', "fill": True, "color": 'red'}
            for source_group in f["sources"]:
                sub_group = f["sources/{}".format(source_group)]
                for source_name in sub_group:

                    if source_group == "point": 
                        source = qpost.sources.point_source(h5file, source_name)
                        patch = draw.draw_circle(source.position, 0.5*grid['dx'], **kwargs)

                    if source_group == "line": 
                        source = qpost.sources.line_source(h5file, source_name)
                        patch = draw.draw_box(source.surface['p1'], source.surface['p2'], **kwargs)

    plt.gca().set_aspect('equal')
    plt.xlim([x[0], x[-1]])
    plt.ylim([y[0], y[-1]])
    plt.show()
