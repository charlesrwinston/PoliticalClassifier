# split_test_and_train.py
import numpy as np
import tensorflow as tf
from sklearn.decomposition import PCA

features_input = np.load('../data-files/features.npy')

features = features_input[:, :-1]
labels = features_input[:, -1:]

pca = PCA(n_components=20)
features = pca.fit_transform(features)

features_train = features[1750:]
print(features_train.shape)

labels_train = labels[1750:]
print(labels_train.shape)

np.save(open('../data-files/train.npy', 'wb'), features[:1750])
np.save(open('../data-files/train_labels.npy', 'wb'), labels[:1750])
np.save(open('../data-files/test.npy', 'wb'), features[1750:])
np.save(open('../data-files/test_labels.npy', 'wb'), labels[1750:])
