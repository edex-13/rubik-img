import cv2 as cv
import cv2
import shutil

import numpy as np
import os
import random

# import tensorflow as tf


def recortar(img):
    height, width, channels = img.shape

    w = int(width)
    h = int(height)

    img = img[int(h/2-125):int(h/2+125), int(w/2-125):int(w/2+125)]

    return img


def generar(img):
    image = recortar(img)
  

    height, width, channels = image.shape

    # print(height)
    # print(width)

    widthToRect = 250 // 3  # En este caso, dividimos la imagen en un grid de 3x3

    COLORES = []

    for i in range(3):
        for j in range(3):
            #print("1")
            start_x = j * widthToRect
            #print("2")

            end_x = (j + 1) * widthToRect

            start_y = i * widthToRect
            end_y = (i + 1) * widthToRect

            # Recorta el bloque de la imagen original
            masked = image[start_y:end_y, start_x:end_x].copy()

            r = 0
            g = 0
            b = 0

            for _ in range(100):

                color = masked[random.randint(
                    0, widthToRect-1), random.randint(0, widthToRect-1)]
  

                r += int(color[0])
                g += int(color[1])
                b += int(color[2])

            r = r//100
            g = g//100
            b = b//100

            # print((r, g, b))



            COLORES.append((r, g, b))

    CUBO = np.zeros((300, 300, 3), np.uint8)
    index = 0

    for i in range(0, 300, 100):
        for j in range(0, 300, 100):
            cv.rectangle(CUBO, (j, i), (j+100, i+100), COLORES[index], -1)
            index += 1

    rotated_image = cv.rotate(CUBO, cv.ROTATE_90_CLOCKWISE)

    # cv.imshow('Imagen', image)
    # cv.imshow('Imagen', rotated_image)

    return CUBO


def recortar_img_cubo(imgs, name, name2):
    p = []
    # print("aaaaaaaaaaaaaaaaaaaaa")
    small_size = 250//3
    n = 0

    # Crea la carpeta de nuevo


    small_images = []

    for i_m in range(3):
        for j_m in range(3):
            start_x = j_m * small_size + 10
            end_x = (j_m + 1) * small_size -10

            start_y = i_m * small_size +10
            end_y = (i_m + 1) * small_size -10
            

            # Recorta el bloque de la imagen original
            masked = imgs[start_y:end_y, start_x:end_x].copy()

            small_images.append(masked)

    # print(len(small_images))
    # Guarda y muestra las imágenes más pequeñas
    n = 0
    colores = []
    f = 0
    for imgsa in small_images:
        filename = f'img/img_{name2}_{n}.jpg'
        color = categorizar(imgsa , f"img_{name2}_{n}")
        print(color)
        n += 1
        colores.append(color)
        # cv.imshow('Imagen', imgsa)
        # print("--")

        p.append([])
        cv.imwrite(filename, imgsa)
    

    return colores

def categorizar(img , name):
    # Convertir la imagen a espacio de color HSV

    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Calcular los valores promedio y la moda de H, S, V
    h, s, v = cv2.split(hsv_img)
    average_hue = np.mean(h)
    average_saturation = np.mean(s)
    average_value = np.mean(v)
    
    # Usar la moda para el tono puede ayudar con la consistencia
    hue_mode = np.argmax(np.bincount(h.flatten()))

    # Función para comprobar si un color es predominante
    def is_color_dominant(hue_range):
        return np.sum((h >= hue_range[0]) & (h <= hue_range[1])) / h.size > 0.7

   
    light_pixels = np.sum((s < 30) & (v > 90))
    light_percentage = light_pixels / (h.size)

    # Clasificación de color
    if light_percentage > 0.5:  # Si más del 80% de los píxeles son considerados claros
        color = "b"
    elif average_saturation < 49 and average_value > 100:
        color = "b"
    elif is_color_dominant((0, 5)) or is_color_dominant((170, 180)):
        color = "r"
    elif is_color_dominant((6, 19)):
        color = "n"
    elif is_color_dominant((19, 53)):
        color = "a"
    elif is_color_dominant((53, 90)):
        color = "v"
    elif is_color_dominant((91, 130)):
        color = "az"
    else:
        # Si no se ha clasificado, usar la moda del tono
        if hue_mode < 5 or hue_mode > 170:
            color = "r"
        elif hue_mode < 19:
            color = "n"
        elif hue_mode < 53:
            color = "a"
        elif hue_mode < 90:
            color = "v"
        elif hue_mode < 130:
            color = "az"
        else:
            color = "r"

    return f"{color}"

def principal():
    pp = []
    nombre_carpeta = 'predecir'
    if os.path.exists('predecir'):
        # Borra la carpeta y su contenido
        # os.rmdir(nombre_carpeta)
        shutil.rmtree(nombre_carpeta)
    os.mkdir(nombre_carpeta)

    for i in range(6):

        filename = 'img/images' + str(i+1) + '.jpg'
        filename2 = 'img/cara' + str(i+1) + '.jpg'
        generar(cv.imread(filename))
        cv.imwrite(filename2, generar(cv.imread(filename)))

        img = cv.imread(f'img/images{i+1}.jpg')
        img = cv2.flip(img, 1)

        img = recortar(img)
        # print("suuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu")
        pp.append(recortar_img_cubo(img, f'img/images{i+1}.jpg', f'cara{i+1}'))


    # folder_path = 'predecir'  # Reemplaza con la ruta de tu carpeta
    # elements = os.listdir(folder_path)
    # count = len(elements)

    # print(f'La carpeta contiene {count} elementos.')

    
    # Convertimos de vuelta a una lista de Python
 
    return pp


principal()