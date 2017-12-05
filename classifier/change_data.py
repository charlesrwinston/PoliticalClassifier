# change_data.py
import json
fin = open('../data-files/tweets1.txt', 'r')
fout = open('../data-files/tweets_new.txt', 'w')
tweets_input = json.loads(fin.read())
for label in tweets_input:
    # ignore independents for now
    if label != 'I':
        for user in tweets_input[label]:
            for tweet in tweets_input[label][user]:
                fout.write(label + ' ' + tweet.replace('\n', ' ') + '\n')
