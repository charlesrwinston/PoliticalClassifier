# test classifier

import numpy as np
import tensorflow as tf
from sklearn.decomposition import PCA


def input_fn_train():
    features = np.load('../data-files/train.npy')
    labels = np.load('../data-files/train_labels.npy')

    print(features.shape)
    print(labels.shape)

    feature_dict = {'entities' : features}
    return feature_dict, labels

def input_fn_test():
    features = np.load('../data-files/test.npy')
    labels = np.load('../data-files/test_labels.npy')

    feature_dict = {'entities' : features}
    return feature_dict, labels

def main():
    # Define feature columns
    entities = tf.feature_column.numeric_column('entities', shape=(20,))

    # Instantiate an estimator, passing the feature columns.
    estimator = tf.estimator.DNNClassifier(
        feature_columns=[entities],
        hidden_units=[512, 256])

    estimator.train(input_fn=input_fn_train, steps=2000)
    metrics = estimator.evaluate(input_fn=input_fn_test, steps=2000)
    print(metrics)

def test():
    features_input = np.load('../data-files/features.npy')

    features = features_input[10:, :-1]
    print(features.shape)
    labels = features_input[:10, -1:]
    print(labels.shape)
    return
    pca = PCA(n_components=20)
    features = pca.fit_transform(features)
    print(features.shape)

if __name__ == '__main__':
    main()
