"""
Afin de construire un modèle de corrélation entre la vitesse et la pente, ce module nous fournit
une régression par un réseau de neurones 
"""

import numpy as np
from tensorflow import keras
from scipy import stats
from torch import softmax
from model_analysis import error, rem_outliers

# Lire les données d'analyse enregistrées dans le fichier npy
D, coordinates, Cols = np.load('./Extracted_data/Data.npy', allow_pickle='TRUE')

# On ne prend que les donnees dont on aura besoin
_, t, Vitesse_lise_Y, _, _, _, _, _, _, Xgrad, Ygrad, _, _, _= D[0]

print(len(Vitesse_lise_Y), len(Ygrad))

x_data =np.array(Ygrad)
y_data =np.array(Vitesse_lise_Y)

print(len(x_data), len(y_data))


# Création du modèle
model = keras.Sequential()
model.add(keras.layers.Dense(units = 1, activation = 'linear', input_shape=[1]))
model.add(keras.layers.Dense(units = 64, activation = 'relu'))
model.add(keras.layers.Dense(units = 64, activation = 'relu'))
model.add(keras.layers.Dense(units = 1, activation = 'linear'))

model.compile(loss='mse', optimizer="SGD")

# Affichage d'un résumé
model.summary()


# Entrainement sur la data du fichier gpx orux
model.fit( x_data, y_data, epochs=60, verbose=1)


# Valeurs predites pour un interval donné
y_predicted = model.predict(np.linspace(-10, 16, 200))

# Calcule d'ensemble des erreurs pour ce modele pour chacun des fichiers gpx
E = []
for i in D :
    X_pred = np.array(i[-4])
    Y_true = np.array(i[2])
    Z1 = stats.zscore(Y_true)
    Z2 = stats.zscore(X_pred)
    new_Yp2, new_Yg = rem_outliers(Y_true, X_pred, Z1, Z2)
    Y_pred = model.predict(new_Yg)
    MSE, MAPE, R2 = error(new_Yp2, Y_pred)
    E.append([MSE[0], MAPE[0], R2])


# Enregistrement des erreurs par rapport a chaque trajet
np.save('./Extracted_data/NN_reg_jose.npy', E)
model.save('Model/NN_Model.h5')