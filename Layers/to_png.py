"""
Ce module enregistre une copie coloree du fichier tiff (format png) afin de la superposer avec 
la carte
"""

import rasterio as rio
import numpy as np
import matplotlib.pyplot as plt

def conv(path,filename):
    # Lit le fichier tiff
    with rio.open(path+filename) as src:
        img = src.read(1)
        nodata = src.nodata
    img[img==nodata] = np.nan 
    # Construit une figure colorée et l'enregistre
    I = plt.imshow(img)
    plt.axis('off')
    plt.savefig(path+filename.split('.')[0]+'.png', bbox_inches='tight', pad_inches=0,transparent=True)