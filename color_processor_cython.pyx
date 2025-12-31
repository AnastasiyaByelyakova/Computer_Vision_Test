# distutils: language = c++

cimport numpy as np
from libcpp.vector cimport vector
from libcpp.unordered_map cimport unordered_map
# Import standard, single-token integer types
from libc.stdint cimport uint32_t, int64_t

import numpy as np

cpdef process_polygons_cython(np.ndarray[unsigned char, ndim=3] base_image, np.ndarray[int, ndim=2] labels, int num_labels):
    """
    A fully-compiled Cython function for maximum performance.
    """
    cdef int height = labels.shape[0]
    cdef int width = labels.shape[1]
    cdef int y, x, i, label_id
    # Use fixed-width types for clarity and compatibility
    cdef uint32_t packed_color, mode_val
    cdef int64_t max_count

    # Use single-token types inside template brackets
    cdef vector[unordered_map[uint32_t, int64_t]] counts_list
    for i in range(num_labels):
        counts_list.push_back(unordered_map[uint32_t, int64_t]())

    # --- Pass 1: Aggregate color counts in a single pass ---
    for y in range(height):
        for x in range(width):
            label_id = labels[y, x]
            if label_id == 0:
                continue

            packed_color = (base_image[y, x, 2] << 16) | (base_image[y, x, 1] << 8) | base_image[y, x, 0]

            counts_list[label_id][packed_color] += 1

    # --- Pass 2: Find the mode for each label ---
    cdef np.ndarray[np.uint32_t, ndim=1] mode_colors_packed = np.zeros(num_labels, dtype=np.uint32)
    for i in range(1, num_labels):
        if counts_list[i].empty():
            continue

        max_count = 0
        mode_val = 0
        for item in counts_list[i]:
            if item.second > max_count:
                max_count = item.second
                mode_val = item.first
        mode_colors_packed[i] = mode_val

    # --- Pass 3: Create the final output image ---
    cdef np.ndarray[unsigned char, ndim=3] output_image = np.zeros_like(base_image)
    cdef unsigned char r, g, b
    for y in range(height):
        for x in range(width):
            label_id = labels[y, x]
            if label_id == 0:
                continue

            packed_color = mode_colors_packed[label_id]
            r = (packed_color >> 16) & 255
            g = (packed_color >> 8) & 255
            b = packed_color & 255
            output_image[y, x, 0] = b
            output_image[y, x, 1] = g
            output_image[y, x, 2] = r

    return output_image
