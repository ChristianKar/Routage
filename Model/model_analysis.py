"""
Ensemble des fonctions qui servent à analyser le modèle de corrélation
"""

import numpy as np
from sklearn.metrics import r2_score

def Pol_regression(x, y, d):
    # Effectue une regression polynômiale de degré d pour trouver un modèle de correlation.
    # Cette régression n'est pas pertinente puisqu'elle va diverger en dehors de l'intervalle des données d'entrainement,
    # mais elle reste un outil de référence et de comparaison avec les autres modèles dans l'intervalle de travail.
    """
    Input:
           - x : pente
           - y : vitesse
           - d : degre du polynome

    Ouput:
           - beta : coefficients du polynome
    """
    X = np.array([x])
    Y = np.array(y)
    # Calcul des paramètres du polynôme avec la méthode des moindres carrés
    Xm = np.concatenate(tuple(X**i for i in range(d)),axis = 0)
    beta1 = np.linalg.inv(np.dot(Xm, Xm.T))
    beta2 = np.dot(Xm, Y.T)
    beta = np.dot(beta1, beta2)
    return beta 

def rem_outliers(X, Y, z_score1, z_score2):
    """
    Input: 
           - X : tableau des abscisses
           - Y : tableau des ordonnees 
           - z_score1 : le score z des points de X
           - z_score2 : le score z des points de Y

    Ouput: 
           - New_X : X sans outliers 
           - New_Y : Y sans ouliers
    
    """
    # Afin de bien calculer les erreurs MSE et MAPE il faut eliminer les points outliers qui ont 
    # un score z superieur à la normale et les points de vitesse nulle

    New_X = []
    New_Y = []
    for i in range(len(z_score1)) :
        if abs(z_score1[i])<2.9 and abs(z_score2[i])<2.9 and X[i] >0.2:
            New_X.append(X[i])
            New_Y.append(Y[i])
    return np.array(New_X), np.array(New_Y)

def error(Y_true, Y_model) :
    # Calcul de l'erreur entre le modele et l'observation

    """
    Input: 
           - Y_true : valeurs reelles 
           - Y_model : images par le modele

    Ouput: 
           - MSE, MAPE, R2
    """
    MSE = 0
    MAPE = 0
    n = len(Y_true)
    for i in range(n):
        MSE += (Y_true[i]-Y_model[i])**2
        MAPE += abs((Y_true[i]-Y_model[i])/Y_true[i])
    return (MSE/n), (MAPE/n), r2_score(Y_true, Y_model)

def sigmoid(x, K, Beta_1, Beta_2):
    # Fonction sigmoid
    res = K / (1 + np.exp(-Beta_1*(-x-Beta_2))) 
    return res    

def Func(beta, xj):
    # Fonction polynomiale
    y = 0
    for i in range(len(beta)):
        y += (beta[i])*(xj**i) 
    return y       