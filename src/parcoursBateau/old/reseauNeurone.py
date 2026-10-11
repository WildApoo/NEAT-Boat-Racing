"""
descente de gradient
https://www.youtube.com/watch?v=a5xuJLFTC7o
https://www.youtube.com/watch?v=N9O0k-K03Tc
-------


https://www.youtube.com/watch?v=g8Y4HFdSyA8&t=98s

y = f(w*x+b)

w vecteur de portée
x vecteur d'entrée
b biais
f fonction d'activation


couche d'entré
couches cachées
couche de sortie



On travaille avec des perceptrons
Fonction de coût basée sur le fonction sugmoïde (sortie entre 0 et 1)

Pour trouver la valeur des points, on utilise le concept statistique de vraisemblance
"""
import random

import numpy as np
"""
forward propagation > prédiction (transformation linéaire puis fonction d'activation)
back propagation > trouver les poids
"""

###
# FORWARD PROPAGATION
###
def sigmoid(x):
    return 1/(1+np.exp(-x))

def hidden(X, W_1, b):
    return sigmoid(np.dot(W_1, X) + b)

def output(H, W_2, b):
    return sigmoid(np.dot(W_2.T, H) + b)    # .T c'est pour avoir la transposée

###
# BACK PROPAGATION
# Cette partie ne semble pas nous intéresser pour commencer
# notre projet
###
def delta_2(o, y):
    # return float((o - y) * o * (1 - o))
    return (o - y) * o * (1 - o)

def delta_1(W_2, h, d2):
    d1 = np.zeros(shape=(3, 1))
    for j in range(d1.shape[0]):    # .shape > taille de la matrice, ici on veut le nombre de ligne
        d1[j] = W_2[j] * d2 * h[j] * (1-h[j])
    return d1

def dJdW_2(h, d2):
    dj = np.zeros(shape=(3, 1))
    for j in range(dj.shape[0]):
        dj[j] = d2 * h[j]
    return dj

def dJdW_1(X, d1):
    dj = np.zeros(shape=(3, 2))
    for j in range(dj.shape[0]):    # pour chaque ligne
        for i in range(dj.shape[1]):    # pour chaque colonne
            # dj[j, i] = d1[j] * X[i]
            dj[j, i] = d1[j][0] * X[i][0]
    return dj


np.random.seed(42)
X = np.random.standard_normal(size=(2, 1)) # couche d'entrée
W_1 = np.random.standard_normal(size=(3, 2))    # matrice de poids entre la couche d'entrée et celle cachée
W_2 = np.random.standard_normal(size=(3, 1))    # matrice de poids entre la couche cachée et celle de sortie
b_1 = np.random.standard_normal(size=(3, 1))    # biais de la couche cachée
b_2 = random.normalvariate(mu=0, sigma=1)   # biais de la couche de sortie
y = random.normalvariate(mu=0, sigma=1)

# forward test

h = hidden(X, W_1, b_1) # couche cachée
o = output(h, W_2, b_2) # neurone de sortie

print(h)
print(o)
d2, djdb_2 = delta_2(o, y), delta_2(o, y)

d1, djdb_1 = delta_1(W_2, h, d2), delta_1(W_2, h, d2)



dj2 = dJdW_2(h, d2)
dj1 = dJdW_1(X, d1)

def train_model(X, W_1, W_2, b_1, b_2, y, alpha):
    # appel :
    # train_model(data, W_1, W_2, b_1, b_2, labels, alpha)
    for i in range(y.shape[0]):
        # forward prop
        h = hidden(X[i].reshape(-1, 1), W_1, b_1)
        o = output(h, W_2, b_2)

        # back prop
        d2, djdb_2 = delta_2(o, y[i]), delta_2(o, y[i])
        d1, djdb_1 = delta_1(W_2, h, d2), delta_1(W_2, h, d2)

        dj2 = dJdW_2(h, d2)
        dj1 = dJdW_1(X[i].reshape(-1, 1), d1)
        W_2 -= alpha * dj2
        W_1 -= alpha * dj1
        b_1 -= alpha * djdb_1
        b_2 -= alpha * djdb_2
    return W_1, W_2, b_1, b_2

def predict_model(X, W_1, W_2, b_1, b_2, y):
    y_hat = []
    for i in range(X.shape[0]):
        h = hidden(X[i].reshape(-1, 1), W_1, b_1)
        o = output(h, W_2, b_2)
        #y_hat.append(float(o))
        y_hat.append(o)
    return y_hat


from sklearn.datasets import make_circles
import seaborn as sns
import matplotlib.pyplot as plt

data, labels = make_circles(100000, noise=0.07, factor=0.1, random_state=42)
sns.scatterplot(x=data[:, 0], y=data[:, 1], hue=labels)
plt.show()


alpha = 0.001   # vitesse d'apprentissage, définie arbitrairement. Ne doit pas être trop importante
epochs = 50
print("avant la boucle")
for i in range(epochs):
    print(f"tour de boucle {i}")
    W_1, W_2, b_1, b_2 = train_model(data, W_1, W_2, b_1, b_2, labels, alpha)
    y_hat = predict_model(data, W_1, W_2, b_1, b_2, labels)

# y_hat = np.array(y_hat)
# y_hat = np.where(y_hat > 0.5,1, 0)

# ia
y_hat = np.array(y_hat).reshape(-1)
y_hat = (y_hat > 0.5).astype(int)

def accuracy(y_hat, y):
    good_pred = y_hat[y_hat == y]
    good_pred = np.ones_like(good_pred)
    return np.sum(good_pred)/len(y_hat)

def accuracy_ia(y_hat, y):
    # On aplatit les tableaux pour être sûr qu'ils ont la même forme (n,)
    y_hat = np.array(y_hat).flatten()
    y = np.array(y).flatten()
    # On compare et on calcule la moyenne des "True" (1)
    return np.mean(y_hat == y)

print(accuracy_ia(y_hat, labels))

plt.figure(figsize=(12, 8))
hh = .02
x_min, x_max = data[:, 0].min() - .5, data[:, 0].max() + .5
y_min, y_max = data[:, 1].min() - .5, data[:, 1].max() + .5
xx, yy = np.meshgrid(np.arange(x_min, x_max, hh),
                     np.arange(y_min, y_max, hh))

Z = np.array(predict_model(np.c_[xx.ravel(), yy.ravel()], W_1, W_2, b_1, b_2, labels))
Z = Z.reshape(xx.shape)

contour = plt.contourf(xx, yy, Z, alpha=0.8)
sns.scatterplot(x=data[:, 0], y=data[:, 1], hue=labels)
plt.colorbar(contour, label='y_hat value')
plt.title("Decision Boundary and y_hat Values")
plt.show()




