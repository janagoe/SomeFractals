import argparse
from mandelbrotset import mandelbrotset, julia_set

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('fractal', choices=['mandelbrot', 'julia'],
                        help="the type of fractal you want")

    parser.add_argument('-is', '--image_size', help="the size in pixels the producted image will be",
                        type=int, default=640)
    parser.add_argument('-in', '--image_name', help="the name of the output image", default='')

    parser.add_argument('-m', '--maxiter', help="the maximal number of iterations",
                        type=int, default=100)
    parser.add_argument('-ho', '--horizon', help="the horizon of the fractal",
                        type=int, default=2)

    parser.add_argument('-zx', '--zoom_point_x',
                        help="the x point where the fractal will be zoomed into",
                        type=float, default=0)
    parser.add_argument('-zy', '--zoom_point_y',
                        help="the y point where the fractal will be zoomed into",
                        type=float, default=0)
    parser.add_argument('-zf', '--zoom_factor',
                        help="how much the fractal will be zoomed into",
                        type=float, default=1)

    parser.add_argument('-rv', '--real_value',
                        help="only needed for the julia set, coordinate on real plane",
                        type=float, default=-0.8)
    parser.add_argument('-iv', '--imaginary_value',
                        help="only needed for the julia set, coorindate on imaginary plane",
                        type=float, default=0.156)

    args = parser.parse_args()

    if args.fractal == 'mandelbrot':
        mandelbrotset(args.image_size, args.image_name,
                      args.maxiter,
                      args.horizon,
                      args.zoom_point_x, args.zoom_point_y,
                      args.zoom_factor)
    elif args.fractal == 'julia':
        julia_set(args.image_size, args.image_name,
                  args.real_value, args.imaginary_value,
                  args.maxiter,
                  args.horizon,
                  args.zoom_point_x, args.zoom_point_y,
                  args.zoom_factor)
