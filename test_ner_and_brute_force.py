"""The main script for reading the GRB corpus and determining statistics for NER and Census methods.

   NER: Named Recognition Entity
   Census: Uses first and surnames collected from the 2010 US census
   GMB: Groningen Meaning Bank corpus
"""

from nltk.chunk import ne_chunk
from nltk.chunk import tree2conlltags

from proper_nouns.funcs.gmb import is_person_tagged
from proper_nouns.funcs.gmb import people_in_census
from proper_nouns.funcs.gmb import read_gmb_corpus

from proper_nouns.funcs.gmb import print_intermediate_results

from proper_nouns.funcs.utilities import download_required_nltk_packages
from proper_nouns.funcs.utilities import get_all_census_names
from proper_nouns.funcs.utilities import parse_ner_counts
from proper_nouns.funcs.utilities import parse_census_counts
from proper_nouns.funcs.utilities import tokenize_string

download_required_nltk_packages()

all_census_names = get_all_census_names()

tags = ['B-PERSON', 'I-PERSON']
census = {'truth_names': 0, 'difference': 0, 'no_names': 0}
tagged = {'truth_names': 0, 'test_names': 0, 'test_minus_tagged': 0, 'tagged_minus_test': 0, 'no_names': 0}

n = 0
corpus = read_gmb_corpus('tags')

for tagged_tokens in corpus:
    sentence = ' '.join([iob[0] for iob in tagged_tokens])

    test_the_tokens = tokenize_string(sentence)
    ne_tree = ne_chunk(test_the_tokens)
    test_tagged_tokens = tree2conlltags(ne_tree)
    ner_counts = is_person_tagged(tagged_tokens, test_tagged_tokens, tags)
    parse_ner_counts(ner_counts, tagged)

    census_counts = people_in_census(tagged_tokens, all_census_names, tags)
    parse_census_counts(census_counts, census)

    n += 1
    if n % 2000 == 0:
        print_intermediate_results(n, tagged, census)
