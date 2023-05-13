# coding:utf-8
import sys
from PIL import Image
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import os


def load_dataset():
    X = []
    y = []

    for i in range(60):
        path = "./services/CSDN/dataset/%d%d.png" % (i / 6, i % 6 + 1)
        pix = np.array(Image.open(path).convert("L"))
        # print(pix.reshape(8*20).shape)
        X.append(pix.reshape(8*20))
        y.append(int(i/6))
    return np.array(X), np.array(y)


def split_letters(img):
    pix = np.array(img.convert("L").resize((48, 20)))
    # threshold image
    pix = (pix > 100) * 255

    col_ranges = [
        [5, 5 + 8],
        [14, 14 + 8],
        [23, 23 + 8],
        [32, 32 + 8]
    ]
    letters = []
    for col_range in col_ranges:
        letter = pix[:, col_range[0]: col_range[1]]
        letters.append(letter.reshape(8*20))
    return letters

def predict(img):
    letters = split_letters(img)

    X, y = load_dataset()
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(X, y)

    return ''.join([str(pred) for pred in knn.predict(letters)])