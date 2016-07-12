import numpy as np
import matplotlib.pyplot as plt
import h5py as h5
from scipy.optimize import curve_fit

def flux_video(filename, dataname):
    import matplotlib.animation as animation

    fig = plt.figure()
    with  h5.File(filename, 'r') as h5file:
        dset = h5file[dataname]
        tf = dset.shape[1] - 1
        ymax = np.max(dset[...])
        ymin = np.min(dset[...])

        xdata = np.arange(dset.shape[0])
        ydata = dset[:,0]
        plt.ylim([ymin, ymax])
        line, = plt.plot(xdata,ydata)
        
        def update(frame):
            ydata = dset[:,frame]
            line.set_data(xdata,ydata)
            return line,

        ani = animation.FuncAnimation(fig, update, np.arange(0,tf), interval=30, blit=True)
        plt.show()

def load_flux(filename, dataname, t=-1):
    with  h5.File(filename, 'r') as h5file:
        h5data = h5file[dataname]
        if len(h5data.shape) > 1:
            flux = h5data[:,t]
        else:
            flux = np.array(h5data)
    return flux

def gaussian(x, A, x0, sig, c):
    return A*np.exp(-(x-x0)**2/(2*sig**2)) + c



if __name__ == "__main__":
    f = load_flux("../build/out.h5", "m1")
    x = np.linspace(1/30,3/30,len(f))
    plt.plot(x, -f, '.')

    res,var = curve_fit(gaussian, x, -f, (1,1,1,0)) 
    y_fit = gaussian(x, *res)
    plt.plot(x,y_fit, linewidth=2, color='r')

    print("A: {}".format(res[0]))
    print("f0: {}".format( res[1]))
    print("df: {}".format(abs( res[2])))
    print("c: {}".format(abs( res[3])))
    print("")
    print("l0: {}".format( 1/res[1]))
    print("dl: {}".format(abs( 1/res[2])))

    plt.show()
