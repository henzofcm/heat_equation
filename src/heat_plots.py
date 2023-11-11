import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ant

from heat_constants import *


def generate_image(matrix, path="..\img\heat_1d_image.png"):
    # Prepares the plotting
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.set_title("Heat equation", fontsize=15)
    ax.set_ylabel("Temperature °C", fontsize=14)
    ax.set_xlabel("X axis", fontsize=14)
    
    # Arbitrary parameters for the axis limits
    y_max = max(TEMPERATURE_START, TEMPERATURE_BEGIN, TEMPERATURE_END)
    y_min = min(TEMPERATURE_START, TEMPERATURE_BEGIN, TEMPERATURE_END)
    
    ax.set(xlim=[0, LENGTH], ylim=[y_min, y_max + 20])

    # Creates the X axis ticks
    x_vector = np.arange(0, LENGTH + 2 * DX, DX)

    # Plot it through every matrix column
    for time in range(matrix.shape[1]):
        ax.plot(x_vector, matrix[:, time], color="teal")

    # Saves it
    fig.savefig(path)


def generate_gif(matrix, path="..\img\heat_1d_animation.gif"):
    # Prepares the plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    line, = ax.plot([], [], lw=2)

    ax.set_title("Heat equation", fontsize=15)
    ax.set_ylabel("Temperature °C", fontsize=14)
    ax.set_xlabel("X axis", fontsize=14)
    
    # Arbitrary parameters for the axis limits
    y_max = max(TEMPERATURE_START, TEMPERATURE_BEGIN, TEMPERATURE_END)
    y_min = min(TEMPERATURE_START, TEMPERATURE_BEGIN, TEMPERATURE_END)
    
    ax.set(xlim=[0, LENGTH], ylim=[y_min, y_max + 20])

    # Creates the X axis ticks
    x_vector = np.arange(0, LENGTH + 2 * DX, DX)

    # Creates the text to account for time
    time_template = "time = %.1f s"
    time_text = ax.text(LENGTH / 2, TEMPERATURE_START + 10, "", horizontalalignment="center")

    dt = TOTAL_TIME / matrix.shape[1]

    # Function to update the graph plot, used in the animation
    def animate(frame):
        line.set_data((x_vector, matrix[:, frame]))
        time_text.set_text(time_template % (frame * dt))

        return line, time_text

    # Generates the gif
    animation = ant.FuncAnimation(fig, animate, frames=matrix.shape[1], interval=200)
    writer = ant.PillowWriter(fps=25)

    # Saves it
    animation.save(path, writer=writer)
    plt.close()
