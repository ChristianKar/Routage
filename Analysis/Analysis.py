"""Description : Ce module analyse les fichiers gpx afin d'extraire une dataframe des coordonnees,
la vitesse (filtree et non filtree) en chaque point ainsi que quleque infos sur le trajet"""


import sys
from pathlib import Path
file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from os import getcwd
import gpxpy
import gpxpy.gpx
import pandas as pd
import numpy as np
import math as m
from pyproj import Transformer
from Layers.point_alt import get_alt
import rasterio
from skimage import io

def deriv(x,y,k = 3, p = 2):
    """
    Input: - x : tableau des abscisses
           - y : tableau des ordonnees 
           - k : 2k+1 est la taille de la fenetre
           - p : degré du polynôme de regression

    Ouput: - x_lisse 
           - y_lisse : ordonnees lissees 
           - y_p_lisse : ordonnees lissees et derivees analytiquement 
    
    """
    n = len(x)
    y_lisse = []
    y_p_lisse = []
    x_lisse = x[k:n-k]
    for i in range(k,n-k):
        try:
            #définition du paramèttre à optimiser : méthode des moindres carrés
            Xi = np.array([x[i-k:i+k]])
            Yi = np.array(y[i-k:i+k])
            arg = tuple([Xi**(p-j) for j in range(p+1)])
            Xi_pow = np.concatenate(arg,axis=0)
            M = np.dot(Xi_pow,Xi_pow.T)
            V = np.dot(Yi, Xi_pow.T)
            P = np.linalg.solve(M,V)
            Xi_pow = np.array([x[i]**(p-j) for j in range(p+1)])
            #ajout de la dérivée de la fonction modèle local en X[i]
            y_lisse.append(np.dot(P,Xi_pow))
            Xip_pow = [(p-j)*x[i]**(p-j-1) for j in range(p)]
            y_p_lisse.append(np.dot(Xip_pow,P[:-1]))
        except: 
            y_p_lisse.append(0)
            y_lisse.append(0)       
    return x_lisse, y_lisse, y_p_lisse

def extract():
    """
    Ouput: D : Tableau des donnees 
    """
    # extracts all the infos from the 5 gpx file and put it all in table D and calculate the speed
    D = []

    # Opening the MNT file in order to get the exact altitude of each point 
    data = io.imread('./MNT/Saclay.png')
    with rasterio.open('./MNT/Saclay.tif') as dataset2:
        table = dataset2.read(1) 
        bounds = dataset2.bounds
        with rasterio.open('./MNT/paris.tif') as dataset1:
            
            # defining all the gpx files we're going to analyse
            d = dict({'T1':'Guichet_asc_orux.gpx', 'T2':'Guichet_asc_strava_slow.gpx',
                    'T3':'Guichet_asc_strava.gpx', 'T4':'Guichet_asc_suunto.gpx', 'T5':'Guichet_dsc_strava.gpx', 'T6':'activity_8541586125.gpx'})
            for name in d.values() :
                if d['T6'] == name :
                    table = dataset1.read(1)   
                    data = io.imread('./MNT/paris.png')
                    bounds = dataset1.bounds

                CURR_PATH = getcwd()
                # The above command will give us the current working directory.
                PATH_DATA = CURR_PATH + "/GPX/"
                # Lire les donnees gpx
                with open(PATH_DATA + name, 'r') as gpx_file:
                    gpx = gpxpy.parse(gpx_file)

                # elevation maxie/mini du trajet, gain et perte d'elevation, et nombre des trajets 
                # detectes dans le meme fichier    
                ele_min_max = gpx.get_elevation_extremes()
                ele_gain_and_loss = gpx.get_uphill_downhill()    
                number_of_tracks = len(gpx.tracks)
                route_info = []
                
                # Construction de la dataframe
                for track in gpx.tracks:

                    for segment in track.segments:
                        prev_point = None

                        for point in segment.points:
                            if not prev_point or (point.time - prev_point.time).total_seconds() > 0 :
                                if prev_point :
                                    route_info.append({
                                        'latitude': point.latitude,
                                        'longitude': point.longitude,
                                        'elevation': point.elevation, 
                                        'new_elevation': get_alt(data, table, [[point.latitude, point.longitude]], bounds)[0][0],
                                        'speed' : point.speed_between(prev_point),
                                        'time' : (point.time - segment.points[0].time).total_seconds()
                                    })
                                # la colone elevation contient l'altitude mesuree dans le fichier gpx (n'est pas exacte)
                                # la colone elevation contient l'altitude prise du MNT a ce point (exacte)  
                                else :
                                    route_info.append({
                                        'latitude': point.latitude,
                                        'longitude': point.longitude,
                                        'elevation': point.elevation, 
                                        'new_elevation': get_alt(data, table, [[point.latitude, point.longitude]], bounds)[0][0],
                                        'speed' : point.speed_between(prev_point),
                                        'time' : 0
                                    })
                            prev_point = point

                # Reprojection des coordonnees spheriques (lom, lat) en coord cartesiennes (x, y) 
                # pour savoir calculer la vitesse
                proj = Transformer.from_crs(4326, 2154)
                for i in range(len(route_info)) :
                    route_info[i]['x'], route_info[i]['y'] = proj.transform(route_info[i]['latitude'], route_info[i]['longitude'] )

                # Calibration des donnees pour les deriver
                t = [point['time'] for point in route_info]
                x = [point['x']-route_info[0]['x'] for point in route_info]
                y = [point['y']-route_info[0]['y'] for point in route_info]
                z = [point['new_elevation']-route_info[0]['new_elevation'] for point in route_info]

                # Derivation analytique des donnees filtrees par la methode du moindre carre
                _, _, x_p = deriv(t,x, k=5)
                _, _, y_p = deriv(t,y, k=5)
                _, _, z_p = deriv(t,z, k=5)
                v_lisse = [m.sqrt(x_p[i]**2+y_p[i]**2+z_p[i]**2) for i in range(len(x_p))]

                # Calcul de la vitesse utilisant la methode de derviation naive
                x_p_naif=[(x[i+1]-x[i])/(t[i+1]-t[i]) for i in range(len(z)-1)]
                z_p_naif=[(z[i+1]-z[i])/(t[i+1]-t[i]) for i in range(len(z)-1)]
                y_p_naif=[(y[i+1]-y[i])/(t[i+1]-t[i]) for i in range(len(z)-1)]
                v_naif =[m.sqrt(x_p_naif[i]**2+y_p_naif[i]**2+z_p_naif[i]**2) for i in range(len(z)-1)]
                
                i_lisse = [i+3 for i in range(len(v_lisse))]
                i_2 = [i for i in range(len(v_naif))]
                route_info = pd.DataFrame(route_info)

                # Enregistrement des resultats pour chaque fichier dans un grand tableau 
                D.append([route_info, i_lisse[7:], v_lisse[7:], i_2, v_naif, ele_min_max, ele_gain_and_loss, number_of_tracks])
    return D       