import numpy as np
import scipy.linalg as lin
import matplotlib.pyplot as plt


ALPHA = 1
LENGTH = 10
DX = 0.5
N = int(LENGTH / DX)
TEMPERATURE_START = 100


def create_difference_matrix():
    main_diag  = -4 * np.eye(N)
    upper_diag = np.diag([1] * (N - 1), 1)
    lower_diag = np.diag([1] * (N - 1), -1)

    block = main_diag + upper_diag + lower_diag
    diags = [block] * (N)
    matrix  = lin.block_diag(*diags)

    I = np.ones((N) * (N - 1))
    upper_I = np.diag(I, N)
    lower_I = np.diag(I, -N)
    
    matrix += upper_I + lower_I

    return matrix * (ALPHA / DX ** 2)


def create_vector():
    vector = TEMPERATURE_START * np.ones(N**2)

    return vector


def find_solution(diff_matrix, vector, time):
    eigenvalues, eigenvectors = np.linalg.eig(diff_matrix)

    constants = np.dot(np.linalg.inv(eigenvectors), vector)

    final_vector = eigenvectors @ (np.diag(np.exp(eigenvalues) ** time)) @ constants

    return final_vector 


def plot_heatmap(vector):
    grid = vector.reshape(N, N)

    plt.clf()

    plt.pcolormesh(grid, cmap=plt.cm.jet, vmin=0, vmax=100)
    plt.colorbar()

    plt.show()


if __name__ == "__main__":
    D = create_difference_matrix()
    u = create_vector()
    
    temperature = find_solution(D, u, 5)

    plot_heatmap(temperature)