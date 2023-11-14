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


def generate_image_by_time(matrix, path="..\img\heat_1d_image_alternative.png"):
    # Prepares the plotting
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.set_title("Specific points through time", fontsize=15)
    ax.set_ylabel("Temperature °C", fontsize=14)
    ax.set_xlabel("Time", fontsize=14)
    
    # Arbitrary parameters for the axis limits
    y_max = max(TEMPERATURE_START, TEMPERATURE_BEGIN, TEMPERATURE_END)
    y_min = min(TEMPERATURE_START, TEMPERATURE_BEGIN, TEMPERATURE_END)
    
    ax.set(xlim=[0, TOTAL_TIME], ylim=[y_min, y_max + 20])

    # Creates the X axis ticks based on time
    x_vector = np.linspace(0, TOTAL_TIME + 0.01, matrix.shape[1])

    # Plot it through every matrix column
    for point in range(matrix.shape[0]):
        ax.plot(x_vector, matrix[point, :], color="coral")

    # Saves it
    fig.savefig(path)    


def generate_image_surface(matrix, path="..\img\heat_1d_image_surface.png"):
    # Prepares the plotting
    fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={"projection": "3d"})

    ax.set_title("Heat equation", fontsize=15)
    ax.set_zlabel("Temperature °C", fontsize=14)
    ax.set_ylabel("X axis", fontsize=14)
    ax.set_xlabel("Time", fontsize=14)
    
    # Arbitrary parameters for the axis limits
    z_max = max(TEMPERATURE_START, TEMPERATURE_BEGIN, TEMPERATURE_END)
    z_min = min(TEMPERATURE_START, TEMPERATURE_BEGIN, TEMPERATURE_END)
    
    ax.set(xlim=[0, TOTAL_TIME], ylim=[0, LENGTH], zlim=[z_min, z_max + 20])

    # Creates the X axis and TIME axis ticks
    x_vector = np.linspace(0, TOTAL_TIME, matrix.shape[1])
    y_vector = np.arange(0, LENGTH, DX)

    x_vector, y_vector = np.meshgrid(x_vector, y_vector)

    # Plot it through every matrix column
    surface = ax.plot_surface(x_vector, y_vector, matrix, cmap="inferno")
    plt.colorbar(surface, shrink=0.25, aspect=5)

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
    x_vector = np.arange(0, LENGTH, DX)

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


def plot_heatmap_2d(grid, time):
    # Cleans the figure and sets the title
    plt.clf()
    plt.title(f"Temperature at t = {time:.2f}")

    # Plots it
    fig, = plt.pcolormesh(grid, cmap=plt.cm.jet, vmin=0, vmax=100)
    plt.colorbar()

    return fig


def generate_gif_2d(temperature, path="..\img\heat_2d_animation.gif"):
    # The update function used in the animation
    def animate(frame):
        plot_heatmap_2d(temperature[frame], frame * DT_2D)
    
    # Does magic
    animation = ant.FuncAnimation(plt.figure(), animate, interval=1, frames=NUMBER_OF_STEPS_2D, repeat=False)

    # Save
    animation.save(path)


def generate_gif_surface(matrix, path="..\img\heat_2d_animation_surface.gif"):
    # Prepares the plotting
    fig, ax = plt.subplots(figsize=(10, 6),  subplot_kw={"projection": "3d"})

    ax.set_title("Heat equation", fontsize=15)
    ax.set_zlabel("Temperature °C", fontsize=14)
    ax.set_ylabel("Y axis", fontsize=14)
    ax.set_xlabel("X axis", fontsize=14)
    
    # Arbitrary parameters for the axis limits
    z_max = max(TEMPERATURE_START, TEMPERATURE_BEGIN, TEMPERATURE_END)
    z_min = min(TEMPERATURE_START, TEMPERATURE_BEGIN, TEMPERATURE_END)
    
    ax.set(xlim=[0, LENGTH_2D], ylim=[0, LENGTH_2D], zlim=[z_min, z_max + 20])

    # Creates the X and Y axis ticks
    x_vector = np.arange(0, LENGTH_2D, DX_2D)
    y_vector = np.arange(0, LENGTH_2D, DX_2D)

    x_vector, y_vector = np.meshgrid(x_vector, y_vector)

    # Creates the text to account for time
    time_template = "time = %.1f s"
    time_text = ax.text2D(0.05, 0.95, "", transform=ax.transAxes)

    # Function to update the graph plot, used in the animation
    def animate(frame):
        # Cleans the axis
        ax.cla()
        ax.set_zlim(z_min, z_max + 20)

        # Plot it through every matrix column
        surface = ax.plot_surface(x_vector, y_vector, matrix[frame], cmap="inferno", vmin=z_min, vmax=z_max)
        time_text.set_text(time_template % (frame * DT_2D))

        return surface, time_text

    # Generates the gif
    animation = ant.FuncAnimation(fig, animate, frames=matrix.shape[0], interval=300)
    writer = ant.PillowWriter(fps=25)

    # Saves it
    animation.save(path, writer=writer)
    plt.close()
