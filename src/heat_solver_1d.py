import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ant

LENGTH = 10
DX = 0.01
N = int(LENGTH / DX)

TOTAL_TIME = 100
TEMPERATURE_START = 100

ALPHA = 1
TEMPERATURE_BEGIN = 0
TEMPERATURE_END = 0


def create_difference_matrix(case="open"):
    # Creates a temporary array of ones
    temp_array = np.ones(N)

    # Sets the matrix diagonal to -2
    matrix = -2 * np.diag(temp_array)

    # Concludes the final [1, -2, 1] pattern in the matrix
    matrix += np.diag(temp_array[:-1], 1) + np.diag(temp_array[:-1], -1)

    if case == "closed":
        matrix[0, 0] = -1
        matrix[-1, -1] = -1

    return matrix * (ALPHA / DX ** 2)


def create_first_vector(case="constant"):
    # Creates the vector according to case
    if case == "sin":
        vector = np.sin(np.arange(0, LENGTH, DX)) + 1
        vector *= (TEMPERATURE_START / 2)
    elif case == "random":
        vector = np.random.randint(0, TEMPERATURE_START, LENGTH / DX)
    elif case == "linear":
        vector = np.linspace(0, 100, N)
        
    else:
        vector = TEMPERATURE_START * np.ones(N)
    
    print(vector)
    return vector


def prepare_solution(diff_matrix, first_vector):
    # Self descriptive: finds the eigenvalues and eigenvectors
    eigenvalues, eigenvectors = np.linalg.eig(diff_matrix)

    # Prepares the constants [S^(-1) * x]
    constants = np.dot(np.linalg.inv(eigenvectors), first_vector)

    return eigenvalues, eigenvectors, constants


def find_solution(eigenvalues, eigenvectors, constants, dt):
    # The e's with eigenvalue * dt in the exponent
    flow = np.exp(eigenvalues) ** dt

    # Will be used only to lessen calculations
    temp_flow = np.exp(eigenvalues) ** 0
    yield temp_flow

    # Loops through all time intervals, using the preceding temp_flow
    # Because of the great property [e^a * e^b = e^(a + b)]
    for time in np.arange(dt, TOTAL_TIME + dt, dt):
        temp_flow *= flow
        output_vector = np.dot(eigenvectors, temp_flow * constants)

        yield output_vector


def generate_solutions(diff_matrix, first_vector, dt):
    # Creates all the necessary vectors
    eigenvalues, eigenvectors, constants = prepare_solution(diff_matrix, first_vector)

    # Creates an empty matrix
    output_matrix = np.empty((N + 2, 0))

    # Loops trough all vectors
    for output_vector in find_solution(eigenvalues, eigenvectors, constants, dt):
        # Just adds the start and the end parts temperatures
        output_vector = np.append(TEMPERATURE_BEGIN, output_vector)
        output_vector = np.append(output_vector, TEMPERATURE_END)
        
        # Save it in a matrix
        output_matrix = np.hstack((output_matrix, output_vector[:, None]))

    return output_matrix


def generate_image(matrix, path="..\img\heat_1d_open.png"):
    # Prepares the plotting
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.set_title("Heat equation", fontsize=15)
    ax.set_ylabel("Temperature °C", fontsize=14)
    ax.set_xlabel("X axis", fontsize=14)
    
    # Arbitrary parameters for the axis limits
    ax.set(xlim=[0, LENGTH], ylim=[0, TEMPERATURE_START + 20])

    # Creates the X axis ticks
    x_vector = np.arange(0, LENGTH + 2 * DX, DX)

    # Plot it through every matrix column
    for time in range(matrix.shape[1]):
        ax.plot(x_vector, matrix[:, time], color="teal")

    # Saves and show it
    fig.savefig(path)
    plt.show()


def generate_gif(matrix, path="..\img\heat_1d_animation.gif"):
    # Prepares the plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    line, = ax.plot([], [], lw=2)

    ax.set_title("Heat equation", fontsize=15)
    ax.set_ylabel("Temperature °C", fontsize=14)
    ax.set_xlabel("X axis", fontsize=14)
    
    # Arbitrary parameters for the axis limits
    ax.set(xlim=[0, LENGTH], ylim=[TEMPERATURE_END, max(TEMPERATURE_START, TEMPERATURE_BEGIN) + 20])

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


if __name__ == "__main__":
    D = create_difference_matrix("closed")
    u = create_first_vector("linear")
    
    # Generates the image with dt of 5s
    out = generate_solutions(D, u, 2)
    generate_image(out, "..\img\heat_1d_image_BC.png")

    # Generates the gif with dt of 0.1s
    out = generate_solutions(D, u, 0.1)
    generate_gif(out, "..\img\heat_1d_animation_BC.gif")
