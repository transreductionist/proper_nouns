# Find name & IP address in string

## Bob found that 127.0.0.1 was bad and 123.4.5.6 was safe.

- Build a web scraper to accumulate data to test against.
    - It can also serve as a way of testing the improvement of the algorithm.
    - Run the algorithm against scraped data and see how well it does.

- Under resources collect a list of common first and last names.
    - Used like password cracking Common Password lists.

- Parts of speech analysis: look for pronouns.
    - Personal pronuns will be followed by words such as laughing, crying, beautiful, etc.

- Are `name` and `ip_address independent`

## Regex

- `r'\b(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\b'`

- `[]` specifies a class of characters and so `[0-9]` specifies pattern matching on the
numbers 0 through 9.

- `\b` Returns a match where the specified characters are at the beginning or at the end of
a word

## Tagset

- `get_tagset('upenn_tagset', 'NN.*')`

## Stats

- total sentences tested: 10,000
- NER
- number of truth-names found: 4,740
- number of test-names found: 7,977
    - correct: 3,693
    - incorrect: 4,284
- number of sentences with no names: 7,326
- percentage correct: 78%
- false positives: 54%

test minus truth = 1
truth: `[Abdullahi, Yusuf, Ahmad]`
test: `[Somalia, Abdullahi, Yusuf, Ahmad]`

truth minus test = 1
truth: `[Muhammad]`
test: `[Islam]`

- 2010 CENSUS
- number of truth-names found: 4,740
- number of test-names found: 3,676
- number of test-names missed: 1,064
- number of sentences with no names: 7,326
- percentage correct: 78%
- percentage incorrect: 22%

Example difference: `['Ahmed', 'Qureia']`
`Qureia` not found in 2010 CENSUS data

## Difference in no names found because of unequal

## Appendix

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


