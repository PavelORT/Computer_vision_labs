from typing import Tuple

import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from numpy import ndarray, dtype, float64
from tqdm import tqdm


def Gauss_filter(image: np.ndarray, filtersize: int = 3, sigma: float = 1, dupledge: bool = False, grout: bool = False, verbose: bool = False) -> np.ndarray:
    """
    image - исходное изображение массив np.ndarray (Н, W, C) H-высота, W - ширина, C - число каналов
    filtersize - размер стороны ядра свёртки, нечётное число
    sigma – стандартное отклонение нормального распределения;
    dupledge = True - расширение зеркалом с дублированием края
    dupledge = False  - расширение зеркалом без дублирования края
    verbose - вывод массивов, по которым происходит выбор
    grout - выбирать большее значение за медиану, только при expand = 0
    
    """
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

    kernel = np.zeros((filtersize, filtersize))
    kernel_center = filtersize // 2
    
    koeff = 1 / (2 * np.pi * sigma * sigma)
    for i in range(filtersize):
        for j in range(filtersize):
            x = i - kernel_center
            y = j - kernel_center
            kernel[i, j] = koeff*np.exp(-(x*x+y*y)/(2*sigma*sigma))
    # Нормализация ядра свёртки
    kernel = kernel / np.sum(kernel)
    
    buf_image = np.zeros((H + 2 * edge, W + 2 * edge, C), dtype=np.uint8)  #  image.dtype

    buf_image[edge: H + edge, edge: W + edge, :] = image #image.copy()

    
    if dupledge:
        bias = 0
    else:
        bias = 1      
    for ed in range(1, edge+1):  
        for k in range(C):
            buf_image[edge-ed:edge-ed+1,edge:W+edge] = image[ed-1+bias:ed+bias, :]
            buf_image[edge+H+ed-1:edge+H+ed,edge:W+edge] = image[H-ed-bias:H-ed+1-bias, :]
    for ed in range(1, edge+1):  
        for k in range(C):
            buf_image[:,edge-ed:edge-ed+1] = buf_image[:, edge+ed-1+bias:edge+ed+bias]
            buf_image[:,W+edge+ed-1:W+edge+ed] = buf_image[:, W+edge-ed-bias:W+edge-ed+1-bias]                
    
    res_image = np.zeros((H, W, C),dtype = np.uint8)  # dtype=image.dtype)

    
    for i in tqdm(range(H)):
        for j in range(W):
            for k in range(C):
                if (i > edge):
                    pass
                if (j > edge):
                    pass
                sub_array = buf_image[i:i + filtersize, j:j + filtersize,k:k+1]
                product = sub_array * kernel
                sum = np.sum(product)
                res_image[i, j, k] = sum #np.sum(sub_array * kernel)
    
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


    arr_med = Gauss_filter(test_arr)
    print(arr_med.squeeze())
    print()
    print(test_arr.squeeze())