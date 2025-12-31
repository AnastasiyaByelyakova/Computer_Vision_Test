# High-Performance Image Polygon Colorizer

This project provides a Python script that processes an image based on a corresponding black and white mask. For each polygon defined in the mask, the script calculates the most frequent color within that polygon's area in the original image and fills the polygon with that color in a new output image.


## Prerequisites

-   Python 3.11+
-   Poetry
-   A C++ compiler (e.g., `g++` on Linux, required for building the Cython extension)

## Setup

1.  **Clone the repository:**
    ```sh
    git clone <your-repo-url>
    cd <your-repo-directory>
    ```

2.  **Install dependencies using Poetry:**
    This command will create a virtual environment and install all necessary packages, including `Cython` and `setuptools`.
    ```sh
    poetry install
    ```

3.  **Compile the Cython Module:**
    This is a crucial one-time step. This command finds the `color_processor_cython.pyx` file, translates it to C++, and compiles it into a native extension module (`.so` on Linux) that your main script can import.
    ```sh
    poetry run python setup.py build_ext --inplace
    ```

## Usage

After compiling the module, you can run the main script. It will automatically import and use the ultra-fast compiled function.

```sh
poetry run python overlay_images.py
```

### Output

The script will generate the output file in the project directory - `processed_image.png`, where each polygon is filled with its most frequent color.

The script will also print the execution time and peak memory usage of the main processing function to the console.

```bash
Execution took 0.2261 seconds
Peak memory usage of 'wrapper': 211.20 MiB
```