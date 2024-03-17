# Random Shape Augmentation

## Overview

This project facilitates the generation of augmented datasets for computer vision tasks. The project offers a versatile solution for creating diverse datasets with a random distribution of input shapes. By incorporating random rotation, scaling and positioning of shapes within specified output dimensions, the script generates augmented images suitable for various computer vision application, such as object detection and classification.

The key features include:

- **Randomization**: Shapes are randomly rotated, scaled and distributed within the output images, providing diversity in the augmented dataset.
  
- **Avoidance of Overlapping Shapes**: The script ensures that generated shapes do not overlap with each other.

- **Flexibility**: Users can specify the dimensions of the output images and the number of images to be generated, allowing customization according to specific requirements.

## Requirements

- Python 3.x
- Pillow (PIL) library

## Installation

1. Clone the repository or download the source code to your local machine.

    ```
    git clone git@github.com:iamamistake/random-shape-augmentation.git
    ```

2. Install the required dependencies using the following command:

    ```
    pip install pillow
    ```

## Usage

1. Prepare your input shape images and place them in a directory.

2. Run the script `random_shape_augmentation.py` with the required command line arguments:

    ```
    python random_shape_augmentation.py --input <input_directory> --out-dims <width> <height> --nout <num_images> --output <output_directory>
    ```

    Replace `<input_directory>` with the path to the directory containing the input shape images. Specify the desired output dimensions `<width>` and `<height>` for the generated images. Set `<num_images>` to the number of output images you want to generate. Finally, provide the path to the output directory `<output_directory>` where the generated images will be saved.

3. After execution, the script will generate the specified number of output images with randomly distributed shapes and save them to the output directory.

    ### Example

    Generate 1000 augmented images with shapes distributed within 1024 x 1024 pixel output images:
    ```
    python random_shape_augmentation.py --input input_shapes --out-dims 1024 1024 --nout 1000 --output output_images
    ```