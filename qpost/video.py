import os
import subprocess
import matplotlib.pyplot as plt
import h5py
import numpy as np


# is this slower than one h5topng call?
# add -R flag
# add defaults
# allow dynamic width
# delete temp directory
# specify name of video file
#  

def make_video(h5file, dataset, t0, tf):
    dirName = ".qpost_temp"
    os.mkdir(dirName)

    for t in range(t0, tf):
        imgFile = "out.t{number:0{width}d}.png".format(width=3, number=t)
        subprocess.call(["h5topng", "-t", "{0}".format(t), "-Zc", "dkbluered", "-a", "yarg", "{0}:{1}".format(h5file, dataset), "-o", "{0}/{1}".format(dirName, imgFile)])
        # subprocess.Popen(["h5topng", "-t {0}:{1}".format(t0,tf), "-Zc", "dkbluered", "-a", "yarg", "../{0}:{1}".format(h5file, dataset)], cwd=dirName)
    subprocess.call(["ffmpeg", "-i", "{0}/out.t%03d.png".format(dirName), "out.mp4", "-y"])

    # os.rmdir(dirName)

def make_video_other(h5file, dataset, t0=0, tf=-1, ms=30, saveFile=None,
                      norm=False):
    import numpy as np
    import matplotlib.pyplot as plt
    import h5py

    with h5py.File(h5file, 'r') as f:
        dset = f[dataset]
        for t in range(t0, tf):
            dataImg = dset[:,:,t]
            vmax = np.max(dataImg) 
            vmin = np.min(dataImg) 
            vmin = -vmax
            fig = plt.figure()
            # img = plt.pcolormesh(dataImg, cmap="bwr", vmin=vmin, vmax=vmax)
            img = plt.imshow(dataImg, cmap="bwr", vmin=vmin, vmax=vmax)
            plt.title(t)
            print("_temp{0:03d}.png".format(t-t0))
            plt.savefig("_temp{0:03d}.png".format(t-t0))
            plt.close()
    subprocess.call(["ffmpeg", "-i", "_temp%03d.png", "out.mp4", "-y"])
    os.system("rm _temp*")


def fp(h5file, dataset, t):
    with h5py.File(h5file, 'r') as f:
        dset = f[dataset]
        dataImg = dset[:,:,t]
        vmax = np.max(dataImg) 
        vmin = np.min(dataImg) 
        vmin = -vmax
        fig = plt.figure()
        # img = plt.pcolormesh(dataImg, cmap="bwr", vmin=vmin, vmax=vmax)
        img = plt.imshow(dataImg, cmap="bwr", vmin=vmin, vmax=vmax)
        plt.title(t)
        print("_temp{0:03d}.png".format(t))
        plt.savefig("_temp{0:03d}.png".format(t))
        plt.close()

def make_video_other_parallel(h5file, dataset, t0=0, tf=-1, ms=30, saveFile=None,
                      norm=False, cores=1):
    import numpy as np
    import h5py
    from multiprocessing import Pool

    p = Pool(cores)
    p.starmap(fp, [(h5file,dataset, i) for i in range(t0,tf)])

    subprocess.call(["ffmpeg", "-i", "_temp%03d.png", "out.mp4", "-y"])
    os.system("rm _temp*")


def make_video_other2(h5file, dataset, t0=0, tf=-1, ms=30, saveFile=None,
                      norm=False, monitors=False):
    import numpy as np
    import matplotlib.animation as animation


    fig = plt.figure()

    with h5py.File(h5file, 'r') as f:
        dset = f[dataset]
        if tf == -1:
            tf = dset.shape[-1] - 1
        dataImg = dset[:,:,t0]
        vmax = np.max(dataImg) 
        # vmin = np.min(dataImg) 
        vmin = -vmax
        
        if norm:
            # vmax = np.max(dset[...])
            for i in range(t0+1, tf):
                dataImg = dset[:,:,i]
                vmax = max(vmax,np.max(dataImg))
            vmin = -vmax
        
        points = {} 
        if monitors:
            for monitor in f["Monitors"]:
                group = f["Monitors/{0}".format(monitor)]
                point1 = np.array(group.attrs["p1"])
                point2 = np.array(group.attrs["p2"])
                points[monitor] = ((point1,point2))

        # im = plt.imshow(dataImg, cmap=plt.get_cmap('bwr'), vmin=vmin, vmax=vmax,  animated=True)
        im = plt.imshow(dataImg, cmap=plt.get_cmap('bwr'), vmin=vmin, vmax=vmax,  animated=True, origin="lower")
        plt.xlim([0,dset.shape[0]])
        plt.ylim([0,dset.shape[1]])

        line_objs = []
        text_objs = []
        
        if monitors:
            for mon in points:
                if mon[-2] == "_":
                    continue
                p1 = 2*points[mon][0]
                p2 = 2*points[mon][1]
                box, = plt.plot([p1[0], p1[0], p2[0], p2[0], p1[0]], [p1[1], p2[1], p2[1], p1[1], p1[1]], linewidth=2, linestyle="--", color='black')
                text = plt.text(p1[0],p2[1]+2, mon)
                # text = plt.text(p1[0],p2[1]+2, mon, bbox={'facecolor':'white', 'alpha':1, 'pad':1})
                line_objs.append(box)
                text_objs.append(text)

        def updatefig(frame):
            plt.title(frame)
            dataImg = dset[:,:,frame]
            im.set_array(dataImg)
            return [im] + line_objs + text_objs

        ani = animation.FuncAnimation(fig, updatefig, np.arange(t0,tf), interval=ms, blit=True)
        if saveFile:
            ani.save(saveFile)
        plt.show()
