import matplotlib.pyplot as plt
import h5py
import numpy as np
import qpost
from qpost.viz.draw import draw_box,draw_circle, draw_ellipse

def make_video(h5file, dataset, t0=0, tf=-1, ms=30, saveFile=None,
                      norm=False, monitors=False, objects=False):

    import matplotlib.animation as animation

    grid = qpost.vec.load_grid(h5file)
    pml = int(grid["pml_thickness"])
    with h5py.File(h5file, 'r') as f:
        dset = f[dataset]
        if tf == -1:
            tf = dset.shape[-1] - 1

        dataImg = dset[:,:,t0]
        vmax = np.max(dataImg) 
        vmin = -vmax
        
        if norm:
            for i in range(t0+1, tf):
                # dataImg = dset[pml:-pml,pml:-pml,i]
                dataImg = dset[60,90,i]
                vmax = max(vmax,np.max(dataImg))
            vmin = -vmax
        dataImg = dset[:,:,t0]

        x = np.linspace(0, grid['Lx'], dset.shape[0])
        y = np.linspace(0, grid['Ly'], dset.shape[1])
        im = plt.pcolormesh(x,y,dataImg.T, cmap='RdBu', vmin=vmin, vmax=vmax, animated=True)
        
        monitor_patches = []
        if monitors:
            kwargs = {"linewidth": 1, "linestyle": '--', "fill": False}
            for monitor_group in f["monitors"]:
                sub_group = f["monitors/{}".format(monitor_group)]
                for monitor in sub_group:

                    if monitor_group == "box_monitor": 
                        mon = qpost.monitors.box_monitor(h5file, monitor)
                        patch = draw_box(mon.volume['p1'], mon.volume['p2'], **kwargs)

                    if monitor_group == "surface_monitor": 
                        mon = qpost.monitors.surface_monitor(h5file, monitor)
                        patch = draw_box(mon.surface['p1'], mon.surface['p2'], **kwargs)

                    if monitor_group == "cylinder_monitor": 
                        mon = qpost.monitors.cylinder_monitor(h5file, monitor)
                        patch = draw_circle(mon.surface['center'], mon.surface['radius'], **kwargs)

                    monitor_patches.append(patch)

        object_patches = []
        if objects:
            kwargs = {"alpha": 0.25, "color": 'gray'}
            for object_group in f["objects"]:
                sub_group = f["objects/{}".format(object_group)]
                for obj in sub_group:

                    if object_group == "cylinders": 
                        cyl = qpost.objects.cylinder(h5file, obj)
                        patch = draw_circle(cyl.position, cyl.radius, **kwargs)

                    if object_group == "blocks": 
                        b = qpost.objects.block(h5file, obj)
                        p1 = b.position - b.dimensions/2
                        p2 = b.position + b.dimensions/2
                        patch = draw_box(p1, p2, angle=b.theta, **kwargs)

                    if object_group == "ellipses": 
                        ell = qpost.objects.ellipse(h5file, obj)
                        patch = draw_ellipse(ell.position, ell.rx, ell.ry, angle=ell.theta, **kwargs)

                    object_patches.append(patch)

        def updatefig(frame):
            dataImg = dset[:-1,:-1,frame]
            im.set_array(np.ravel(dataImg.T))

            return [im] + monitor_patches + object_patches

        plt.gca().set_aspect('equal')
        ani = animation.FuncAnimation(plt.gcf(), updatefig, np.arange(t0,tf), interval=ms, blit=True)

        if saveFile:
            ani.save(saveFile)

        plt.show()

# def make_video(h5file, dataset, t0, tf):
    # dirName = ".qpost_temp"
    # os.mkdir(dirName)

    # for t in range(t0, tf):
        # imgFile = "out.t{number:0{width}d}.png".format(width=3, number=t)
        # subprocess.call(["h5topng", "-t", "{0}".format(t), "-Zc", "dkbluered", "-a", "yarg", "{0}:{1}".format(h5file, dataset), "-o", "{0}/{1}".format(dirName, imgFile)])
        # subprocess.Popen(["h5topng", "-t {0}:{1}".format(t0,tf), "-Zc", "dkbluered", "-a", "yarg", "../{0}:{1}".format(h5file, dataset)], cwd=dirName)
    # subprocess.call(["ffmpeg", "-i", "{0}/out.t%03d.png".format(dirName), "out.mp4", "-y"])

    # os.rmdir(dirName)

# def make_video_other(h5file, dataset, t0=0, tf=-1, ms=30, saveFile=None,
                      # norm=False):
    # import numpy as np
    # import matplotlib.pyplot as plt
    # import h5py

    # with h5py.File(h5file, 'r') as f:
        # dset = f[dataset]
        # for t in range(t0, tf):
            # dataImg = dset[:,:,t]
            # vmax = np.max(dataImg) 
            # vmin = np.min(dataImg) 
            # vmin = -vmax
            # fig = plt.figure()

            # img = plt.pcolormesh(dataImg, cmap="bwr", vmin=vmin, vmax=vmax)
            # img = plt.imshow(dataImg, cmap="bwr", vmin=vmin, vmax=vmax)
            # plt.title(t)
            # print("_temp{0:03d}.png".format(t-t0))
            # plt.savefig("_temp{0:03d}.png".format(t-t0))
            # plt.close()
    # subprocess.call(["ffmpeg", "-i", "_temp%03d.png", "out.mp4", "-y"])
    # os.system("rm _temp*")


# def fp(h5file, dataset, t):
    # with h5py.File(h5file, 'r') as f:
        # dset = f[dataset]
        # dataImg = dset[:,:,t]
        # vmax = np.max(dataImg) 
        # vmin = np.min(dataImg) 
        # vmin = -vmax
        # fig = plt.figure()
        # img = plt.pcolormesh(dataImg, cmap="bwr", vmin=vmin, vmax=vmax)
        # img = plt.imshow(dataImg, cmap="bwr", vmin=vmin, vmax=vmax)
        # plt.title(t)
        # print("_temp{0:03d}.png".format(t))
        # plt.savefig("_temp{0:03d}.png".format(t))
        # plt.close()

# def make_video_other_parallel(h5file, dataset, t0=0, tf=-1, ms=30, saveFile=None,
                      # norm=False, cores=1):
    # import numpy as np
    # import h5py
    # from multiprocessing import Pool

    # p = Pool(cores)
    # p.starmap(fp, [(h5file,dataset, i) for i in range(t0,tf)])

    # subprocess.call(["ffmpeg", "-i", "_temp%03d.png", "out.mp4", "-y"])
    # os.system("rm _temp*")


