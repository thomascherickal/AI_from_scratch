"""
This script is created by Njad Nissi 2024.02.28
Weight estiomation/approximation for linear data sets
y_pred = w . x
 Where:
 ->> y_pred is the predicted y to be tested agains the true y
 ->> w is the estimated weight that aims to minimize the 
 distance between the prediction and the exact value
 mean_squared_error d = (y - y_pred)^2, the lesser the better

  b: bias
"""

import random as rnd

EPSILON = .001 # epsilon
lr = .001 # learning rate

# dataset1 : y = 2x + .5
dataset1 = [
    (0, 0.5),
    (1, 2.5),
    (2, 4.5),
    (3, 6.5),
    (4, 8.5),
    (5, 10.5)
]

# dataset2 : y = -2x + 1
dataset2 = [
    (0, 1),
    (1, -1),
    (2, -3),
    (3, -5),
    (4, -7),
    (5, -9)
]

dataset = dataset2

def mse(w, b, X=dataset):
    cost = 0
    for x in X:
        y = x[0] * w + b
        error = (x[1] - y) ** 2
        cost += error

    return cost / len(X)


def grad(w, b):
    global EPSILON # epsilon
    m2e = mse(w, b)
    dw = (mse(w + EPSILON, b) - m2e) / EPSILON
    db = (mse(w, b + EPSILON) - m2e) / EPSILON
    return w - lr * dw, b - lr * db # minimization on the opposite direction of the gradient


def train(w0, b0, iters, X=dataset):
    w = w0
    b = b0
    m2e = 100
    for _ in range(iters):
        m2e = mse(w, b)
        print(f'{w}\t\t{b}\t\t{m2e}')
        w, b = grad(w, b)
    
    return w, b, m2e


activation = lambda x: round(x)


if __name__=="__main__":
    w0 = rnd.random() * 10 # Initial Weight: start with a guess from 0-10
    b0 = rnd.random() * 5 # Initial bias: start with a guess from 0-5
    print('\tWEIGHT\t\t\t\tBIAS\t\t\t\tERROR', '\n', '-*-'*30)
    w, b, m2e = train(w0, b0, 500)
    w = activation(w)
    print(f"Prediction: w={w}, b={b} with mse={m2e}")
