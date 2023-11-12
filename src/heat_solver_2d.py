import numpy as np
import scipy.linalg as lin

from heat_constants import *
from heat_plots import *


def create_difference_matrix():
    main_diag  = -4 * np.eye(N_2D)
    upper_diag = np.diag([1] * (N_2D - 1), 1)
    lower_diag = np.diag([1] * (N_2D - 1), -1)

    block = main_diag + upper_diag + lower_diag
    diags = [block] * (N_2D)
    matrix  = lin.block_diag(*diags)

    I = np.ones((N_2D) * (N_2D - 1))
    upper_I = np.diag(I, N_2D)
    lower_I = np.diag(I, -N_2D)
    
    matrix += upper_I + lower_I

    return matrix * (ALPHA / DX_2D ** 2)


def create_vector():
    vector = TEMPERATURE_START * np.ones(N_2D**2)

    return vector


def find_solution(diff_matrix, vector):
    eigenvalues, eigenvectors = np.linalg.eig(diff_matrix)

    constants = np.dot(np.linalg.inv(eigenvectors), vector)

    flow = np.exp(eigenvalues) ** DT_2D

    temp_flow = np.exp(eigenvalues) ** 0

    temperature = np.empty((NUMBER_OF_STEPS_2D+1, N_2D**2))
    temperature[0] = vector

    for step in range(1, NUMBER_OF_STEPS_2D+1):
        temp_flow *= flow
        temperature[step] = eigenvectors @ np.diag(temp_flow) @ constants

    return temperature


if __name__ == "__main__":
    D = create_difference_matrix()
    u = create_vector()
    
    temperature = find_solution(D, u)

    generate_gif_2d(temperature)