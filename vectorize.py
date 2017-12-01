# vectorize.py
# spark job

import pyspark
from google.cloud import language
import json
#from entity_sentiment2 import EntitySentiment

def main():
    # Get bucket and project id
    bucket = 'political-classifier-bucket'

    # Instantiates a language client
    client = language.LanguageServiceClient()

    sc = pyspark.SparkContext()
    rdd = sc.textFile('twitter_data.csv')
    def map_func(text):
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

        return final_result[0][0]['name']

    id_length = 18

    rdd = rdd.map(lambda line: (line[:id_length], line[19:(len(line) - 2)], line[(len(line) - 1):]))
    def test(text):
        document = types.Document(
            content=text,
            type=enums.Document.Type.PLAIN_TEXT)
        analysis_result = client.analyze_entity_sentiment(document)
        return analysis_result

    rdd = rdd.map(lambda triple: (triple[0], triple[2], map_func(triple[1])))
    print(rdd.collect())

    # Set the configuration for importing data from BigQuery.
    # Specifically, make sure to set the project ID and bucket for Cloud Dataproc,
    # and the project ID, dataset, and table names for BigQuery.
    '''
    conf = {
        # Input Parameters
        "mapred.bq.project.id": project,
        "mapred.bq.gcs.bucket": bucket,
        "mapred.bq.temp.gcs.path": input_directory,
        "mapred.bq.input.project.id": project,
        "mapred.bq.input.dataset.id": "political_data",
        "mapred.bq.input.table.id": "twitter_data"
    }
    '''

    # Read the data from BigQuery into Spark as an RDD.
    #table_data = pyspark.SparkContext.newAPIHadoopRDD("com.google.cloud.hadoop.io.bigquery.JsonTextBigQueryInputFormat", "org.apache.hadoop.io.LongWritable", "com.google.gson.JsonObject", conf=conf)

    # Extract the JSON strings from the RDD.
    #table_json = table_data.map(lambda x: x[1])
    #print(table_json)


if __name__ == '__main__':
    main()
