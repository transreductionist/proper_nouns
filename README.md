[](https://github.com/transreductionist/proper_nouns/issues/4)

# Find Name & IP Address in String

## Bob found that 127.0.0.1 was bad and 123.4.5.6 was safe.

### Use Named Recognition Entity Tools for Names

- Links to data used in this project can be found in Appendix A & B.

- Try using frequencies of characters with respect to position in a word or name as a discriminator.
    - Names derived from Social Security Administration database and word from wordnet.
    - Characters in names do not seem to have significantly different frequencies from those in words.

- Try brute force.
    - Collect names from data sources.
    - Use set (hashed) operations to find names in non-tagged tokens.
    - Compare results to known IOB tagged corpus Gronigen Meaning Bank (GMB)

- Try Named Entity Recognition:
    - Tokenize sentence.
    - Using `nltk.ne_chunk` build a Named Entity tree.
    - Use the tree to build Inside-Outside-Beginning (IOB) tagged tokens.
    - Compare results to known IOB tagged corpus Gronigen Meaning Bank (GMB)

- Question: Are `name` and `ip_address independent` from one another?
    - If not they may be used to obtain information about the name.

### Use Regex for IP Addresses

- `r'\b(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\b'`

## Results

- **Total sentences tested**: 10,000

- **Named Entity Recognition Analysis**:
    - number of truth-names found: 4,740
    - number of test-names found: 7,977
        - correct: 3,693
        - incorrect: 4,284
    - number of sentences with no names: 7,326
    - percentage correct: 78%
    - false positives: 54%
- **Named Entity Recognition Misses**:
    - `set(test) - set(truth) = 1`
        - truth: [ Abdullahi, Yusuf, Ahmad ]
        - test: [ Somalia, Abdullahi, Yusuf, Ahmad ]
    - `set(truth) - set(test) = 1`
        - truth: [ Muhammad ]
        - test: [ Islam ]
- **2010 Census Analysis**:
    - number of truth-names found: 4,740
    - number of test-names found: 3,676
    - number of test-names missed: 1,064
    - number of sentences with no names: 7,326
    - percentage correct: 78%
    - percentage incorrect: 22%
- **2010 Census/SSA Misses**:
    - Example difference: [ Ahmed, Qureia ]
    - Qureia not found in Social Security Administration first name list.

## Weaknesses

### Named Entity Recognition
- Is only as accurate as simple brute force, but with many false positives.
- Can be trained to have less FP and higher percentage correct.
- Use surrounding tagged tokens to discriminate better:
    - People laugh, cry, shout, etc.

### Brute Force
- Can be added to.
- May be used in conjunction with NER analysis.


## Appendix A: Gronigen Meaning Bank

A free semantically annotated corpus, which is used in this project to test the accuracy of
the Named Entity Recognition for people's names.

The [Gronigen Meaning Bank (GMB)](http://gmb.let.rug.nl/), developed at the University of
Groningen, comprises thousands of texts in raw and tokenised format, tags for part of
speech, named entities and lexical categories, and discourse representation structures
compatible with first-order logic.


## Appendix B: U.S. Census Data

The brute force method uses names from 2 sources: (1) surnames from the U.S. Census, and (2)
first names from the Social Security Administration.

- [Frequently Occurring Surnames from the Census 2010](https://www.census.gov/topics/population/genealogy/data.html)
- [Social Security Administration First Names Database](https://data.world/len/us-first-names-database)


## Appendix C

- CC: conjunction, coordinating
- CD: numeral, cardinal
- DT: determiner
- EX: existential there
- IN: preposition or conjunction, subordinating
- JJ: adjective or numeral, ordinal
- JJR: adjective, comparative
- MD: modal auxiliary
- NN: noun, common, singular or mass.
- NNP: noun, proper, singular
- NNS: noun, common, plural
- PDT: pre-determiner
- POS: genitive marker
- PRP: pronoun, personal
- PRP$: pronoun, possessive
- RB: adverb
- RBR: adverb, comparative
- RBS: adverb, superlative
- RP: particle
- UH: interjection
- VB: verb, base form
- VBD: verb, past tense
- VBG: verb, present participle or gerund
- VBN: verb, past participle
- VBP: verb, present tense, not 3rd person singular
- VBZ: verb, present tense, 3rd person singular
- WDT: WH-determiner
- WP: WH-pronoun
- WRB: Wh-adverb


