from nltk.chunk import ne_chunk
from nltk.chunk import tree2conlltags

from funcs.gmb import get_names_from_tokens

from funcs.utilities import download_required_nltk_packages
from funcs.utilities import find_ip_addresses_regex
from funcs.utilities import read_txt
from funcs.utilities import SENTENCES_PATH
from funcs.utilities import tokenize_string

download_required_nltk_packages()

test_sentences = read_txt(SENTENCES_PATH['txt'])
tokens = []
names = []
ip_addresses = []
for idx, sentence in enumerate(test_sentences):
    print('sentence {}: {}'.format(idx, sentence))
    token = tokenize_string(sentence)
    tokens.append(token)
    ip_addresses.append(find_ip_addresses_regex(sentence))
    named_entity_tree = ne_chunk(token)
    iob_tagged = tree2conlltags(named_entity_tree)
    names.append(get_names_from_tokens(iob_tagged, ['B-PERSON']))


print('\n')
print(names)
print(ip_addresses)