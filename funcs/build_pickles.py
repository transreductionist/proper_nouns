from nltk.corpus import wordnet as wn
from proper_noun_original.funcs.utilities import FIRST_NAMES_PATHS
from proper_noun_original.funcs.utilities import SURNAMES_PATHS
from proper_noun_original.funcs.utilities import WORDS_PATHS
from proper_noun_original.funcs.utilities import read_csv
from proper_noun_original.funcs.utilities import get_longest_item
from proper_noun_original.funcs.utilities import dump_data_to_pickle


def build_first_name_data():
    print('\n***** Build first names.')
    first_name_data = read_csv(FIRST_NAMES_PATHS['csv'], FIRST_NAMES_PATHS['columns'])
    max_length_first_name = get_longest_item(first_name_data)
    dump_data_to_pickle(FIRST_NAMES_PATHS['pkl'], first_name_data, max_length_first_name)


def build_surname_data():
    print('***** Build surnames.')
    surname_data = read_csv(SURNAMES_PATHS['csv'], SURNAMES_PATHS['columns'])
    max_length_surname = get_longest_item(surname_data)
    dump_data_to_pickle(SURNAMES_PATHS['pkl'], surname_data, max_length_surname)


def build_word_data():
    print('***** Build words.\n')
    words = []
    for word in wn.words():
        words.append(word)
    max_length_word = get_longest_item(words)
    dump_data_to_pickle(WORDS_PATHS['pkl'], words, max_length_word)
