"""Explore frequencies of characters with respect to position in words as opposed to names."""

from functools import reduce
from statistics import mean

from proper_noun_original.funcs.utilities import FIRST_NAMES_PATHS
from proper_noun_original.funcs.utilities import WORDS_PATHS
from proper_noun_original.funcs.utilities import load_pickle
from proper_noun_original.funcs.utilities import multiply
from proper_noun_original.funcs.utilities import print_frequencies

words_probs = load_pickle(WORDS_PATHS['pkl_cnts_norm'])
words_probs = words_probs['data']
word_probs = []
word_means = []

first_names_probs = load_pickle(FIRST_NAMES_PATHS['pkl_cnts_norm'])
first_names_probs = first_names_probs['data']
name_probs = []
name_means = []

words = load_pickle(WORDS_PATHS['pkl'])['data']
names = load_pickle(FIRST_NAMES_PATHS['pkl'])['data']

for idx, name in enumerate(names):
    test_name = list(name)
    name_prob = []
    for i in range(0, len(test_name)):
        name_prob.append(first_names_probs[i][test_name[i]])
    name_means.append(mean(name_prob))
    name_prob = reduce(multiply, name_prob)
    name_probs.append(name_prob)

    test_name = list(name.lower())
    word_prob = []
    for i in range(0, len(test_name)):
        word_prob.append(words_probs[i][test_name[i]])
    word_means.append(mean(word_prob))
    word_prob = reduce(multiply, word_prob)
    word_probs.append(word_prob)

print_frequencies('Name as Word', names, [name_probs, name_means], [word_probs, word_means])

for idx, word in enumerate(words):
    test_word = list(word)
    word_prob = []
    for i in range(0, len(test_word)):
        word_prob.append(words_probs[i][test_word[i]])
    word_means.append(mean(word_prob))
    word_prob = reduce(multiply, word_prob)
    word_probs.append(word_prob)

    test_word = list(word.title())
    if len(test_word) <= 15:
        name_prob = []
        for i in range(0, len(test_word)):
            name_prob.append(first_names_probs[i][test_word[i]])
        name_means.append(mean(name_prob))
        name_prob = reduce(multiply, name_prob)
        name_probs.append(name_prob)

print_frequencies('Word as Name', names, [name_probs, name_means], [word_probs, word_means])
