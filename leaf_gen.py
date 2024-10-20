import matplotlib.pyplot as plt
import numpy as np

wave_amt = 0.3
num_waves = 4

# Between 0 and 1 - 0 being a straight line, 1 being a circle
tubbiness = 0.5

shift = 0.6

def plot_leaf():
    t = np.linspace(0, np.pi, 100)

    # A general wiggly sin wave
    x_mod = np.sin(t * num_waves + np.pi)

    # Include t, so it applies more in the middle of the leaf
    x_mod_with_t = np.sin(t - np.pi * shift) * x_mod

    x_mod_positive = np.abs(x_mod_with_t) * wave_amt

    # Parametric equations for a leaf shape
    x = tubbiness * (((np.sin(t) * np.sin(t))) + x_mod_positive)
    y = np.cos(t)

    # Plot the leaf outline (both sides)
    plt.plot(x, y, color='green')
    plt.plot(-x, y, color='green')

    #plt.plot(t, x_mod_with_t, color='blue')

    plt.gca().set_aspect('equal')

    # Show the leaf plot
    plt.show()

plot_leaf()




# The parametrized function to be plotted
def f(t, amplitude, frequency):
    return amplitude * np.sin(2 * np.pi * frequency * t)

t = np.linspace(0, 1, 1000)

# Define initial parameters
init_amplitude = 5
init_frequency = 3

# Create the figure and the line that we will manipulate
fig, ax = plt.subplots()
line, = ax.plot(t, f(t, init_amplitude, init_frequency), lw=2)
ax.set_xlabel('Time [s]')

# adjust the main plot to make room for the sliders
fig.subplots_adjust(left=0.25, bottom=0.25)

# Make a horizontal slider to control the frequency.
axfreq = fig.add_axes([0.25, 0.1, 0.65, 0.03])
freq_slider = Slider(
    ax=axfreq,
    label='Frequency [Hz]',
    valmin=0.1,
    valmax=30,
    valinit=init_frequency,
)

# Make a vertically oriented slider to control the amplitude
axamp = fig.add_axes([0.1, 0.25, 0.0225, 0.63])
amp_slider = Slider(
    ax=axamp,
    label="Amplitude",
    valmin=0,
    valmax=10,
    valinit=init_amplitude,
    orientation="vertical"
)


# The function to be called anytime a slider's value changes
def update(val):
    line.set_ydata(f(t, amp_slider.val, freq_slider.val))
    fig.canvas.draw_idle()


# register the update function with each slider
freq_slider.on_changed(update)
amp_slider.on_changed(update)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
resetax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')


def reset(event):
    freq_slider.reset()
    amp_slider.reset()
button.on_clicked(reset)

plt.show()