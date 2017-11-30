# create_data.py

from google.cloud.language import LanguageServiceClient, enums, types
import numpy as np
import json
import entity_sentiment



def get_feature_vector(current_entities, entities_dict, length):
    feature_vector = np.zeroes(length)
    for ent in current_entities:
        sentiment = ent['sentiment']
        magnitude = ent['magnitude']
        salience = ent['salience']
        ent_id = ent['id']
        ent_index = entities_dict[ent_id]

        if sentiment > 0.0:
            feature_vector[ent_index + 1] = sentiment * magnitude * saliance * 10
        else:
            feature_vector[ent_index] = sentiment * magnitude * saliance * 10

    return feature_vector

def get_label_vector(label_string):
    if label_string == 'R':
        return np.ndarray([0, 1])
    elif label_string == 'D':
        return np.ndarray([1, 0])
    else:
        exit('Error: Not a label')

def create_vectors():
    # Read in data and convert to json
    tweets_file = open('tweets1.txt', 'r')
    tweets_input = json.loads(tweets_file.read())

    tweets = []
    entities_dict = {}

    for label in tweets_input:
        # ignore independents for now
        if label != 'I':
            for user in tweets_input[label]:
                for tweet in tweets_input[label][user]:
                    # Get the entity sentiment of tweet
                    current_entities = entity_sentiment.analysis(tweet)

                    # Modify entities
                    for ent in current_entities:
                        #del ent['mentions'] # unnecessary for our purposes

                        # If not recognized on Wikipedia, simply map with name string (lowercase).
                        # However, if it is on wikipedia, map with link. This eliminates buggy
                        # different name tags for same entities from Google API.
                        if ent['wikipedia_url'] == '-':
                            ent['name'] = ent['name'].lower()
                            if ent['name'].lower() not in entities_dict:
                                entities_dict[ent['name'].lower()] = len(entities_dict)
                            ent['id'] = ent['name'].lower() # Add definite id
                        else:
                            if ent['wikipedia_url'] not in entities_dict:
                                entities_dict[ent['wikipedia_url']] = len(entities_dict)
                            ent['id'] = ent['wikipedia_url'] # Add definite id

                    print(label + '\n' + str(current_entities) + '\n' + tweet + '\n\n')
                    tweets.append((tweet, label, current_entities))

    feature_vector_length = len(entities_dict) * 2
    features = []
    print(entities_dict)

    result_file = open('tweet_result.txt', 'w')

    for tweet in tweets:

        text = tweet[0]
        label = tweet[1]
        entities = tweet[2]

        feature_vector = get_feature_vector(entities, entities_dict, feature_vector_length)
        label_vector = get_label_vector(label)

        result_file.write(label + '\n' + str(entities) + '\n' + text + '\n\n')

        features.append(feature_vector, label_vector)

    shuffle(features)

    np.save(open('features.npy', 'w'), np.ndarray(features))


if __name__ == '__main__':
    create_vectors()
