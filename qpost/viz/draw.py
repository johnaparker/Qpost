import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

def rotation_transform(axis, angle, ax = plt.gca()):
    t_scale = ax.transData
    t_rotate = mpl.transforms.Affine2D().rotate_deg_around(axis[0], axis[1], angle*180/np.pi)
    return t_rotate + t_scale

def draw_box(p1, p2, angle = 0, ax = plt.gca(), **kwargs):
    p1 = np.asarray(p1)
    p2 = np.asarray(p2)

    center = (p1 + p2)/2
    t = rotation_transform(center, angle, ax)

    xy = p1
    width, height = p2 - p1
    box = mpl.patches.Rectangle(xy, width, height, transform=t, **kwargs)
    ax.add_patch(box)
    return box

def draw_circle(center, radius, ax = plt.gca(), **kwargs):
    center = np.asarray(center)

    circle = mpl.patches.Circle(center, radius, **kwargs)
    ax.add_patch(circle)
    return circle

def draw_ellipse(center, rx, ry, angle = 0, ax = plt.gca(), **kwargs):
    center = np.asarray(center)

    t = rotation_transform(center, angle, ax)

    xy = center
    ellipse = mpl.patches.Ellipse(xy, 2*rx, 2*ry, transform=t, **kwargs)
    ax.add_patch(ellipse)
    return ellipse
