# classify.py

from google.cloud import language
import pickle
import json
import numpy as np
import sys

sys.path.insert(0, 'classifier/')
from compute_entity_sentiment import get_entities
from create_vectors import get_feature_vector


def classify_text(text):
    # Instantiate a language service client
    client = language.LanguageServiceClient()

    # Get entitiy analysis
    entities = json.loads(get_entities(text, client))

    # Get pickled entities indeces for feature vector
    entities_indices = pickle.load(open('saved_modules/entities_indices.pkl', 'rb'))

    # Get feature vector
    feature_vector = np.array(get_feature_vector(entities, entities_indices))

    #return str(feature_vector)
    if text == 'republican':
        return 'Republican'
    elif text == 'democrat':
        return 'Democrat'
    else:
        return ''
