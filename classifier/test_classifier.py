# test classifier

import numpy as np
import tensorflow as tf
from sklearn.decomposition import PCA

SHAPE = 20

feature_spec = {'entities': tf.FixedLenFeature(SHAPE, tf.float32)}
'''
def serving_input_receiver_fn():
  """An input receiver that expects a serialized tf.Example."""
  serialized_tf_example = tf.placeholder(dtype=tf.float64,
                                         shape=(SHAPE,),
                                         name='input_example_tensor')
  receiver_tensors = {'examples': serialized_tf_example}
  features = tf.parse_example(serialized_tf_example, feature_spec)
  return tf.estimator.export.ServingInputReceiver(features, receiver_tensors)
'''
def input_fn_train():
    # Load numpy arrays
    features = np.load('data-files/train.npy')
    labels = np.load('data-files/train_labels.npy')

    # Convert to Tensors
    features = tf.convert_to_tensor(features)
    labels = tf.convert_to_tensor(labels)

    print(features.shape)
    print(labels.shape)

    feature_dict = {'entities' : features}
    return feature_dict, labels

def input_fn_test():
    features = np.load('data-files/test.npy')
    labels = np.load('data-files/test_labels.npy')

    # Convert to Tensors
    features = tf.convert_to_tensor(features)
    labels = tf.convert_to_tensor(labels)

    print(features.shape)
    print(labels.shape)

    feature_dict = {'entities' : features}
    return feature_dict, labels

def main():
    # Define feature columns
    entities = tf.feature_column.numeric_column('entities', shape=(SHAPE,))

    # Instantiate an estimator, passing the feature columns.
    estimator = tf.estimator.DNNClassifier(
        feature_columns=[entities],
        hidden_units=[128, 64],
        n_classes=2)

    # Train model
    estimator.train(input_fn=input_fn_train, steps=2000)

    # Test model
    metrics = estimator.evaluate(input_fn=input_fn_test, steps=2000)
    print(metrics)

    # Save model
    estimator.export_savedmodel('./saved_modules', tf.estimator.export.build_parsing_serving_input_receiver_fn(feature_spec))

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
