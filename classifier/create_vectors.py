# create_vectors.py
#
#   Reads from BigQuery database of tweets, uses entities entry to create
#   feature vectors for classifier
#
#   Charles Winston
#   Political Classifier

from google.cloud import bigquery
from random import shuffle
import numpy as np
import json
import operator


def create_vectors():
    # Instantiate a BigQuery client
    bigquery_client = bigquery.Client(project='political-classifier')

    # Query database to get all records
    query = """
        #standardSQL
        SELECT *
        FROM political_data.tweet_entities;
        """
    query_job = bigquery_client.query(query)
    results = query_job.result()    # API call
    print('Results recieved')       # Log

    # Keep track of all unique entities in order to create an index for each
    # entity in the feature vector
    entities_count = {}
    ents_and_labels = []
    for row in results:
        # Convert json string to object in Python
        #print(row.entities)
        entities = json.loads(str(row.entities))
        ents_and_labels.append((entities, row.label))
        for ent in entities:
            # Add to count
            if ent['id'] not in entities_count:
                entities_count[ent['id']] = 1
            else:
                entities_count[ent['id']] += 1

    entities_index = {}
    for ent_id in entities_count:
        # Add entity to dict if new
        if entities_count[ent_id] > 1:
            entities_index[ent_id] = len(entities_index)

    #for ent_id in entities_index:
    #    print(ent_id + ' ' + str(entities_count[ent_id]))
    # Now that we have a dictionary that maps entities to indeces,
    # we can create the vectors
    feature_vector_length = len(entities_index) * 2
    features = []
    #for ent_id, count in sorted(entities_count.items(), key=operator.itemgetter(1)):
    #    print('{}:\t{}'.format(ent_id, count))
    for pair in ents_and_labels:
        # Get values from pair of entities and label
        entities = pair[0]
        label = pair[1]

        # Convert json string to object in Python
        entities = json.loads(row.entities)

        # Get feature and label vectors and append to feature list
        feature_vector = get_feature_vector(entities, entities_index, feature_vector_length)
        label_vector = get_label_vector(label)
        #print(feature_vector)
        feature_vector.append(label_vector)
        features.append(feature_vector)

    shuffle(features)

    # Save feature list as numpy array
    features = np.array(features)
    np.save(open('../data-files/features.npy', 'wb'), features)


def get_feature_vector(current_entities, entities_index, length):
    feature_vector = [0 for i in range(length)]
    for ent in current_entities:
        if ent['id'] in entities_index:
            sentiment = ent['score']
            magnitude = ent['magnitude']
            salience = ent['salience']
            ent_id = ent['id']
            ent_index = entities_index[ent_id]

            feature_vector[ent_index] = salience * 10
            feature_vector[ent_index + 1] = sentiment * magnitude * 10

    #print(feature_vector)
    return feature_vector

def get_label_vector(label_string):
    if label_string == 'R':
        return 1
    elif label_string == 'D':
        return 0
    else:
        exit('Error: Not a label')


if __name__ == '__main__':
    create_vectors()
