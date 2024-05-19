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
    print (width, height)
    depth = int(f.readline())
    assert depth <= 255
    print (depth)
    
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
                thresholded_row.append(255)  # Pixel branco
            else:
                thresholded_row.append(0)    # Pixel preto
        thresholded_image.append(thresholded_row)
    return thresholded_image



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
print (np.asarray (img))
#os.system("{} {} &".format("eog", image_name))

#transformations 
img = threshold(img, 100)

print (np.asarray (img))
savepgm("result.pgm", img, 255)

# os.system("{} {} &".format("eog", "result.pgm"))

#Discomment this line for windows system
os.system("{} {} &".format("i_view64", "result.pgm"))