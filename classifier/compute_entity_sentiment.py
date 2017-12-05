# entity_sentiment.py
#
#   Reads from BigQuery database of tweets, anaylyzes entity sentiment using
#   Google Natural Language API, and updates database to include analysis
#
#   Charles Winston
#   Political Classifier

from google.cloud import language, bigquery
import sys
import json

# Adds entities to all records in bigquery database with given label
def main(label):
    # Instantiates language and bigquery clients
    language_client = language.LanguageServiceClient()
    bigquery_client = bigquery.Client(project='political-classifier')

    # Query database to get all records that have not been analyzed
    query = """
        #standardSQL
        SELECT text, tweet_id, label, entities
        FROM political_data.twitter_data
        WHERE entities IS NULL AND label='{}';
        """.format(label)
    query_job = bigquery_client.query(query)
    results = query_job.result()    # API call
    print('Results recieved')       # Log
    #print(len(list(results)))

    dataset = bigquery_client.dataset('political_data')
    table = dataset.table('tweet_entities')
    table = bigquery_client.get_table(table)

    new_rows = []
    count = 0
    for row in results:
        # Analyze entity sentiment
        ents = get_entities(row.text, language_client)
        count += 1
        print(count)
        print(ents)
        new_rows.append((row.tweet_id, ents, row.label))


        # Add new entities to table
        #query = """
        #    #standardSQL
        #    UPDATE political_data.tweet_entities
        #    SET entities = '{}'
        #    WHERE tweet_id='{}';
        #    """.format(ents, row.tweet_id)
        #query_job = bigquery_client.query(query)
        #results = query_job.result()    # API call

    errors = bigquery_client.create_rows(table, new_rows)  # API request
    print(errors)
    assert errors == []


def get_entities(text, client):
    # Initialize the document
    document = language.types.Document(
        content=text,
        type=language.enums.Document.Type.PLAIN_TEXT,
        language='en')

    # Raw entities
    entities = client.analyze_entities(document).entities

    # entity types from enums.Entity.Type
    entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
                   'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')

    final_result = []       # Final return list of entities
    raw_ents = {}           # Dictionary of raw entities with wikipedia url

    # Filter wikipedia articles from entities
    for entity in entities:
        current_ent = {
            'name'          :   entity.name,
            'type'          :   entity_type[entity.type],
            'salience'      :   entity.salience,
            'wikipedia_url' :   entity.metadata.get('wikipedia_url', '-'),
        }
        # Add to list of raw ents to check with later
        raw_ents[current_ent['name']] = current_ent

    analysis_result = client.analyze_entity_sentiment(document)
    entities_dict = {}

    for entity in analysis_result.entities:
        current_ent = {
            'name'      :   entity.name,
            'mentions'  :   [],
        }
        if current_ent['name'] in raw_ents:
            del current_ent['mentions'] # unnecessary for our purposes
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

            final_result.append(current_ent)

    return json.dumps(final_result)


if __name__ == '__main__':
    main(sys.argv[1])
