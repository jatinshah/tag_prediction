import csv
import hashlib
import cPickle as pickle
import bs4
import re

# Load training  & test data
training_file = 'data/Train40K.csv'
train_reader = csv.reader(open(training_file, 'r'))
train_reader.next()     # Skip headers

# Training
tags_map = {}
for row in train_reader:
    question_id = row[0]
    question = row[1].lower()
    body = row[2].lower()
    tags = row[3].split()

    question_hash = hashlib.sha1(question).hexdigest()

    # Questions & tags for predicting tags of duplicate questions
    # in test set
    if question_hash in tags_map:
        tags_map[question_hash] = list(set(tags_map[question_hash] + tags))
    else:
        tags_map[question_hash] = tags

    # Pre-processing
    # Remove HTML tags from body
    body = ' '.join([text for text in bs4.BeautifulSoup(body).stripped_strings])
    # Remove all non-alphanumeric characters
    body = re.sub('[^A-Za-z0-9+#]+', ' ', body)

    #TF-IDF Computation


# Write tags dictionary to file
with open('data/question_tag.dict', 'wb') as f:
    pickle.dump(tags_map, f)

