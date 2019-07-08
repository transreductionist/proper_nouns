"""Build counts for names and words."""

from proper_nouns.funcs.utilities import dump_data_to_pickle
from proper_nouns.funcs.utilities import FIRST_NAMES_PATHS
from proper_nouns.funcs.utilities import get_counts
from proper_nouns.funcs.utilities import load_pickle
from proper_nouns.funcs.utilities import normalize_counts
from proper_nouns.funcs.utilities import SURNAMES_PATHS
from proper_nouns.funcs.utilities import WORDS_PATHS


def build_first_name_counts():
    """Build first name counts."""

    print('\n***** Build first name counts.')
    first_names = load_pickle(FIRST_NAMES_PATHS['pkl'])
    counts_first = get_counts(first_names)
    counts_first_normalized = normalize_counts(counts_first)
    dump_data_to_pickle(FIRST_NAMES_PATHS['pkl_cnts'], counts_first)
    dump_data_to_pickle(FIRST_NAMES_PATHS['pkl_cnts_norm'], counts_first_normalized)


def build_surname_counts():
    """Build surname counts."""

    print('***** Build surname counts.')
    surnames = load_pickle(SURNAMES_PATHS['pkl'])
    counts_surname = get_counts(surnames)
    counts_surname_normalized = normalize_counts(counts_surname)
    dump_data_to_pickle(SURNAMES_PATHS['pkl_cnts'], counts_surname)
    dump_data_to_pickle(SURNAMES_PATHS['pkl_cnts_norm'], counts_surname_normalized)


def build_word_counts():
    """Build word counts."""

    print('***** Build word counts.\n')
    words = load_pickle(WORDS_PATHS['pkl'])
    counts_word = get_counts(words)
    counts_word_normalized = normalize_counts(counts_word)
    dump_data_to_pickle(WORDS_PATHS['pkl_cnts'], counts_word)
    dump_data_to_pickle(WORDS_PATHS['pkl_cnts_norm'], counts_word_normalized)
