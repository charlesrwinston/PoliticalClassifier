# classifier.py
#
#   Classifier class for Political Classifer project
#   Charles Winston

import numpy as np
import tensorflow as tf

def input_fn_train(dataset):
   # manipulate dataset, extracting feature names and the label
   features = np.load('../data-files/features.npy')

   return feature_dict, label

def input_fn_test(dataset):
   # manipulate dataset, extracting feature names and the label
   # TODO
   return feature_dict, label

def input_fn_predict(dataset):
   # manipulate dataset, extracting feature names and the label
   # TODO
   return feature_dict, label

def get_model(train_set, test_set):
    # Define feature columns
    sentiment = tf.feature_column.numeric_column('sentiment')
    entities_categorical = tf.feature_column.categorical_column_with_hash_bucket('entities', 100000)
    entities_dense = tf.feature_column.embedding_column(entities_categorical, combiner='sqrtn', 10)

    # Instantiate an estimator, passing the feature columns.
    estimator = tf.estimator.Estimator.DNNClassifier(
        feature_columns=[sentiment, entities_dense],
        hidden_units=[1024, 512, 256])

    return estimator

def get_train_and_test_set(full_set):
    split = (len(full_set) / 10) * 9
    return full_set[:split], full_set[split:]

def get_full_set():


class Classifier:

    def __init__(self):
        self.full_set = get_full_set()
        self.train_set, self.test_set = get_train_and_test_set(self.full_set)
        self.model = get_model(self.train_set, self.test_set)

    def train(self):
        self.model.train(input_fn=input_fn_train, steps=100)

    def test(self):
        metrics = self.model.test(input_fn=input_fn_test, steps=100)

    def classify(self, text):
        prediction = self.model.predict(input_fn=input_fn_predict)
