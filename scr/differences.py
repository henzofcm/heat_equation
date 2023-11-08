import numpy as np
import matplotlib as mpl

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

    # Prepares the output vector, the constants used and the e's
    output_vector = np.zeros(LENGTH)
    constants = np.dot(np.linalg.inv(eigenvectors), first_vector)
    flow = np.exp(eigenvalues) ** time

    # Calculates each output state de facto
    output_vector = np.dot(eigenvectors, flow * constants)

    return output_vector


def plot_image():
    pass


if __name__ == "__main__":
    D = create_difference_matrix()
    u = create_first_vector()
    
    out = find_solution(D, u, 3)
    print(out)
