import sys
from pathlib import Path
file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from Layers.point_alt import get_alt
import rasterio
from skimage import io
import matplotlib.pyplot as plt

def compare_alt_point(point, logs, data, table, bounds):
    '''
    Input :
           - point : a point of the map [[lat, long]]
           - logs : a dataframe
    '''
    # We get the altitude of the points from the MNT
    couple = get_alt(data, table, point, bounds)[0]
    if couple != None:
        alt, snd = couple
    else:
        alt = 0
    # We get the altitude of the points from the gps logs
    alt_bis = []
    for idx in logs.index:
        lon = logs.at[idx, "longitude"]
        lat = logs.at[idx, 'latitude']
        alt_ = logs.at[idx, 'elevation']
        if abs(lat - point[0][0]) < 0.00001 and abs(lon - point[0][1]) < 0.00001:
            alt_bis.append(alt_)
    if alt == 0:
        alt = alt_bis[0]
    return (alt - alt_bis[0])


def differential_dt(logs, paris):
    D = []
    data = io.imread('./MNT/Saclay.png')
    if paris :
        data = io.imread('./MNT/paris.png')
    
    with rasterio.open('./MNT/Saclay.tif') as dataset1:
        with rasterio.open('./MNT/paris.tif') as dataset2:
            table = dataset1.read(1)
            bounds = dataset1.bounds
            if paris :
                table = dataset2.read(1)
                bounds = dataset2.bounds
            for idx in logs.index:
                lat = logs.at[idx, "latitude"]
                lon = logs.at[idx, "longitude"]
                ele = logs.at[idx, "elevation"]
                d = compare_alt_point([[lat, lon]], logs, data, table, bounds)
                if d != 0:
                    D.append((lat, lon, (100*d/ele)))
    return D


# print(differential_dt())


def plot_diff(route_df, paris):
    #fig = plt.figure()
    # syntax for 3-D projection
    D = differential_dt(route_df, paris)
    #ax = plt.axes(projection='3d')
    X = []
    Y = []
    Z = []
    for d in D:
        x, y, z = d
        X.append(x)
        Y.append(y)
        Z.append(z)

    # plotting
    #ax.plot3D(X, Y, Z)
    #ax.set_title('Differentiel')
    #plt.show()
    return X, Y, Z


def find_max_diff(tab):
    """
    Input :
           - An array of (long, lat, diff) 

    Output :
           - The max value
    """
    long, lat, max = tab[0]
    for f in tab:
        a, b, c = f
        if abs(c) > abs(max):
            max = c
    return max


def find_min_diff(tab):
    """
    Input :
           - An array of (long, lat, diff)
           
    Output :
           - The min value
    """
    long, lat, min = tab[0]
    for f in tab:
        a, b, c = f
        if abs(c) < abs(min):
            min = c
    return min


def delete_biais(tab):
    max = find_max_diff(tab)
    min = find_min_diff(tab)
    tab_bd = []
    for f in tab:
        a, b, c = f
        tab_bd.append((a, b, c - min))
    return tab_bd


# plot_diff(delete_biais(differential_dt()))

# We try to estimate the errors on the slopes between the MNT and the gps logs


def histogram(tab):
    max = abs(find_max_diff(tab))
    min = abs(find_min_diff(tab))
    occ_neg = [0] * (int(max) + 1)
    occ_pos = [0] * (int(max) + 1)
    zero = 0
    for f in tab:
        a, b, c = f
        cat = int(c)
        if cat < 0:
            occ_neg[-cat] += 1
        elif cat == 0:
            zero += 1
        else:
            occ_pos[cat] += 1
    occ = occ_neg + [zero] + occ_pos
    zero_pos = len(occ_neg)
    plt.hist(occ)
    plt.show()
