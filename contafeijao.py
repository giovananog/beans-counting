'''-------------------------------------------------------------------------
 * Universidade Federal de Alfenas - UNIFAL-MG
 * Bacharelado em Ciencia da Computacao
 * Trabalho de Processamento de Imagens
 * Atividade 1 - Contagem de Feijoes
 * Professor: Luiz Eduardo da Silva
 * Aluna: Giovana Nogueira Oliveira
 *-------------------------------------------------------------------------'''

import matplotlib.image as img
import numpy as np
import argparse

def readpgm (name):
    '''
    Reads a PGM image file and returns its pixel values as a list of lists.
    '''
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
    '''
    Saves a PGM image with the given name, image array, and depth.
    '''
    heigth = len(img)
    width = len(img[0])

    with open(name, 'w') as f:
        f.write("P2\n")
        f.write("# Image processing with python - ByDu\n")
        f.write("{} {}\n".format(width, heigth))
        f.write("{}\n".format(depth))  

        for line in img:
            for pixel in line:
                f.write("{} ".format(pixel))
            f.write("\n")

def imgalloc (nl, nc):
    '''
    Allocates an image with given dimensions (nl x nc).
    '''
    img = []
    for i in range(nl):
        lin = []
        for j in range(nc):
            lin.append(0)
        img.append(lin)
    return img

def find(parent, i):
    '''
    Finds the root of the set containing element i.
    This function implements path compression to keep the tree flat.
    '''
    while parent[i] != i:
        i = parent[i]
    return i

def union(parent, i, j):
    '''
    Unites the sets containing elements i and j.
    This function uses the `find` function to determine the roots and then performs the union.
    '''
    x = find(parent, i)
    y = find(parent, j)
    parent[y] = x

def label(image):
    '''
    Labels connected components in a image.
    Uses a union-find algorithm to manage connected components and returns the number of components.
    '''
    nr = len(image)
    nc = len(image[0])
    px = [item for sublist in image for item in sublist]
    num_label = 0
    parent = [i for i in range(1000)]

    for i in range(1, nr):
        for j in range(1, nc):
            p = px[i * nc + j]
            r = px[(i - 1) * nc + j]
            t = px[i * nc + j - 1]

            if p != 0:
                if r == 0 and t == 0:
                    px[i * nc + j] = num_label + 1
                    num_label += 1
                if r != 0 and t == 0:
                    px[i * nc + j] = r
                if r == 0 and t != 0:
                    px[i * nc + j] = t
                if r != 0 and t != 0 and t == r:
                    px[i * nc + j] = r
                if r != 0 and t != 0 and t != r:
                    px[i * nc + j] = t
                    union(parent, r, t)

    return len(set([find(parent, x) for x in px])) - 1

def dilate(image):
    '''
    Performs dilation on the given image.
    '''
    nr = len(image)
    nc = len(image[0])
    out = [row[:] for row in image] 

    for i in range(1, nr - 1):
        for j in range(1, nc - 1):
            maximum = -1  
            for y in range(-1, 2):
                for x in range(-1, 2):
                    pixel = image[i + y][j + x]
                    maximum = max(maximum, pixel)
            out[i][j] = maximum  

    return out

def erode(image):
    '''
    Performs erosion on the given image.
    '''
    nr = len(image)
    nc = len(image[0])
    out = [[0] * nc for _ in range(nr)] 

    for i in range(1, nr - 1):
        for j in range(1, nc - 1):
            minimum = float('inf') 
            for y in range(-1, 2):
                for x in range(-1, 2):
                    pixel = image[i + y][j + x]
                    minimum = min(minimum, pixel)
            out[i][j] = minimum  

    return out

def count_beans(img):
    '''
    Applies thresholding, erosion, dilation, and labeling to count the number of beans in the img.
    Returns the number of beans.
    '''
    img = np.array(img)
    threshold_value = 63

    # thresholding
    img_thresholded = np.where(img >= threshold_value, 0, 1)

    # erosion
    img_eroded = erode(img_thresholded)
    img_eroded = erode(img_eroded)

    # dilation
    img_dilated = dilate(img_eroded)

    return label(img_dilated)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script description')
    parser.add_argument('image_name', type=str, help='Image name in format .PGM')
    args = parser.parse_args()
    image_name = args.image_name

    img = readpgm (image_name)
    beans = count_beans(img)
    print("#componentes: ", beans)