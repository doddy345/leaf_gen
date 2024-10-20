import matplotlib.pyplot as plt
import numpy as np

from matplotlib.widgets import Button, Slider

init_roundness = 1
init_spikes = 0
init_sa = 0.1
init_w = 1.0

l = 1.0

def normalize(x):
    return (x - np.min(x)) / (np.max(x) - np.min(x))

def get_leaf_side(roundness, l, s, sa, w):
    t = np.linspace(0, np.pi, 1000)

    r = l / (np.abs(np.cos(t / 4)) + np.abs(np.sin(t / 4))) ** (1 / roundness)
    r = r + sa * (np.sin(s * t) - 0.5 * np.cos(7 * t))

    y = np.cos(t) * r
    x = np.sin(t) * r
    return normalize(x) * w, normalize(y)


# Create the figure and the line that we will manipulate
fig, ax = plt.subplots()

x, y = get_leaf_side(init_roundness, l, init_spikes, init_sa, init_w)

line, = ax.plot(x, y, lw=1, color='g')
line2, = ax.plot(-x, y, lw=1, color='g')

# adjust the main plot to make room for the sliders
fig.subplots_adjust(left=0.5, bottom=0.25)

ax_roundness = fig.add_axes([0.1, 0.25, 0.0225, 0.63])
ax_spikes = fig.add_axes([0.2, 0.25, 0.0225, 0.63])
ax_sa = fig.add_axes([0.3, 0.25, 0.0225, 0.63])
ax_w = fig.add_axes([0.4, 0.25, 0.0225, 0.63])

roundness_slider = Slider(
    ax=ax_roundness,
    label="roundness",
    valmin=0.01,
    valmax=1,
    valinit=init_roundness,
    valstep=0.01,
    orientation="vertical"
)

spikes_slider = Slider(
    ax=ax_spikes,
    label="spikes",
    valmin=0,
    valmax=100,
    valinit=init_spikes,
    valstep=2,
    orientation="vertical"
)

sa_slider = Slider(
    ax=ax_sa,
    label="sa",
    valmin=0,
    valmax=0.1,
    valinit=init_sa,
    valstep=0.01,
    orientation="vertical"
)

width_slider = Slider(
    ax=ax_w,
    label="width",
    valmin=0.1,
    valmax=1.0,
    valinit=init_w,
    valstep=0.01,
    orientation="vertical"
)

def update(val):
    x, y = get_leaf_side(roundness_slider.val, l, spikes_slider.val, sa_slider.val, width_slider.val)
    line.set_xdata(x)
    line.set_ydata(y)
    line2.set_xdata(-x)
    line2.set_ydata(y)
    fig.canvas.draw()


roundness_slider.on_changed(update)
spikes_slider.on_changed(update)
sa_slider.on_changed(update)
width_slider.on_changed(update)

plt.show()