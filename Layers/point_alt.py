"""
Ce module donne une liste des altitudes (d'apres le MNT) et couleurs qui correspondent a 
une liste des coordonees (lat, lon)
"""


from pyproj import Transformer


def get_alt(img, table, points, bounds):
    """
    Input: 
           - img : l'image du MNT
           - table : table 2d des altitudes (donnees du MNT)
           - points : liste des points (lat, lon)

    Ouput: 
           - altitude : liste des altitudes et des couleurs correspendantes prises de l'image en chaque point
    """
    altitude = []
    for p in points:
        try : 
            # converting to x/y
            lat = p[0]
            lon = p[1]
            proj = Transformer.from_crs(4326, 2154, always_xy=True)
            x, y = proj.transform(lon, lat)
            # prise de l'altitude du MNT
            dy = bounds[-1]-y-int(bounds[-1]-y)
            dx = x-bounds[0] - int(x-bounds[0])
            zx = table[int(bounds[-1]-y), int(x-bounds[0])]*dx + table[int(bounds[-1]-y), int(x-bounds[0])+1]*(1-dx)
            zy = table[int(bounds[-1]-y), int(x-bounds[0])]*dy + table[int(bounds[-1]-y)+1, int(x-bounds[0])+1]*(1-dy)
            # couleur du point dans l'image
            color = img[0, 0][:3]
            altitude.append(((zx+zy)/2, color))
        except :
            altitude.append((0, img[0, 0][:3]))    
    return altitude


#print(get_alt('./MNT/moulon.tif', [[48.7035,   2.1696]]))
