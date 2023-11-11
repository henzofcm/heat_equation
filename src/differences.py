import numpy as np
import matplotlib.pyplot as plt


def create_difference_matrix(number_of_points, alpha, time_step, point_step):
    # Creates a temporary array of ones
    temp_array = np.ones(number_of_points)

    param = alpha * time_step / (point_step ** 2)

    # Sets the tridiagonal matrix
    matrix = (1 - 2 * param) * np.diag(temp_array)
    matrix += param * (np.diag(temp_array[:-1], 1) + np.diag(temp_array[:-1], -1))

    # Modify matrix to keep temperature at endpoints 
    matrix[0,0] = 1
    matrix[0,1] = 0
    matrix[-1,-1] = 1
    matrix[-1,-2] = 0

    return matrix


def get_initial_temperature(points):
    # Creates the vector with initial temperature
    vector = np.sin(2 * np.pi * points)

    return vector


def find_solution(diff_matrix, initial_temperature, time, time_step):
    # Self descriptive: finds the eigenvalues and eigenvectors
    eigenvalues, eigenvectors = np.linalg.eig(diff_matrix)

    # Prepares the constants [S^(-1) * x]
    constants = np.linalg.inv(eigenvectors) @ initial_temperature

    # Eigenvalues matrix raised to number_of_steps
    number_of_steps = int(time / time_step)
    flow = np.linalg.matrix_power(np.diag(eigenvalues), number_of_steps)

    # Calculates output state de facto
    output_vector = eigenvectors @ flow @ constants

    return output_vector


def plot_image(points, temperature):
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.set(ylim=[-1,1])

    ax.set_title("Heat equation", fontsize=15)
    ax.set_ylabel("Temperature °C", fontsize=14)
    ax.set_xlabel("X axis", fontsize=14)
    
    ax.plot(points, temperature, color='blue')

    fig.savefig("heat_diff.png")
    plt.show()


if __name__ == "__main__":
    alpha = 0.1
    length = 1
    number_of_points = 21

    point_step = length / (number_of_points - 1)
    time_step = point_step ** 2 / (2 * alpha)

    points = np.linspace(0, length, number_of_points)

    D = create_difference_matrix(number_of_points, alpha, time_step, point_step)
    u = get_initial_temperature(points)
    
    final_temperature = find_solution(D, u, 5, time_step)
    plot_image(points, final_temperature)
