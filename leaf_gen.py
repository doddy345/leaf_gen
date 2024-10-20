import matplotlib.pyplot as plt
import numpy as np

from matplotlib.widgets import Button, Slider

init_roundness = 1
init_spikes = 0
init_sa = 0
init_w = 1.0
init_vein_length = 0.8
init_num_veins = 5
init_vein_wave = 0

vein_steps = 10

t = np.linspace(0, np.pi, 1000)

def normalize(x):
    return (x - np.min(x)) / (np.max(x) - np.min(x))

def get_r(t, roundness, s, sa):
    l = 1.0
    r = l / (np.abs(np.cos(t / 4)) + np.abs(np.sin(t / 4))) ** (1 / roundness)
    r = r + sa * np.abs(np.sin(s * t) - 0.5 * np.cos(7 * t))

    return normalize(r)

def get_leaf_side(roundness, s, sa, w):
    r = get_r(t, roundness, s, sa)

    x = np.sin(t) * r
    y = np.cos(t) * r

    return x * w, y

def get_main_vein(vl):
    x = np.zeros(vein_steps)
    y = np.linspace(0, vl, vein_steps)

    return x, y

def update(val):
    x, y = get_leaf_side(roundness_slider.val, spikes_slider.val, sa_slider.val, width_slider.val)
    line.set_xdata(x)
    line.set_ydata(y)
    line2.set_xdata(-x)
    line2.set_ydata(y)
    fig.canvas.draw()
    draw_small_veins()
    update_vein()

small_veins = []

def clear_small_veins():
    for sv in small_veins:
        sv.remove()
    
    small_veins.clear()

def get_side_vein(vein_y):
    all_points_x, all_points_y = get_leaf_side(roundness_slider.val, spikes_slider.val, sa_slider.val, width_slider.val)
    closest_point_idx = np.argmin(np.abs(all_points_y - vein_y))
    vein_x = 0.8 * all_points_x[closest_point_idx]

    x = np.linspace(0, vein_x, vein_steps)
    y = vein_y + 0.02 * np.sin(np.cos(vein_y) + x * np.pi  * vein_wave_slider.val)
    return x, y

def draw_small_vein(vein_y):
    x, y = get_side_vein(vein_y)
    small_veins.append(ax.plot(x, y, lw=1, color='brown')[0])
    small_veins.append(ax.plot(-x, y, lw=1, color='brown')[0])

def draw_small_veins():
    clear_small_veins()

    num_small_veins = num_veins_slider.val

    for i in range(num_small_veins):
        vein_y = i * main_vein_slider.val / num_small_veins
        draw_small_vein(vein_y)

    fig.canvas.draw()

def update_vein():
    _, y = get_main_vein(main_vein_slider.val)
    main_vein_line.set_ydata(y)
    draw_small_veins()
    fig.canvas.draw()



# Create the figure and the line that we will manipulate
fig, ax = plt.subplots()

x, y = get_leaf_side(init_roundness, init_spikes, init_sa, init_w)

line, = ax.plot(x, y, lw=1, color='g')
line2, = ax.plot(-x, y, lw=1, color='g')

x, y = get_main_vein(init_vein_length)
main_vein_line, = ax.plot(x, y, lw=1, color='brown')

# adjust the main plot to make room for the sliders
fig.subplots_adjust(left=0.5, bottom=0.4)

ax_roundness = fig.add_axes([0.1, 0.25, 0.0225, 0.63])
ax_spikes = fig.add_axes([0.2, 0.25, 0.0225, 0.63])
ax_sa = fig.add_axes([0.3, 0.25, 0.0225, 0.63])
ax_w = fig.add_axes([0.4, 0.25, 0.0225, 0.63])

ax_mv = fig.add_axes([0.2, 0.05, 0.63, 0.0225])
ax_nv = fig.add_axes([0.2, 0.1, 0.63, 0.0225])
ax_vw = fig.add_axes([0.2, 0.15, 0.63, 0.0225])

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

main_vein_slider = Slider(
    ax=ax_mv,
    label="main vein",
    valmin=0.1,
    valmax=1.0,
    valinit=init_vein_length,
    valstep=0.01,
    orientation="horizontal"
)

num_veins_slider = Slider(
    ax=ax_nv,
    label="num veins",
    valmin=1,
    valmax=50,
    valinit=init_num_veins,
    valstep=1,
    orientation="horizontal"
)


vein_wave_slider = Slider(
    ax=ax_vw,
    label="vein waviness",
    valmin=1,
    valmax=12,
    valinit=init_vein_wave,
    valstep=1,
    orientation="horizontal"
)

roundness_slider.on_changed(update)
spikes_slider.on_changed(update)
sa_slider.on_changed(update)
width_slider.on_changed(update)
num_veins_slider.on_changed(update)
main_vein_slider.on_changed(update)
vein_wave_slider.on_changed(update)

update(None)
plt.show()