import numpy as np
import scipy.linalg as lin

from heat_constants import *
from heat_plots import *


def create_difference_matrix():
    # Creates the [1, -4, 1] matrix
    D  = -4 * np.eye(N_2D)
    D += np.diag([1] * (N_2D - 1), 1) + np.diag([1] * (N_2D - 1), -1)

    # Sets D to be the diagonal of the output matrix
    diags = [D] * (N_2D)
    matrix  = lin.block_diag(*diags)

    # Adds the I's to the desired matrix
    I = np.ones((N_2D) * (N_2D - 1))
    matrix += np.diag(I, N_2D) + np.diag(I, -N_2D)

    return matrix * (ALPHA / DX_2D ** 2)


def create_vector(case="constant"):
    # Creates the vector according to case
    if case == "sin":
        vector = np.arange(0, LENGTH_2D**2, DX_2D**2)
        vector *= vector
        vector = (np.sin(vector) + 1) * TEMPERATURE_START
    elif case == "linear":
        vector = np.linspace(0, TEMPERATURE_START, N_2D**2)
    else:
        vector = TEMPERATURE_START * np.ones(N_2D**2)

    return vector


def find_solution(diff_matrix, vector):
    # Finds the eigenvalues and eigenvectors
    eigenvalues, eigenvectors = np.linalg.eig(diff_matrix)

    # Prepares the constants
    constants = np.dot(np.linalg.inv(eigenvectors), vector)

    # The e's with eigenvalue * dt in the exponent
    flow = np.exp(eigenvalues) ** DT_2D
    temp_flow = np.exp(eigenvalues) ** 0

    # Creates the matrix that holds all times
    temperature = np.empty((NUMBER_OF_STEPS_2D + 1, N_2D**2))
    temperature[0] = vector

    # Loops through all the dt's
    for step in range(1, NUMBER_OF_STEPS_2D + 1):
        temp_flow *= flow
        temperature[step] = eigenvectors @ np.diag(temp_flow) @ constants

    # Returns it reshaped
    temperature = np.reshape(temperature, (NUMBER_OF_STEPS_2D + 1, N_2D, N_2D))
    return temperature


if __name__ == "__main__":
    # Creates differences matrix and starting vector
    D = create_difference_matrix()
    u = create_vector()
    
    # Generates the final 2D image
    temperature = find_solution(D, u)
    generate_gif_2d(temperature)
    generate_gif_surface(temperature)
