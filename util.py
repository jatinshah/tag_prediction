import csv
import hashlib
import cPickle as pickle
import os.path
import bs4
import re


def process_input(file_name, file_type='train'):

    """
    Process input files by removing HTML tags, lower casing
    and removing non-alphanumeric characters.
    Store tokens in a pickled dictionary.
    Process tags & store a question hash & tokens in a dictionary

    :param file_name: name of the input file
    :param file_type: either 'train' or 'test'
    :return: none
    """

    input_file = open(file_name, 'r')
    file_reader = csv.reader(input_file)
    file_reader.next()  # Skip headers

    file_prefix = os.path.splitext(os.path.basename(file_name))[0]
    output_file = open('data/' + file_prefix + '_tokens.csv', 'w')
    output_writer = csv.writer(output_file, quoting=csv.QUOTE_ALL)

    tokens_map = {}
    tags_map = {}
    i = 0

    for row in file_reader:
        # Track
        i += 1
        if i % 10000 == 0:
            print "Processing question: " + str(i)

        question_id = row[0]

        question = row[1].lower()
        question_hash = hashlib.sha1(question).hexdigest()

        body = row[2].lower()

        # For predicting tags of duplicate questions
        if file_type == 'train':
            tags = row[3].split()
            if question_hash in tags_map:
                tags_map[question_hash] = list(set(tags_map[question_hash] + tags))
            else:
                tags_map[question_hash] = tags

        # Pre-processing input
        # Remove HTML tags from body
        body = ' '.join([text for text in bs4.BeautifulSoup(body).stripped_strings])
        # Remove all non-alphanumeric characters
        body = re.sub('[^A-Za-z0-9+#]+', ' ', body)

        output_writer.writerow([question_id, body])

    if file_type == 'train':
        with open('data/' + file_prefix + '_tags.dict', 'wb') as f:
            pickle.dump(tags_map, f)

    input_file.close()
    output_file.close()

process_input('data/Train40K.csv')
