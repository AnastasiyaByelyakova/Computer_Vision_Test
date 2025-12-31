import cv2
import numpy as np
import time
from memory_profiler import memory_usage

# Import the newly compiled Cython module
import color_processor_cython

def time_it(func):
    """
    A decorator to measure the execution time of a function.
    """
    def wrapper(*args, **kwargs):
        print(f"Running '{func.__name__}'...")
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution took {end_time - start_time:.4f} seconds")
        return result
    return wrapper

def memory_it(func):
    """
    A decorator to measure the peak memory usage of a function.
    """
    def wrapper(*args, **kwargs):
        mem_usage, retval = memory_usage((func, args, kwargs), retval=True, max_usage=True)
        print(f"Peak memory usage of '{func.__name__}': {mem_usage:.2f} MiB")
        return retval
    return wrapper

def read_image(image_path):
    """Reads an image from a given path."""
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not read image from {image_path}")
    return img

def apply_mask_overlay(base_image, mask_image):
    """Applies a mask to a base image."""
    if base_image.shape != mask_image.shape:
        print("Error: Images must have the same size for overlaying.")
        return None
    if len(mask_image.shape) > 2:
        mask = cv2.cvtColor(mask_image, cv2.COLOR_BGR2GRAY)
    else:
        mask = mask_image
    return cv2.bitwise_and(base_image, base_image, mask=mask)

@memory_it
@time_it
def process_polygons_cython_wrapper(base_image, mask_image):
    """
    Wrapper function to call the high-performance Cython implementation.
    """
    if len(mask_image.shape) > 2:
        gray_mask = cv2.cvtColor(mask_image, cv2.COLOR_BGR2GRAY)
    else:
        gray_mask = mask_image

    _, thresh = cv2.threshold(gray_mask, 1, 255, cv2.THRESH_BINARY)
    num_labels, labels = cv2.connectedComponents(thresh)
    
    # Ensure labels are of type int for Cython function
    labels = labels.astype(np.int32)

    # Call the compiled C function
    return color_processor_cython.process_polygons_cython(base_image, labels, num_labels)


if __name__ == '__main__':
    image_path1 = '/media/cassie/DATA/test_task_CV3/color_mask.png'
    mask_path = '/media/cassie/DATA/test_task_CV3/mask.png'
    overlay_output_path = '/media/cassie/DATA/test_task_CV3/overlay.png'
    processed_output_path = '/media/cassie/DATA/test_task_CV3/processed_image.png'

    base_image = read_image(image_path1)
    mask_image = read_image(mask_path)

    if base_image is not None and mask_image is not None:
        overlaid_image = apply_mask_overlay(base_image, mask_image)
        if overlaid_image is not None:
            cv2.imwrite(overlay_output_path, overlaid_image)
            print(f"Overlay image saved to {overlay_output_path}")

        # Use the Cython implementation
        processed_image = process_polygons_cython_wrapper(base_image, mask_image)
        if processed_image is not None:
            cv2.imwrite(processed_output_path, processed_image)
            print(f"Processed image saved to {processed_output_path}")
