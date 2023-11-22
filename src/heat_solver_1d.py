import numpy as np

from heat_constants import *
from heat_plots import *


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
        vector *= TEMPERATURE_START / 2
    elif case == "random":
        vector = np.random.randint(0, TEMPERATURE_START, N)
    elif case == "linear":
        vector = np.linspace(0, 100, N)
    else:
        vector = TEMPERATURE_START * np.ones(N)
    
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

    # Will be used only to lessen future calculations
    temp_flow = np.exp(eigenvalues) ** 0

    # Yields the first vector, as it won't apper in the loop
    yield np.dot(eigenvectors, temp_flow * constants)

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
    output_matrix = np.empty((N, 0))

    # Loops trough all vectors
    for output_vector in find_solution(eigenvalues, eigenvectors, constants, dt):
        # Save it in a matrix
        output_matrix = np.hstack((output_matrix, output_vector[:, None]))

    return output_matrix


if __name__ == "__main__":
    # Creates differences matrix and starting vector
    D = create_difference_matrix()
    u = create_first_vector()
    
    # Generates the image with dt of 5s
    out = generate_solutions(D, u, 5)
    generate_image(out)

    # Generates the gif with dt of 0.1s
    out = generate_solutions(D, u, 0.1)
    generate_gif(out)
