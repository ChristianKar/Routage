""" 
Puisqu'on veut apres presenter toutes les courbes et anlyses sur une page HTML interractive, les 
calculs ne peuvent pas se faire en temps reel car ca va prendre du temps de refraichir le page
chaque fois, pour cette raison, en utilisant ce module on fait tous les calculs et analyses et 
les enregistrer dans un fichier npy qui va rendre l'acces aux donnees rapide et simple.

"""

import sys
from pathlib import Path
file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from Analysis import extract, deriv
from Compare_alt import plot_diff
import numpy as np
import pandas as pd
from Layers.point_alt import get_alt
import pandas as pd
import haversine as hs
import rasterio
from skimage import io


# Extraction des données des fichiers gpx en utilisant le module Analysis.py
D = extract()

coordinates = [[tuple(x) for x in i[0][['latitude', 'longitude']].to_numpy()] for i in D]
values = []

data1 = io.imread('./MNT/Saclay.png')
data2 = io.imread('./MNT/paris.png')

# Genere un tableau des couleurs qu'on va associer a chaque portion du trajet en fonction de l'altitude.
# La fonction get_alt du module point_alt.py retourne l'altitude en chaque point ainsi que la couleur
# associée
with rasterio.open('./MNT/Saclay.tif') as dataset1:
    with rasterio.open('./MNT/paris.tif') as dataset2:
        table1 = dataset1.read(1)
        table2 = dataset2.read(1)
        values = [get_alt(data1, table1, c, dataset1.bounds) for c in coordinates[:-1]]
        values += [get_alt(data2, table2, c, dataset2.bounds) for c in coordinates[-1:]]
colors = []

for i in range(len(values)):
    C = []
    for j in range(len(values[i])):
        if values[i][j]:
            C.append(values[i][j][1])
        else:
            C.append([None])
    colors.append(C)


def haversine_distance(lat1, lon1, lat2, lon2) :
    #fonction qui calcule la distance en metre la distance entre deux point en coordonnees spheriques
    """
    Input: - lat1, lon1: Coordonnee du premier point
           - lat2, lon2: Coordonnee du deuxieme point

    Ouput: distance entre les deux points       
    
    """
    distance = hs.haversine(
        point1=(lat1, lon1),
        point2=(lat2, lon2),
        unit=hs.Unit.METERS
    )
    return np.round(distance, 2)

