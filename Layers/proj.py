"""
Ce module enregistre une copie reprojectése du fichier tiff du crs EPSG:2154 vers le crs EPSG:4326
puisque le module d'affichage de cartes (folium) prend en entree les coordonees au format EPSG:4326
"""

import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling


def reproj(path, filename):
    dst_crs = 'EPSG:4326'

    with rasterio.open(path+filename) as src:
        transform, width, height = calculate_default_transform(
            'EPSG:2154', dst_crs, src.width, src.height, *src.bounds)   
        kwargs = src.meta.copy()
        kwargs.update({
            'crs': dst_crs,
            'transform': transform,
            'width': width,
            'height': height
        })

        with rasterio.open(path+'proj_'+filename, 'w', **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs='EPSG:2154',
                    dst_transform=transform,
                    dst_crs=dst_crs,
                    resampling=Resampling.nearest)          