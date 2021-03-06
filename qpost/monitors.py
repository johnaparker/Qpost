import numpy as np
import h5py
import qpost.vec as vec

def load_frequency(filename, path):
    with h5py.File(filename, 'r') as f:
        return f[path]["dft_frequency"][...]

class monitor:
    def __init__(self, filename, group_name, monitor_name):
        self.filename = filename
        self.group_name = group_name
        self.path = "/monitors/{0}/{1}".format(group_name, monitor_name)
        self.freq = load_frequency(filename, self.path)

    def flux(self):
        with h5py.File(self.filename) as f:
            flux = f[self.path]["flux"][...]
            return flux

class surface_monitor(monitor):
    def __init__(self, filename, name):
        super().__init__(filename, "surface_monitor", name)
        self.surface = vec.load_surface(filename, self.path)

class box_monitor(monitor):
    def __init__(self, filename, name):
        super().__init__(filename, "box_monitor", name)
        self.volume = vec.load_volume(filename, self.path)

class cylinder_monitor(monitor):
    def __init__(self, filename, name):
        super().__init__(filename, "cylinder_monitor", name)
        self.surface = vec.load_cylinder_surface(filename, self.path)

def get_freq_range(filename):
    """get (min_freq, max_freq) across all existing monitors (includes tfsf)"""

    with h5py.File(filename, 'r') as f:
        min_freq = np.inf
        max_freq = 0

        def find_freq(name, dset):
            nonlocal min_freq, max_freq
            if "frequency" in name:
                freq = dset[...]
                min_freq = min(min_freq, np.min(freq))
                max_freq = max(max_freq, np.max(freq))

        f.visititems(find_freq)

        return min_freq, max_freq

# def flux_video(filename, dataname):
    # import matplotlib.animation as animation

    # fig = plt.figure()
    # with  h5.File(filename, 'r') as h5file:
        # dset = h5file[dataname]
        # tf = dset.shape[1] - 1
        # ymax = np.max(dset[...])
        # ymin = np.min(dset[...])

        # xdata = np.arange(dset.shape[0])
        # ydata = dset[:,0]
        # plt.ylim([ymin, ymax])
        # line, = plt.plot(xdata,ydata)
        
        # def update(frame):
            # ydata = dset[:,frame]
            # line.set_data(xdata,ydata)
            # return line,

        # ani = animation.FuncAnimation(fig, update, np.arange(0,tf), interval=30, blit=True)
        # plt.show()
