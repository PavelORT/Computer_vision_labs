from typing import Tuple

import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from numpy import ndarray, dtype, float64


def Median_filter(image: np.ndarray, filtersize: int = 3) -> np.ndarray:
    H = image.shape[0]
    W = image.shape[1]
    C = image.shape[2]
    edge = 1
    if (filtersize % 2 and filtersize > 0):
        edge = (filtersize - 1) // 2
    else:
        ####Error
        raise ValueError("Размер ядра должен быть нечетным числом")
        # res_image = np.zeros((H, W, C))

    # kernel = np.zeros((filtersize, filtersize))
    buf_image = np.zeros((H + 2 * edge, W + 2 * edge, C), dtype=image.dtype)  # np.uint8

    buf_image[edge: H + edge, edge: W + edge, :] = image.copy()

    res_image = np.zeros((H, W, C))  # dtype=image.dtype)
    for k in range(C):
        for i in range(H):
            for j in range(W):
                arr_len = filtersize * filtersize
                value_array = np.zeros(1, dtype=np.uint8)
                for jl in range(2 * edge + 1):
                    for il in range(2 * edge + 1):
                        if (il + jl == 0):
                            value_array[0] = buf_image[i + il][j + jl][k]
                        else:
                            for pos in range(len(value_array)):
                                pos_val = buf_image[i + il][j + jl][k]
                                if (value_array[pos] >= pos_val):
                                    value_array = np.insert(value_array, pos, pos_val)
                                    break
                                elif (pos == arr_len - 1):
                                    value_array = np.append(value_array, pos, pos_val)

                print(value_array)
                center = len(value_array) // 2
                value = value_array[center]
                res_image[i][j][k] = value
    return res_image.astype(np.uint8)


if __name__ == "__main__":
    rng = np.random.default_rng(seed=42)# Создаем генератор случайных чисел
    test_arr = rng.integers(0, 255, size=(3, 3, 1))
    print(test_arr.squeeze())
    print()
    image = test_arr
    filtersize = 3
    H = image.shape[0]
    W = image.shape[1]
    C = image.shape[2]
    edge = 1
    if (filtersize % 2 and filtersize > 0):
        edge = (filtersize - 1) // 2
    else:
        ####Error
        raise ValueError("Размер ядра должен быть нечетным числом")
        # res_image = np.zeros((H, W, C))

    # kernel = np.zeros((filtersize, filtersize))
    buf_image = np.zeros((H + 2 * edge, W + 2 * edge, C), dtype=image.dtype)  # np.uint8

    buf_image[edge: H + edge, edge: W + edge, :] = image.copy()

    res_image = np.zeros((H, W, C))  # dtype=image.dtype)
    for k in range(C):
        for i in range(H):
            for j in range(W):
                arr_len = filtersize * filtersize
                value_array = np.zeros(1, dtype=np.uint8)
                for jl in range(2 * edge + 1):
                    for il in range(2 * edge + 1):
                        if (il + jl == 0):
                            value_array[0] = buf_image[i + il][j + jl][k]
                        else:
                            for pos in range(len(value_array)):
                                pos_val = buf_image[i + il][j + jl][k]
                                if (value_array[pos] >= pos_val):
                                    value_array = np.insert(value_array, pos, pos_val)
                                    break
                                elif (pos == arr_len - 1):
                                    value_array = np.append(value_array, pos, pos_val)

                print(value_array)
                center = len(value_array) // 2
                value = value_array[center]
                res_image[i][j][k] = value
    print(res_image.squeeze())


    arr_med = Median_filter(test_arr)
    print(arr_med.squeeze())
    print()
    print(test_arr.squeeze())