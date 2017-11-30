# entity_sentiment.py
import sys
import json
from google.cloud.language import LanguageServiceClient, enums, types

def analysis(text):
    # Instantiates a client
    client = LanguageServiceClient()

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

    for entity in analysis_result.entities:
        current_ent = {
            'name'      :   entity.name,
            'mentions'  :   [],
        }
        if current_ent['name'] in raw_ents:
            for mention in entity.mentions:
                current_ent['mentions'].append({
                    'begin_offset'  :   mention.text.begin_offset,
                    'content'       :   mention.text.content,
                    'magnitude'     :   mention.sentiment.magnitude,
                    'sentiment'     :   mention.sentiment.score,
                    'type'          :   mention.type,
                })
            current_ent['salience'] = entity.salience
            current_ent['magnitude'] = entity.sentiment.magnitude
            current_ent['sentiment'] = entity.sentiment.score
            current_ent['wikipedia_url'] = raw_ents[current_ent['name']]['wikipedia_url']
            final_result.append(current_ent)

    #print(json.dumps(final_result))
    return final_result

def main():
    text = sys.argv[1]
    analysis(text)

if __name__ == "__main__":
    main()
