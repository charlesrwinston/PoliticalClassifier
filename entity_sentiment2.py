# entity_sentiment2.py

import sys
import json
from google.cloud.language import LanguageServiceClient, enums, types

class EntitySentiment:
    def __init__(self):
        self.test = 1

    def analyze(self, text, client):
        document = types.Document(
            content=text,
            type=enums.Document.Type.PLAIN_TEXT)

        # Raw entities
        entities = client.analyze_entities(document).entities

        # entity types from enums.Entity.Type
        entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
                       'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')

        final_result = []       # Final return list
        raw_ents = {}           # Dictionary of valid raw ents

        # Filter valid entities
        for entity in entities:
            print('hi')
            current_ent = {
                'name'          :   entity.name,
                'type'          :   entity_type[entity.type],
                'salience'      :   entity.salience,
                'wikipedia_url' :   entity.metadata.get('wikipedia_url', '-'),
            }

            # Don't add unless entity has wikipedia
            # if current_ent['wikipedia_url'] != '-':
            raw_ents[current_ent['name']] = current_ent

        analysis_result = client.analyze_entity_sentiment(document)
        entities_dict = {}

        for entity in analysis_result.entities:
            current_ent = {
                'name'      :   entity.name,
                'mentions'  :   [],
            }
            if current_ent['name'] in raw_ents:
                del ent['mentions'] # unnecessary for our purposes
                current_ent['salience'] = entity.salience
                current_ent['magnitude'] = entity.sentiment.magnitude
                current_ent['score'] = entity.sentiment.score
                current_ent['wikipedia_url'] = raw_ents[current_ent['name']]['wikipedia_url']

                # If not recognized on Wikipedia, simply map with name string (lowercase).
                # However, if it is on wikipedia, map with link. This eliminates buggy
                # different name tags for same entities from Google API.
                if current_ent['wikipedia_url'] == '-':
                    current_ent['name'] = current_ent['name'].lower()
                    current_ent['id'] = current_ent['name'].lower() # Add definite id
                else:
                    current_ent['id'] = current_ent['wikipedia_url'] # Add definite id
                if current_ent['id'] not in entities_dict:
                    entities_dict[current_ent['id']] = len(entities_dict)
                current_ent['index'] = entities_dict[current_ent['id']]

                final_result.append(current_ent)

        self.result = final_result

    def main():
        text = sys.argv[1]
        client = LanguageServiceClient()
        analysis(text)

if __name__ == "__main__":
    main()
