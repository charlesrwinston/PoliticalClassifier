# twitter_data.py
#
#   Module responsible for getting all the twitter data
#   Charles Winston

# Import dependencies
import json
from google.cloud import bigquery
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

# Import local libraries
import screen_names

# Variables that contains the user credentials to access Twitter API
ACCESS_TOKEN = '930879090420219905-nJTbPIePNkOBOlftvCehvZo8AAUi720'
ACCESS_SECRET = '6WVBLPUHHrfnMM9Bke7gHCEbOY7khDAoks0MVli7JTnGZ'
CONSUMER_KEY = 'H0qNtCOHBEKCARKL7rMxD34tW'
CONSUMER_SECRET = 'Hbxrr1YA5fAYdOeZATX7DUtcPTGrfd9PrwfFssatbAukCMJIEI'

# Other constants
TWEET_COUNT = 20    # number of tweets to grab from each user
R           = 0     # Tweet list index for dict of tweets for republicans
D           = 1     # Tweet list index for dict of tweets for democrats
I           = 2     # Tweet list index for dict of tweets for independents
SCREEN_NAME = 0     # Senator pair index for screen name
PARTY_LABEL = 1     # Senator pair index for party label


# Main procedure
def main():

    # Get authorization
    oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

    # Initiate the connection to Twitter Streaming API
    twitter = Twitter(auth=oauth)

    # Get list of senators' screen names
    senators = screen_names.senators

    # Create and populate a dictionary of three dictionaries of party users and tweets
    tweets = []
    for user in senators:
        print(user)
        screen_name = user[0]
        label = user[1]
        result = twitter.statuses.user_timeline(screen_name=screen_name, count=TWEET_COUNT)
        for tweet in result:
            if 'text' in tweet:
                tweets.append((tweet['id'], tweet['text'].replace('\n', ' '), label))

    # Initialize a BigQuery database to store the twitter data
    client = bigquery.Client(project='political-classifier')

    # Get the dataset
    dataset = None
    for inner_dataset in client.list_datasets():
        dataset = inner_dataset

    SCHEMA = [
        bigquery.SchemaField('tweet_id', 'STRING', mode='required'),
        bigquery.SchemaField('text', 'STRING', mode='required'),
        bigquery.SchemaField('label', 'STRING', mode='required'),
    ]

    tables = list(client.list_dataset_tables(dataset))
    table = tables[0]
    assert(table.table_id == 'twitter_data')

    errors = client.create_rows(table, tweets)  # API request
    assert(errors == [])
    print(errors)


if __name__ == '__main__':
    main()
