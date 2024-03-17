import argparse
import random
import os
import math
from PIL import Image

def parse_user_input_arguments():
    parser = argparse.ArgumentParser(prog = "Random Shape Augmentation",
                                     description = "Generate augmented dataset with random distribution of input shapes")

    parser.add_argument("--input", type = str, required = True, help = "Input directory containing the shape images")
    parser.add_argument("--out-dims", type = int, nargs = 2, required = True, help= "Dimensions of the output images (W x H)")
    parser.add_argument("--nout", type = int, required = True, help = "Number of output images to be generated")
    parser.add_argument("--output", type = str, required = True, help = "Output directory to save generated images")
    return parser.parse_args()

def get_max_iterations_per_shape(background_size, input_shape_size, total_input_shapes_num):
    return (((math.ceil((background_size // ((2 ** 0.5) * input_shape_size))/2)) ** 2) // total_input_shapes_num)

def get_random_shape_coordinates(background, shape, occupied_coordinates):
    shape_width, shape_height = shape.size
    background_width, background_height = background.size

    while True:
        shape_random_x = random.randint(0, (background_width - 1) - shape_width)
        shape_random_y = random.randint(0, (background_height - 1) - shape_height)

        if not any(shape_random_x <= occupied_shape_x + occupied_shape_width and shape_random_x + shape_width >= occupied_shape_x and
                   shape_random_y <= occupied_shape_y + occupied_shape_height and shape_random_y + shape_height >= occupied_shape_y
                   for occupied_shape_x, occupied_shape_y, occupied_shape_width, occupied_shape_height in occupied_coordinates):
            break

    occupied_coordinates.append((shape_random_x, shape_random_y, shape_width, shape_height))
    return (shape_random_x, shape_random_y)

def main():
    input_args = parse_user_input_arguments()

    INPUT_SHAPES_DIR = input_args.input
    OUTPUT_DIMENSIONS = tuple(input_args.out_dims)
    TOTAL_OUTPUT_IMAGES_NUM = input_args.nout
    OUTPUT_IMAGES_DIR = input_args.output
    
    INPUT_SHAPES = [os.path.join(INPUT_SHAPES_DIR, image) for image in os.listdir(INPUT_SHAPES_DIR)]
    TOTAL_INPUT_SHAPES_NUM = len(INPUT_SHAPES)

    MAX_INPUT_SHAPE_SIZE = max(max(Image.open(shape).size) for shape in INPUT_SHAPES)
    MIN_BACKGROUND_SIZE = min(OUTPUT_DIMENSIONS)
    MAX_ITERATIONS_PER_SHAPE = get_max_iterations_per_shape(MIN_BACKGROUND_SIZE, MAX_INPUT_SHAPE_SIZE, TOTAL_INPUT_SHAPES_NUM)

    if MAX_ITERATIONS_PER_SHAPE == 0:
        raise Exception("Unable to fit all input shapes within the output image dimensions (consider increasing the output image dimensions, reducing the number of input shapes or decreasing the input shape dimensions)")

    SHAPE_ROTATION_MIN_BOUND_DEG = 0
    SHAPE_ROTATION_MAX_BOUND_DEG = 90
    SHAPE_SCALING_FACTOR_MIN_BOUND = 0.75
    SHAPE_SCALING_FACTOR_MAX_BOUND = 1.0

    for output_images_num in range(TOTAL_OUTPUT_IMAGES_NUM):
        output_image = Image.new('RGB', OUTPUT_DIMENSIONS, (0, 0, 0))
        occupied_coordinates = []

        for shape in INPUT_SHAPES:
            shape = Image.open(shape)
            for _ in range(MAX_ITERATIONS_PER_SHAPE):
                rotated_shape = shape.rotate(random.randint(SHAPE_ROTATION_MIN_BOUND_DEG, SHAPE_ROTATION_MAX_BOUND_DEG), expand = True)
                scaling_factor = random.uniform(SHAPE_SCALING_FACTOR_MIN_BOUND, SHAPE_SCALING_FACTOR_MAX_BOUND)
                scaled_size = tuple(int(shape_dimensions * scaling_factor) for shape_dimensions in rotated_shape.size)
                scaled_shape = rotated_shape.resize(scaled_size)

                output_image.paste(scaled_shape, get_random_shape_coordinates(output_image, scaled_shape, occupied_coordinates))

        output_image.save(f"{OUTPUT_IMAGES_DIR}/{output_images_num}.jpg")

if __name__ == "__main__":
    main()