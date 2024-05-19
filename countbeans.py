'''-------------------------------------------------------------------------
 * Universidade Federal de Alfenas - UNIFAL-MG
 * Bacharelado em Ciencia da Computacao
 * Trabalho de Processamento de Imagens
 * Atividade 1 - Contagem de Feijoes
 * Professor: Luiz Eduardo da Silva
 * Aluno: Giovana Nogueira Oliveira
 *-------------------------------------------------------------------------'''

import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np
import argparse
import os

#############################
# manipulate img functions  #
#############################

def readpgm (name):
    f = open(name,"r")

    assert f.readline() == 'P2\n'
    line = f.readline()
    while (line[0] == '#'):
           line = f.readline()
    (width, height) = [int(i) for i in line.split()]
    depth = int(f.readline())
    assert depth <= 255
    
    img = []
    row = []
    j = 0
    for line in f:
       values = line.split()
       for val in values:
           row.append (int (val))
           j = j + 1
           if j >= width:
              img.append (row)
              j=0
              row = []

    f.close()
    return img

def savepgm(name, img, depth):
    # Dimensions
    heigth = len(img)
    width = len(img[0])

    # Open file to write in
    with open(name, 'w') as f:
        # Pgm header
        f.write("P2\n")
        f.write("# Image processing with python - ByDu\n")
        f.write("{} {}\n".format(width, heigth))
        f.write("{}\n".format(depth))  # Max gray level

        # write pixels to pgm file
        for line in img:
            for pixel in line:
                f.write("{} ".format(pixel))
            f.write("\n")

def imgalloc (nl, nc):
    img = []
    for i in range(nl):
        lin = []
        for j in range(nc):
            lin.append(0)
        img.append(lin)
    return img


#############################
# threshold                 #
#############################

def threshold(image, threshold_value):
    thresholded_image = []
    for row in image:
        thresholded_row = []
        for pixel in row:
            if pixel >= threshold_value:
                thresholded_row.append(255) 
            else:
                thresholded_row.append(0)
        thresholded_image.append(thresholded_row)
    return thresholded_image


#############################
# labeling                  #
#############################

def connected_components_labeling(image):
    label = 1
    image_np = np.array(image) 
    labels = np.zeros_like(image_np)

    for i in range(image_np.shape[0]):
        for j in range(image_np.shape[1]):
            if image_np[i, j] == 0:
                label_up = labels[i - 1, j] if i > 0 else 0
                label_left = labels[i, j - 1] if j > 0 else 0

                if label_up == 0 and label_left == 0:
                    labels[i, j] = label
                    label += 1
                elif label_up != 0 and label_left == 0:
                    labels[i, j] = label_up
                elif label_up == 0 and label_left != 0:
                    labels[i, j] = label_left
                else:
                    labels[i, j] = label_left
                    if label_up != label_left:
                        labels[labels == label_up] = label_left

    num_components = len(np.unique(labels)) - 1 
    print("#componentes:", num_components)

    return labels



#############################
# dilata                    #
#############################

def dilate(image, kernel):
    image_height, image_width = image.shape
    kernel_height, kernel_width = kernel.shape

    pad_height = kernel_height // 2
    pad_width = kernel_width // 2

    dilated_image = np.zeros_like(image)

    for i in range(image_height):
        for j in range(image_width):
            if image[i, j] == 255:
                for m in range(kernel_height):
                    for n in range(kernel_width):
                        row = i + m - pad_height
                        col = j + n - pad_width
                        if 0 <= row < image_height and 0 <= col < image_width:
                            if kernel[m, n] == 1:
                                dilated_image[row, col] = 255

    return dilated_image

#############################
# erosao                    #
#############################
def erode(image, kernel):
    image_height, image_width = image.shape
    kernel_height, kernel_width = kernel.shape
    pad_height = kernel_height // 2
    pad_width = kernel_width // 2
    eroded_image = np.zeros_like(image)
    for i in range(image_height):
        for j in range(image_width):
            min_val = 255
            for m in range(kernel_height):
                for n in range(kernel_width):
                    row = i + m - pad_height
                    col = j + n - pad_width
                    if 0 <= row < image_height and 0 <= col < image_width:
                        if kernel[m, n] == 1:
                            min_val = min(min_val, image[row, col])
            eroded_image[i, j] = min_val
    return eroded_image

#############################
# 'main'  #
#############################

#Read image
parser = argparse.ArgumentParser(description='Script description')

# Add Arguments
parser.add_argument('image_name', type=str, help='Image name in format .PGM')

# Analising arguments in command line
args = parser.parse_args()
image_name = args.image_name

img = readpgm (image_name)

img = np.array(img)

img = threshold(img, 55)
img = np.array(img)

kernel = np.ones((4, 4), dtype=np.uint8)
img = dilate(img, kernel)

kernel = np.ones((3, 3), dtype=np.uint8)
img = erode(img, kernel)

img = connected_components_labeling(img)

savepgm("result.pgm", img, 255)

#Discomment this line for linux system
# os.system("{} {} &".format("eog", "result.pgm"))

#Discomment this line for windows system
os.system("{} {} &".format("i_view64", "result.pgm"))