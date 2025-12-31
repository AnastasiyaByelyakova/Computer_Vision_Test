import cv2
import numpy as np
import time
from memory_profiler import memory_usage

# Import the newly compiled Cython module
import color_processor_cython
from decorators import time_it, memory_it

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
    image_path1 = 'color_mask.png'
    mask_path = 'mask.png'
    processed_output_path = 'processed_image.png'

    base_image = read_image(image_path1)
    mask_image = read_image(mask_path)

    if base_image is not None and mask_image is not None:
        overlaid_image = apply_mask_overlay(base_image, mask_image)

        # Use the Cython implementation
        processed_image = process_polygons_cython_wrapper(base_image, mask_image)
        if processed_image is not None:
            cv2.imwrite(processed_output_path, processed_image)
            print(f"Processed image saved to {processed_output_path}")
