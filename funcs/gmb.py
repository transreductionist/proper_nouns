"""Utility functions/constants for utilizing the Groningen Meaning Bank (GMB) corpus."""

import os

GMB_ROOT = 'data/gmb/gmb-2.2.0'


def people_in_census(tagged_tokens, all_census_names, tags):
    """Determine the Census counts given the tagged tokens."""

    census_counts = {
        'truth_names': 0,
        'difference': 0
    }
    tagged_tokens_names = get_names_from_tokens(tagged_tokens, tags)
    if tagged_tokens_names:
        census_counts['truth_names'] = len(tagged_tokens_names)

        difference = set(tagged_tokens_names).difference(all_census_names)
        census_counts['difference'] = len(difference)

    return census_counts


def is_person_tagged(tagged_tokens, test_tagged_tokens, tags):
    """Determine the Named Entity Recognition (NER) counts given the tagged tokens."""

    ner_counts = {'truth_names': 0, 'test_names': 0, 'tagged_minus_test': 0, 'test_minus_tagged': 0}

    tagged_tokens_names = get_names_from_tokens(tagged_tokens, tags)
    test_tagged_tokens_names = get_names_from_tokens(test_tagged_tokens, tags)

    ner_counts['truth_names'] = len(tagged_tokens_names)
    ner_counts['test_names'] = len(test_tagged_tokens_names)
    if len(set(tagged_tokens_names).difference(set(test_tagged_tokens_names))):
        ner_counts['tagged_minus_test'] = len(set(tagged_tokens_names).difference(set(test_tagged_tokens_names)))
    elif len(set(test_tagged_tokens_names).difference(set(tagged_tokens_names))):
        ner_counts['test_minus_tagged'] = len(set(test_tagged_tokens_names).difference(set(tagged_tokens_names)))
    return ner_counts


def get_names_from_tokens(tokens, tags):
    """Pull the names from tokens."""

    tokens_names = []
    for idx, token in enumerate(tokens):
        if token[2] in tags:
            tokens_names.append(token[0])
    return tokens_names


def read_gmb_corpus(file_extension):
    """Read in the Groningen Meaning Bank (GMB) corpus from files using os.walk."""

    file_extension = '.{}'.format(file_extension)
    for root, dirs, files in os.walk(GMB_ROOT):
        for file_name in files:
            if file_name.endswith(file_extension):
                file_pointer = open(os.path.join(root, file_name), 'rb')
                annotated_sentences = get_annotated_sentences(file_pointer)
                annotated_tokens = get_tags_from_sentences(annotated_sentences)
                tokens_in_standard_form = convert_to_standard_form(annotated_tokens)
                conll_tokens = to_conll_iob(tokens_in_standard_form)
                yield [(w, t, iob) for w, t, iob in conll_tokens]
                file_pointer.close()


def to_conll_iob(annotated_sentence):
    """Transform annotated tokens to proper Inside-Outside-Beginning (IOB) tagging format."""

    proper_iob_tokens = []
    for idx, annotated_token in enumerate(annotated_sentence):
        tag, word, ner = annotated_token
        ner = add_iob_prefix(ner, idx, annotated_sentence)
        ner = ner_transform_person_tag(ner)
        proper_iob_tokens.append((tag, word, ner))
    return proper_iob_tokens


def add_iob_prefix(ner, idx, annotated_sentence):
    """Add the Inside-Outside-Beginning (IOB) prefix."""

    if ner != 'O':
        if idx == 0:
            ner = "B-" + ner
        elif annotated_sentence[idx - 1][2] == ner:
            ner = "I-" + ner
        else:
            ner = "B-" + ner
    return ner


def ner_transform_person_tag(ner):
    """Transform the Groningen Meaning Bank (GMB) person tags."""

    if ner == 'B-per-giv':
        return 'B-PERSON'
    elif ner == 'B-per-mid':
        return 'B-PERSON'
    elif ner == 'B-per-nam':
        return 'I-PERSON'
    elif ner == 'B-per-fam':
        return 'I-PERSON'
    elif ner == 'I-per-fam':
        return 'I-PERSON'
    elif ner == 'B-per-ini':
        return 'I-PERSON'
    return ner


def get_annotated_sentences(file_pointer):
    """Get all the annotated sentences from a Groningen Meaning Bank (GMB) file."""

    return file_pointer.read().decode('utf-8').strip().split('\n\n')


def get_tags_from_sentences(annotated_sentences):
    """Get the tokens from the Groningen Meaning Bank (GMB) annotated sentences."""

    for annotated_sentence in annotated_sentences:
        return get_tokens(annotated_sentence)


def convert_to_standard_form(annotated_tokens):
    """Convert the annotated tokens to IOB standard form."""

    tokens_in_standard_form = []
    for idx, annotated_token in enumerate(annotated_tokens):
        annotations = annotated_token.split('\t')
        word, tag, ner = annotations[0], annotations[1], annotations[3]
        format_tag_to_nltk(tag)
        get_primary_tag(ner)
        tokens_in_standard_form.append((word, tag, ner))
    return tokens_in_standard_form


def get_tokens(annotated_sentence):
    """Get the tagged tokens from an annotated sentence."""

    return [seq for seq in annotated_sentence.split('\n') if seq]


def format_tag_to_nltk(tag):
    """Transform some Groningen Meaning Bank (GMB) to NLTK."""

    if tag in ('LQU', 'RQU'):
        return '``'


def get_primary_tag(ner):
    """Get the primary tag and discard others."""

    if ner != 'O':
        return ner.split('-')[0]
    return ner


def print_people(tagged_tokens, test_tagged_tokens):
    """Utility function for printing the truth tokens and the test tokens side-by-side."""

    idx_max = max(len(tagged_tokens), len(test_tagged_tokens)) - 1
    if len(tagged_tokens) >= len(test_tagged_tokens):
        tokens0, tokens1 = tagged_tokens, test_tagged_tokens
        first, second = 'tagged', 'test'
    else:
        tokens0, tokens1 = test_tagged_tokens, tagged_tokens
        first, second = 'test', 'tagged'

    template = '{0:50}|{1:50}'
    print(template.format(first, second))
    for idx, token in enumerate(tokens0):
        if idx <= idx_max:
            print(template.format(token, tokens1[idx]))
        else:
            print(template.format(token, ''))


def print_intermediate_results(n, tagged, census):
    """Print results of Named Entity Recognition and Census methods."""

    print('\n')
    print('****** total sentences tested = {} ******'.format(n))
    print('named entity recognition')
    print('    truth names            : {}\n'.format(tagged['truth_names']))
    print('    test names             : {}'.format(tagged['test_names']))
    print('    test minus tagged      : {}'.format(tagged['test_minus_tagged']))
    print('    tagged minus test      : {}'.format(tagged['tagged_minus_test']))
    print('    test names correct     : {}\n'.format(
        tagged['test_names'] - tagged['test_minus_tagged'] - tagged['tagged_minus_test'])
    )
    print('    no names               : {}\n'.format(tagged['no_names']))
    print('census data')
    print('    truth_names            : {}'.format(census['truth_names']))
    print('    difference             : {}'.format(census['difference']))
    print('    no names               : {}'.format(census['no_names']))
