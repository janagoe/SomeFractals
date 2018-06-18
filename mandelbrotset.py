import matplotlib.pyplot as plt
import numpy as np
import math
import datetime


def mandelbrotset(X, maxiter=100, horizon=2, zoom_point_x=0, zoom_point_y=0, zoom_factor=1):

    image_width = len(X[0])
    image_height = len(X)

    for r_pixel in range(image_width):  # real
        for i_pixel in range(image_height):  # imaginary

            comp = complex_number_from_pixels(image_width, image_height, zoom_point_x, zoom_point_y,
                                                      zoom_factor, r_pixel, i_pixel)

            X[i_pixel][r_pixel] = color_code(comp, 0, maxiter, horizon)


def julia_set(X, complex_x, complex_y, maxiter=100, horizon=2, zoom_point_x=0, zoom_point_y=0, zoom_factor=1):

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


def complex_number_from_pixels(image_width, image_height, zoom_point_x, zoom_point_y, zoom_factor, r_pixel, i_pixel):
    # 4 weil interval [-2,2] 4 lang ist
    fractal_width = 4 * (1 / zoom_factor)
    fractal_height = 4 * (1 / zoom_factor)

    x_min = zoom_point_x - fractal_width / 2
    x_max = zoom_point_x + fractal_width / 2

    y_min = zoom_point_y - fractal_height / 2
    y_max = zoom_point_y + fractal_height / 2

    return complex(
        coorinate(0, image_width, x_min, x_max, r_pixel),  # real
        coorinate(0, image_height, y_min, y_max, i_pixel)  # imaginary
    )


# lineare funktion mit den grenzen
# y = mx + n
def coorinate(pixel_min, pixel_max, value_min, value_max, pixel):
    return ((value_max-value_min) / (pixel_max-pixel_min)) * pixel + value_min


def f(comp, z):
    return z ** 2 + comp


def escape_count(comp, start_value, maxiter, horizon):
    value = start_value
    for i in range(maxiter):
        value = f(comp, value)
        if abs(value) > horizon:
            return i, abs(value)
    return maxiter, 0


def color_code(complex, start_value, maxiter, horizon):
    iterations, blow_up_value = escape_count(complex, start_value, maxiter, horizon)

    # smooth shading
    # https://linas.org/art-gallery/escape/smooth.html
    if blow_up_value > 0:
        return iterations + 1 - math.log10(math.log10(blow_up_value)) / math.log10(2)
    else:
        return maxiter


def arr(image_size):
    return np.zeros([image_size, image_size])  # [image_height, image_width]


def make_image(X):
    plt.axis('off')
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    plt.imsave("images/%s.png" % time, X, cmap='magma')


if __name__ == '__main__':

    image_size = 1920

    # mandelbrotset
    # M = arr(image_size)
    # mandelbrotset(M)
    # make_image(M)

    # julia set
    real_value = -0.8
    imaginary_value = 0.156
    J = arr(image_size)
    julia_set(J, real_value, imaginary_value, zoom_factor=1.3, maxiter=200, horizon=3)
    make_image(J)



