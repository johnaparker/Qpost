import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

def draw_box(p1, p2, angle = 0, ax = plt.gca(), **kwargs):
    t_scale = ax.transData
    center = (p1 + p2)/2
    t_rotate = mpl.transforms.Affine2D().rotate_deg_around(center[0], center[1], angle*180/np.pi)
    t = t_rotate + t_scale

    xy = p1
    width, height = p2 - p1
    box = mpl.patches.Rectangle(xy, width, height, transform=t, **kwargs)
    ax.add_patch(box)
    return box

def draw_circle(center, radius, ax = plt.gca(), **kwargs):
    circle = mpl.patches.Circle(center, radius, **kwargs)
    ax.add_patch(circle)
    return circle