for i in D : 

    route_df, Xp2, Yp2, X, velocity, elem, eleg, num = i
    print('jj')

    # Ajout d'une colonne de difference d'altitude pour calculer le gradient ensuite
    route_df['new_elevation_diff'] = route_df['new_elevation'].diff()
    route_df['elevation_diff'] = route_df['elevation'].diff()

    # Ajout d'une colonne des distances entre chaque paire de points
    distances = [np.nan]
    for j in range(len(route_df)):
        if j == 0:
            continue
        else:
            distances.append(haversine_distance(
                lat1=route_df.iloc[j - 1]['latitude'],
                lon1=route_df.iloc[j - 1]['longitude'],
                lat2=route_df.iloc[j]['latitude'],
                lon2=route_df.iloc[j]['longitude']
            ))
    route_df['distance'] = distances        

    # Calcul du gradient des altitudes prises du fichier MNT 
    gradients = [np.nan]

    for ind, row in route_df.iterrows(): 
        if ind == 0:
            continue
        if row['distance'] :
            grade = (row['new_elevation_diff'] / row['distance']) * 100
            gradients.append(np.round(grade, 1))
        else :
            gradients.append(np.round(0, 1))   
    route_df['new_gradient'] = gradients

    # Calcul du gradient des altitudes mesurées dans le fichier gpx
    gradients2 = [np.nan]
    for ind, row in route_df.iterrows(): 
        if ind == 0:
            continue
        if row['distance'] :
            grade = (row['elevation_diff'] / row['distance']) * 100
            gradients2.append(np.round(grade, 1))
        else :
            gradients2.append(np.round(0, 1))   
    route_df['gradient'] = gradients2

    # Calcul du gradient à l'aide de la fonction deriv

    x = np.array(i[0]['x'])
    y = np.array(i[0]['y'])      
    Distance = [0]*5
    # filtrage des coordonnées x et y
    _, x, _ = deriv(np.arange(len(x)), x, k=5)
    _, y, _ = deriv(np.arange(len(y)), y, k=5)
    for j in range(1, len(x)):
        Distance.append(((x[j]-x[j-1])**2 + (y[j]-y[j-1])**2)**0.5+Distance[-1])  
 

    print(len(gradients), len(route_df['new_elevation']), len(Distance))

    print('grad')

    Xgrad, _, Ygrad = deriv(Distance, route_df['new_elevation'][5:-5], k=5)
    if D.index(i) == 5 : 
        Xgrad, _, Ygrad = deriv(Distance, route_df['elevation'][5:-5], k=5)
    # Regroupement des infos sur le trajet dans une petite dataframe
    Analysis_data2 = {'T'+str(D.index(i)+1):['min', 'max'],'elevation': list(elem), 'elevation gain':[round(eleg[0], 2), round(eleg[1], 2)], 'number of tracks':[num, num]}
    df2 = pd.DataFrame(Analysis_data2)
    
    # Calcule des diffrences entre l'altitude mesurée et prise du MNT
    Xd, Yd, Zd = plot_diff(route_df, D.index(i)==5)

    #Ajout des différents résultats dans le tableau D
    i.pop(-1)
    i.pop(-1)
    i.pop(-1)
    i.append(df2)
    i += [Xd, Yd, Zd]
    i += [Xgrad[1:], np.array(Ygrad[1:])*100]

    # Creating the bins/bar for the histogram!
    bins = pd.IntervalIndex.from_tuples([
        (-40, -15),
        (-15, -12),
        (-12, -10),
        (-10, -7),
        (-7, -5),
        (-5, -3),
        (-3, -1),
        (-1, 0),
        (0, 1),
        (1, 3),
        (3, 5),
        (5, 7),
        (7, 10),
        (10, 12),
        (12, 15),
        (15, 40)
    ], closed='left')

    route_df['gradient_range'] = pd.cut(route_df['new_gradient'], bins = bins)

    gradient_info = []

    for gr_range in route_df['gradient_range'].unique():
        
        # Basically, the following takes a bin and try to add everything that belongs in the same bin!
        # It gives a column with false and true if it belongs to the specific bin!

        bin_belonging = route_df[route_df['gradient_range'] == gr_range]
        
        # Some Statistics of the Route!
        total_distance = bin_belonging['distance'].sum() # The total distance in this bin (in this range).
        pct_of_the_total_ride = (bin_belonging['distance'].sum() / route_df['distance'].sum()) * 100 # The range's percentage of the total ride! 
        
        # Elevation (gain & lost) of the route!
        elevation_gain = bin_belonging[bin_belonging['new_elevation_diff'] > 0]['new_elevation_diff'].sum()
        elevation_lost = bin_belonging[bin_belonging['new_elevation_diff'] < 0]['new_elevation_diff'].sum()

        # Time calcualatio for each bin!
        bin_time = bin_belonging['time'].sum() # The total time in each bin (in this range).
        
        # Save the info and the statistics we obtained:
        
        gradient_info.append({
            'gradient_range': gr_range,
            'total_distance': np.round(total_distance, 2),
            'total_time': np.round(bin_time, 2),
            'pct_of_the_total_ride': np.round(pct_of_the_total_ride, 2),
            'elevation_gain': np.round(elevation_gain, 2),
            'elevation_lost': np.round(np.abs(elevation_lost), 2)
        })

    # Sorted by gradient range! (from smaller to greater!)

    gradient_infodetails_df = pd.DataFrame(gradient_info).sort_values(by='gradient_range').reset_index(drop = True)

    # By analyzing this dataframe (gradient_infodetails_df), we can understand the profile of the route!
    # Also, we can conclude on what was the pace of the user!

    # We create a list of colours for the bins!
    color_map = [
        # Blue Shades
        '#0000FF', '#1E90FF', '#00BFFF',
        '#87CEFA', '#B0E0E6',
        # Green Shades
        '#69bb66', '#fff59d', '#ffee58',
        # Red Shades
        '#ffca28', '#ffa000', '#ff6f00', '#f4631e', '#d80000', '#eb0000', '#FF0000']

    # Each bar will show the distance and the time the user spent in this bin!
    bins_text = [f'''<b>{range_group}%</b> - {distance}km - {time} min''' for range_group, distance, time in
    zip(
        gradient_infodetails_df['gradient_range'].astype('str'),
        gradient_infodetails_df['total_distance'].apply(lambda x: round(x / 1000, 2)),
        gradient_infodetails_df['total_time'].apply(lambda y: round(y / 60, 2))
    )]
    i.append(color_map)
    i.append(bins_text)
    i.append(gradient_infodetails_df)

    

# Enregistrement des Output d'analyses dans un fichier npy
T = np.array([D, np.array(coordinates), np.array(colors)])
np.save('./Extracted_data/Data2.npy', T)