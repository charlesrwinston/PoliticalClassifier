# twitter_data.py
#
#   Module responsible for getting all the twitter data
#   Charles Winston

# Import dependencies
import json
from google.cloud.bigtable.client import Client
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
    f = open('tweets1.txt', 'w')
    tweets = { 'R': {}, 'D': {}, 'I': {} }
    for user in senators:
        screen_name = user[0]
        party = user[1]
        result = twitter.statuses.user_timeline(screen_name=screen_name, count=TWEET_COUNT)
        tweets[party][screen_name] = result
        for tweet in result:
            f.write(party + '\t' + screen_name + '\t' + json.dumps(tweet) + '\n\n')
'''
    # Initialize a database to store the twitter data
    client = Client(project='political-classifier', admin=True)
    instance = client.instance('political-classifier-instance')
    table = instance.table('tweet-table')
    table.create()
    screen_name_column = table.column_family('screen_name')
    screen_name_column.create()
    tweet_column = table.column_family('tweet')
    tweet_column.create()
    label_column = table.column_family('label')
    label_column.create()

    # Add each tweet to the Google Cloud Bigtable database
    for party in tweets:
        for screen_name in tweets[party]:
            i = 0   # row key iterator
            for tweet in tweets[party][screen_name]:
                row_key = screen_name + str(i)
                row = table.row(row_key)
                # Set cells for each column
                row.set_cell('screen_name', screen_name_column, screen_name)
                row.set_cell('tweet', tweet_column, json.dumps(tweet))
                row.set_cell('label', label_column, party)
                row.commit()
'''


if __name__ == '__main__':
    main()
