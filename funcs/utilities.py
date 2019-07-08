"""A collection of constants and utility functions."""

import copy
import csv
import nltk
import pickle
import re
import string
from statistics import mean
from statistics import median

FIRST_NAMES_PATHS = {
    'csv': 'data/archive/csv/first_names_ssa.csv',
    'pkl': 'data/pickles/first_names_ssa.pkl',
    'pkl_cnts': 'data/pickles/first_names_cnts.pkl',
    'pkl_cnts_norm': 'data/pickles/first_names_cnts_normalized.pkl',
    'columns': [0]
}

SURNAMES_PATHS = {
    'csv': 'data/archive/csv/surnames_2010_census.csv',
    'pkl': 'data/pickles/surnames_2010_census.pkl',
    'pkl_cnts': 'data/pickles/surnames_cnts.pkl',
    'pkl_cnts_norm': 'data/pickles/surnames_cnts_normalized.pkl',
    'columns': [0]
}

WORDS_PATHS = {
    'pkl': 'data/pickles/words.pkl',
    'pkl_cnts': 'data/pickles/words_cnts.pkl',
    'pkl_cnts_norm': 'data/pickles/words_cnts_normalized.pkl'
}

SENTENCES_PATH = {
    'txt': 'data/sentences/test_sentences.txt'
}

IP_REGEX = re.compile(r'\b(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\b')


def download_required_nltk_packages(quiet=True):
    """Some required nltk packages."""

    nltk.download('punkt', quiet=quiet)
    nltk.download('averaged_perceptron_tagger', quiet=quiet)
    nltk.download('maxent_ne_chunker', quiet=quiet)
    nltk.download('words', quiet=quiet)


def get_all_census_names():
    """Return the set of all first and surnames from the US 2010 Census."""

    first_names = load_pickle(FIRST_NAMES_PATHS['pkl'])
    surnames = load_pickle(SURNAMES_PATHS['pkl'])
    return set(first_names['data']).union(set(surnames['data']))


def parse_census_counts(census_counts, census):
    """Tally counts obtained from the Census method."""

    no_names = True
    if census_counts['truth_names'] != 0:
        census['truth_names'] += census_counts['truth_names']
        no_names = False
    if census_counts['difference'] != 0:
        no_names = False
        census['difference'] += census_counts['difference']
    if no_names:
        census['no_names'] += 1


def parse_ner_counts(ner_counts, tagged):
    """Tally counts obtained from the Named Recognition Entity method."""

    no_names = True
    if ner_counts['truth_names'] != 0:
        tagged['truth_names'] += ner_counts['truth_names']
        no_names = False
    if ner_counts['test_names'] != 0:
        tagged['test_names'] += ner_counts['test_names']
        no_names = False
    if ner_counts['tagged_minus_test'] != 0:
        tagged['tagged_minus_test'] += ner_counts['tagged_minus_test']
        no_names = False
    if ner_counts['test_minus_tagged'] != 0:
        tagged['test_minus_tagged'] += ner_counts['test_minus_tagged']
        no_names = False
    if ner_counts['truth_names'] == 0:
        no_names = True
    if no_names:
        tagged['no_names'] += 1


def find_ip_addresses_regex(sentence):
    """Return all IP addresses in the given sentence."""

    return IP_REGEX.findall(sentence)


def read_txt(file_path):
    """Read in a text file."""

    with open(file_path, 'r') as file_pointer:
        return file_pointer.read().splitlines()


def read_csv(file_path, columns, header=True):
    """Read in a CSV file."""

    is_name = is_name_in_filepath(file_path)
    with open(file_path, 'r') as file_pointer:
        reader = csv.reader(file_pointer)
        if header:
            next(reader)
        return read_csv_data(reader, columns, is_name)


def read_csv_data(reader, columns, is_name):
    """Given a CSV reader read/condition the data."""

    data = []
    for row in reader:
        if is_name:
            data_item = map(lambda i: row[i].lower(), columns) if len(columns) > 1 else row[columns[0]].title()
        else:
            data_item = map(lambda i: row[i].lower(), columns) if len(columns) > 1 else row[columns[0]]
        data.append(data_item)
    return data


def is_name_in_filepath(file_path):
    """Determine if a file is one of the Census files."""

    if 'first_names' in file_path or 'surnames' in file_path:
        return True
    return False


def get_longest_item(items):
    """Given a list of items find the longest one."""

    max_length = 0
    for item in items:
        if len(item) > max_length:
            max_length = len(item)
    return max_length


def dump_data_to_pickle(file_path, data, max_length=None):
    """Dump data to a Python pickle."""

    if max_length:
        data_dump = {'data': data, 'max_length': max_length}
    else:
        data_dump = {'data': data}
    with open(file_path, 'wb') as fp:
        pickle.dump(data_dump, fp)


def load_pickle(file_path):
    """Load data from a Python pickle."""

    with open(file_path, 'rb') as fp:
        return pickle.load(fp)


def initialize_counts(max_length):
    """Initialize the counts dictionary for counting frequency of characters."""

    counts = {}
    for i in range(0, max_length):
        counts[i] = {}
        for ch in list(string.printable):
            counts[i][ch] = 0
    return counts


def get_counts(data):
    """Get frequency data for characters given position in word."""

    max_length = data['max_length']
    counts = initialize_counts(max_length)
    for i in range(0, max_length):
        for item in data['data']:
            if item == 'all other names':
                continue
            chrs = list(item)
            if len(chrs) <= i:
                continue
            counts[i][chrs[i]] += 1
    return counts


def normalize_counts(counts0):
    """Normalize the frequency data for characters given position in word."""

    counts1 = copy.copy(counts0)
    for position0, chr_count0 in counts0.items():
        total0 = sum(chr_count0.values())
        for chr0, cnt0 in chr_count0.items():
            cnt1 = cnt0 / total0
            counts1[position0][chr0] = cnt1
    return counts1


def multiply(x, y):
    """Function used for reduce."""

    return x * y


def tokenize_string(text):
    """Use NLTK to tokenize a string"""

    tokens = nltk.word_tokenize(text)
    return nltk.pos_tag(tokens)


def get_tagset(tagset_name, regex=None):
    """Return a tagset given a regex, e.g. NN.*"""

    return getattr(nltk.help, tagset_name)(regex)


def print_frequencies(title, names, name_probs, word_probs):
    """Print word and name frequencies."""

    print(title)
    print('Length of name list: {}\n'.format(len(names)))
    print('Names Statistics')
    print('    Names\n        min: {}    mean: {}    median: {}    max: {}'.format(
            min(name_probs[0]),
            mean(name_probs[0]),
            median(name_probs[0]),
            max(name_probs[0])
        )
    )
    print('    Words\n        min: {}    mean: {}    median: {}    max: {}'.format(
            min(word_probs[0]),
            mean(word_probs[0]),
            median(word_probs[0]),
            max(word_probs[0])
        )
    )
    print('\nIndividual name statistics:')
    print('    Names\n        min: {}    mean: {}    median: {}    max: {}'.format(
            min(name_probs[1]),
            mean(name_probs[1]),
            median(name_probs[1]),
            max(name_probs[1])
        )
    )
    print('    Words\n        min: {}    mean: {}    median: {}    max: {}'.format(
            min(word_probs[1]),
            mean(word_probs[1]),
            median(word_probs[1]),
            max(word_probs[1])
        )
    )
    print('\n\n')
