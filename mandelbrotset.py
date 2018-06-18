import matplotlib.pyplot as plt
import numpy as np
import datetime
import math


def mandelbrotset(X, maxiter=100, horizon=2, zoom_point_x=0, zoom_point_y=0, zoom_factor=1):
    """
    The values of the Mandelbrot set will be calculated and written into the array X.
    """

    image_width = len(X[0])
    image_height = len(X)

    for r_pixel in range(image_width):  # real
        for i_pixel in range(image_height):  # imaginary

            comp = complex_number_from_pixels(image_width, image_height, zoom_point_x, zoom_point_y, zoom_factor,
                                              r_pixel, i_pixel)

            X[i_pixel][r_pixel] = color_code(comp, 0, maxiter, horizon)


def julia_set(X, complex_x, complex_y, maxiter=100, horizon=2, zoom_point_x=0, zoom_point_y=0, zoom_factor=1):
    """
    The values of the Julia set will be calculated and written into the array X.
    """

    image_width = len(X[0])
    image_height = len(X)

    for r_pixel in range(image_width):  # real
        for i_pixel in range(image_height):  # imaginary

            comp = complex(
                complex_x,
                complex_y
            )

            start_number = complex_number_from_pixels(image_width, image_height, zoom_point_x, zoom_point_y,
                                                      zoom_factor, r_pixel, i_pixel)

            X[i_pixel][r_pixel] = color_code(comp, start_number, maxiter, horizon)


def complex_number_from_pixels(array_width, array_height, zoom_point_x, zoom_point_y, zoom_factor, x, y):
    """
    :param array_width: width of the array
    :param array_height: height of the array
    :param zoom_point_x: the x-value of the point to which the image will be zoomed into
    :param zoom_point_y: the y-value of the point to which the image will be zoomed into
    :param zoom_factor: factor to scale the picture, if zoom_factor=1 there will be no change in size
    :param x: the current x-value of the array
    :param y: the current y-value of the array
    :return: complex number of the place in the coorinate system
    """

    # making displayed fractal size smaller, scaling the fractal size
    # 4 is the normal fractal size (with zoom_factor=0) because
    # it ranges from -2 to 2
    fractal_width = 4 * (1 / zoom_factor)
    fractal_height = 4 * (1 / zoom_factor)

    x_min = zoom_point_x - fractal_width / 2
    x_max = zoom_point_x + fractal_width / 2

    y_min = zoom_point_y - fractal_height / 2
    y_max = zoom_point_y + fractal_height / 2

    return complex(
        linear_function(0, array_width, x_min, x_max, x),  # real value
        linear_function(0, array_height, y_min, y_max, y)  # imaginary value
    )


def linear_function(x_min, x_max, y_min, y_max, x):
    """
    Represents a regular linear function specified for the purpose of calculating
    a coordinate value from the index number of the array.

    :param x_min: minimal x-value that needs to be calculated
    :param x_max: maximal x-value that needs to be calculated
    :param y_min: minimal y-value that gets returned if the minimal x-value gets entered
    :param y_max: maximal y-value that gets returned if the maximal x-value gets entered
    :param x: the current x-value
    :return: regular linear function value of the type y=mx+n
    """
    return ((y_max - y_min) / (x_max - x_min)) * x + y_min


def f(c, z):
    """
    Function which specifies the Mandelbrot set / Julia set
    Returns complex number
    """
    return z**2 + c


def escape_count(comp, start_value, maxiter, horizon):
    """
    Counts the steps until the function diverges (becomes greater than the horizon).

    :param comp: complex number
    :param start_value: starting value from where the iteration begins, eeded for the Julia set
    :param maxiter: number of iterations after which the calculation ends
    :param horizon: determines when the function blows up
    :return: number of iterations needed to blow up and the value when it blows up, or if the
    function converges the maximum number of iterations and 0
    """

    value = start_value
    for i in range(maxiter):
        value = f(comp, value)
        if abs(value) > horizon:
            return i, abs(value)
    return maxiter, 0


def color_code(complex, start_value, maxiter, horizon):
    """
    Using the escape_count to calculate a smooth shading for the exterior
    of the Fractal.
    Formular from https://linas.org/art-gallery/escape/smooth.html

    Returns a float value raging from 0 to maxiter.
    """

    iterations, escape_value = escape_count(complex, start_value, maxiter, horizon)
    if escape_value > 0:
        return iterations + 1 - math.log10(math.log10(escape_value)) / math.log10(2)
    else:
        return maxiter


def arr(size):
    """
    Returning a 1:1 two dimensional empty array where later the fractal
    values will be written in
    """
    return np.zeros([size, size])  # [image_height, image_width]


def make_image(X):
    """
    Creating an image out of the array with the fractal values.
    The image name will be the current time, and it will be saved in the folder /images.
    """
    plt.axis('off')
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    plt.imsave("images/%s.png" % time, X, cmap='magma')


if __name__ == '__main__':

    image_size = 1920

    # uncomment either the mandelbrot set or the julia set, depending on what you want

    # mandelbrotset
    M = arr(image_size)
    mandelbrotset(M)
    make_image(M)

    # julia set
    real_value = -0.8
    imaginary_value = 0.156
    J = arr(image_size)
    julia_set(J, real_value, imaginary_value, zoom_factor=1.3, maxiter=200, horizon=3)
    make_image(J)

