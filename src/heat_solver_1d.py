import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ant

LENGTH = 10 - 1
DX = 0.01
N = int(LENGTH / DX)
TOTAL_TIME = 100
TEMPERATURE_START = 100
TEMPERATURE_BEGIN = 0
TEMPERATURE_END = 0


def create_difference_matrix():
    # Creates a temporary array of ones
    temp_array = np.ones(N)

    # Sets the matrix diagonal to -2
    matrix = -2 * np.diag(temp_array)

    # Concludes the final [1, -2, 1] pattern in the matrix
    matrix += np.diag(temp_array[:-1], 1) + np.diag(temp_array[:-1], -1)

    return matrix / DX**2


def create_first_vector():
    # Creates the vector with constant temperature
    vector = TEMPERATURE_START * np.ones(N)

    return vector


def prepare_solution(diff_matrix, first_vector):
    # Self descriptive: finds the eigenvalues and eigenvectors
    eigenvalues, eigenvectors = np.linalg.eig(diff_matrix)

    # Prepares the constants [S^(-1) * x]
    constants = np.dot(np.linalg.inv(eigenvectors), first_vector)

    return eigenvalues, eigenvectors, constants


def find_solution(eigenvalues, eigenvectors, constants, time):
    # The e's with eigenvalue * time in the exponent
    flow = np.exp(eigenvalues) ** time

    # Calculates output state de facto
    output_vector = np.dot(eigenvectors, flow * constants)

    return output_vector


def generate_solutions(diff_matrix, first_vector, dt):
    # Creates all the necessary vectors
    eigenvalues, eigenvectors, constants = prepare_solution(diff_matrix, first_vector)

    # Creates an empty matrix
    output_matrix = np.empty((N + 2, 0))

    # Loops trough all time intervals
    for time in np.arange(0, TOTAL_TIME + dt, dt):
        output_vector = find_solution(eigenvalues, eigenvectors, constants, time)

        # Just adds the start and the end parts that have 0 °C
        output_vector = np.append(TEMPERATURE_BEGIN, output_vector)
        output_vector = np.append(output_vector, TEMPERATURE_END)
        
        # Save it in a matrix
        output_matrix = np.hstack((output_matrix, output_vector[:, None]))

    return output_matrix


def generate_image(matrix):
    # Prepares the plotting
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.set_title("Heat equation", fontsize=15)
    ax.set_ylabel("Temperature °C", fontsize=14)
    ax.set_xlabel("X axis", fontsize=14)
    
    ax.set(xlim=[0, LENGTH], ylim=[0, TEMPERATURE_START + 20])

    # Creates the X axis ticks
    x_vector = np.arange(0, LENGTH + 2 * DX, DX)

    # Plot it through every matrix column
    for time in range(matrix.shape[1]):
        ax.plot(x_vector, matrix[:, time], color="teal")

    # Saves and show it
    fig.savefig("..\img\heat_1d_image.png")
    plt.show()


def generate_gif(matrix):
    # Prepares the plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    line, = ax.plot([], [], lw=2)

    ax.set_title("Heat equation", fontsize=15)
    ax.set_ylabel("Temperature °C", fontsize=14)
    ax.set_xlabel("X axis", fontsize=14)
    
    ax.set(xlim=[0, LENGTH], ylim=[0, TEMPERATURE_START + 20])

    # Creates the X axis ticks
    x_vector = np.arange(0, LENGTH + 2 * DX, DX)

    # Creates the text to account for time
    time_template = "time = %.1f s"
    time_text = ax.text(LENGTH / 20, TEMPERATURE_START + 10, "", transform=ax.transAxes)

    dt = TOTAL_TIME / matrix.shape[1]

    # Function to update the graph plot, used in the animation
    def animate(k):
        line.set_data((x_vector, matrix[:, k]))
        time_text.set_text(time_template % (k * dt))

        return line, time_text

    # Generates the gif
    animation = ant.FuncAnimation(fig, animate, matrix.shape[1], interval=20)
    writer = ant.PillowWriter(fps=25)

    # Saves it
    animation.save('..\img\heat_1d_gif.gif', writer=writer)  
    plt.close()


if __name__ == "__main__":
    D = create_difference_matrix()
    u = create_first_vector()
    
    out = generate_solutions(D, u, 5)
    generate_image(out)
    out = generate_solutions(D, u, 0.1)
    generate_gif(out)
