"""Prédire le temps de parcours d'un trajet donné a partir du modele construit du reseau de neurones"""


import sys
from pathlib import Path
file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

import numpy as np


def predict(j, model):
    """
    Parametres :
                 - j : l'indice du trajet qu'on veut Prédire son temps
                 - model : le modele NN
    Sortie [T_réel, T_pred] :
                             - T_réel : le temps du trajet réel pris du fichier gpx
                             - T_pred : le temps estimé           
    
    """

    # lire les données du trajet donné
    D, _, _ = np.load('./Extracted_data/Data.npy', allow_pickle='TRUE')
    # Extraire la pente, l'ensemble des coordonées x, y, z
    route_Df = D[j][0]
    Pente = D[j][-4]
    X = list(route_Df['x'])
    Y = list(route_Df['y'])
    Z = list(route_Df['new_elevation'])
    
    # Calculer la difference de distance entre chaque deux points
    Distances = []
    Distances0 = []
    for i in range(len(X)-1) :
        d = ((X[i+1]-X[i])**2+(Y[i+1]-Y[i])**2+(Z[i+1]-Z[i])**2)**0.5
        # remove spike values
        if i >=1 and d>3*(10+Distances[-1]) :
            Distances.append(Distances[-1])
        else :    
            Distances.append(d)   
        Distances0.append(d)    

    Distances = np.array(Distances)

    # Prédir la vitesse en chaque point en fonction de la Pente
    Speed = model.predict(Pente)    
    Speed = np.array([i[0] for i in Speed])

    # Calculer le temps de chaque portion du trajet et sommer pour obtenir le temps total
    Distances = Distances[8:-8]/Speed
    Time = sum(Distances)

    # Calculer le temps réel d'apres les données extraites du fichier gpx
    T = list(route_Df['time'][8:-8])


    # Comparing with naive time 
    dis = sum(Distances0)
    Vmoy = sum(D[4][2])/len(D[4][2])
    naive_time = dis/Vmoy

    return round(abs(T[0]-T[-1]), 2), int(round(Time,2)), int(naive_time)