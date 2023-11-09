import numpy as np
import matplotlib.pyplot as plt

LENGTH = 10
TEMPERATURE_START = 100
TOTAL_TIME = 10


def create_difference_matrix():
    # Creates a temporary array of ones
    temp_array = np.ones(LENGTH)

    # Sets the matrix diagonal to -2
    matrix = -2 * np.diag(temp_array)

    # Concludes the final [1, -2, 1] pattern in the matrix
    matrix += np.diag(temp_array[:-1], 1) + np.diag(temp_array[:-1], -1)

    return matrix


def create_first_vector():
    # Creates the vector with constant temperature
    vector = TEMPERATURE_START * np.ones(LENGTH)

    return vector


def find_solution(diff_matrix, first_vector, time):
    # Self descriptive: finds the eigenvalues and eigenvectors
    eigenvalues, eigenvectors = np.linalg.eig(diff_matrix)

    # Prepares the constants [S^(-1) * x]
    constants = np.dot(np.linalg.inv(eigenvectors), first_vector)

    # The e's with eigenvalue * time in the exponent
    flow = np.exp(eigenvalues) ** time

    # Calculates output state de facto
    output_vector = np.dot(eigenvectors, flow * constants)

    return output_vector


def plot_image(vector):
    # Prepares the plotting
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.set_title("Heat equation", fontsize=15)
    ax.set_ylabel("Temperature °C", fontsize=14)
    ax.set_xlabel("X axis", fontsize=14)
    
    ax.set(xlim=[0, LENGTH + 1], ylim=[0, TEMPERATURE_START + 20])

    # Just adds the start and the end parts that have 0 °C
    buff = np.append(0, vector)
    buff = np.append(buff, 0)

    # Plot it
    ax.plot(buff)

    # Saves and show it
    fig.savefig("heat_diff.png")
    plt.show()


if __name__ == "__main__":
    D = create_difference_matrix()
    u = create_first_vector()
    
    out = find_solution(D, u, 0)
    plot_image(out)
