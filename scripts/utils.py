import os
import pygame

BASE_IMAGE_PATH = 'data/images/'

# load a single image
def load_image(path):
    img = pygame.image.load(BASE_IMAGE_PATH + path).convert()
    img.set_colorkey((0,0,0))
    return img

# load all images in a directory
def load_images(path):
    images = []

    for img_name in sorted(os.listdir(BASE_IMAGE_PATH + path)): # sorted is used for OS interoperability
        images.append(load_image(path + '/' + img_name))

    return images


