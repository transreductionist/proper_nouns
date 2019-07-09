<div align="center"><img src="https://user-images.githubusercontent.com/8593071/60805400-f8309d00-a14d-11e9-86a8-f9780e3110e5.jpg" width="200" height="125" align="middle"/></div>



# Find Name & IP Address in String

- `pip install nltk`
- `pip install wordnet`

**Preface**: As natural language processing problems are solved, a programmer comes to understand our limitations. For a human, finding a name in a sentence is easy, on the other hand, for a machine the matter is qute different. Then there are the other complications, e.g. misspellings, disambiguation, etc. The methods  used below treat language as data, using pattern matching and statistical analysis (tagged corpi) to extract information from that data.

As an example, `nltk.chunk` provides classes and interfaces for identifying non-overlapping linguistic groups (such as base noun phrases) in unrestricted text. A chunk structure is a tree containing tokens and chunks, where each chunk is a subtree containing only tokens. The chunking uses regular-expression pattern matching at its base for build the tree.

What would be exciting is to find other techniques, such as those that use nueral networks, to process language. These would "understand" language and be able to make long range associations. One can think of the analogy of a grammer as opposed to a universal grammar.

## Satement of the Problem

A rather simple statement:

- given a string of text detect IP Addresses and Persons/Names in the string. For example, with the input:
    - "Bob found that 127.0.0.1 was bad and 123.4.5.6 was safe."
        - The solution is: `[ 127.0.0.1, 123.4.5.6 ]` for the IP Addresses.
        - For the person's name it should find `[ Bob ]`.

And as is often the case with simple questions, a less than simple solution. Use any python packages you find useful, and any data structures/print statements, etc. to demonstrate the results.

Provide a general discussion for any kind of weaknesses with the approach that you use as well as
general thoughts about the problem. I'd like to see discussion about how you would approach testing this
problem, or about any other possible solution paths you would be looking to test.

## General Comments on Code

- Document strings were included, however they need to be expanded.
- The organization of the helper functions can be improved.
- Some of the functions need to be more narrowly crafted.
- The use of generators should be employed where possible. Perhaps using classes for the Gronigen Meaning Bank (GMB)
would create a more readable and functional structure.


## Comment on Data Sets

The project used several data sets that are listed in Appendix A & B. These sets were large and so have
not been included in the repository, and they can be downloaded from the links provided. Other data sets were
generated from Python scripts, and again have not been saved in the repository.

The given test sentence, along with some other examples have been included in a text file in the
Data directory. The second and third sentences are:

- Caroline found out that the IP address 192.168.1.89/32 was a honey pot.
- Alice found out that the IP address 192.168.1.89/32 was a honey pot.

It is an interesting example, because the name Caroline is retrieved by the Named Entity Recognition solution,
while the name Alice is not. This points to an underlying complexity to the problem.

## Bob found that 127.0.0.1 was bad and 123.4.5.6 was safe.

### Named Entity Recognition & Brute Force

- Near-human performance can be achieved with the best NER systems. Consider that one of the best systems
scored 93.39% of F-measure, and human annotators, like the ones who created the Gronigen Meaning Bank (GMB)
corpus, scored 97.60% and 96.95%. Out-of-the box the results here are not that high, however with more
study on why tagging missed certain names, it can definitely be improved.

- Links to data used in this project can be found in Appendix A & B.

- [NLTK Organization Book Chapter 7](http://www.nltk.org/book_1ed/ch07.html) covers extracting information from text.

- [Chunking HOWTO](http://www.nltk.org/howto)

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
    - If not, they may be used to obtain information about the name.

#### Other Named Entity Recognition Platforms

- GATE supports NER across many languages and domains out of the box, usable via a graphical interface and a Java API.
- OpenNLP includes rule-based and statistical named-entity recognition.
- SpaCy features fast statistical NER as well as an open-source named-entity visualizer.

### Use Regex for IP Addresses

Numerical IP Addresses can be captured with a regex, such as:

- `r'\b(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\b'`

If the IP address can be something like `https://github.com/transreductionist/proper_nouns` our problem becomes more
difficult.

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

## Weaknesses & Comments

The analysis here was done in English. Opening up the problem domain to other languages adds more complexity.

### Named Entity Recognition

- Susceptible to errors, such as tagging Christion Dior as a name.
- Out-of-the box it appears that `ne_chunk` performs like the simple brute force method, but with many false positives (FP).
- Can be trained to have less FP and higher percentage correct.
- Use surrounding tagged tokens to discriminate better:
    - People laugh, cry, shout, etc.
    - Neighborhood associations.
- Adaptable and extendable.

### Brute Force

- Can be added to, and names are fairly static entities. Once you have them you have them.
- There are extensive databases across the internet that can be used to build a more comprehensive list.
- Search algorithms can be created to improve performance.
- It is not adaptable.
- May be used alongside a NER analysis.


## Appendix A: Gronigen Meaning Bank

A free semantically annotated corpus, which is used in this project to test the accuracy of
the Named Entity Recognition for people's names.

The [Gronigen Meaning Bank (GMB)](http://gmb.let.rug.nl/), developed at the University of
Groningen, comprises thousands of texts in raw and tokenised format, tags for part of
speech, named entities and lexical categories, and discourse representation structures
compatible with first-order logic.


## Additional Work

- Look into using the `nltk.chunk.api` module and its `evaluate(gold)` function. There is also
`nltk.chunk.util.ChunkScore`.
- Investigate the large number of false positives as compared to the percentage correct for the Named
Entity Recognition analysis.

## Appendix B: U.S. Census Data

The brute force method uses names from 2 sources: (1) surnames from the U.S. Census, and (2)
first names from the Social Security Administration.

- [Frequently Occurring Surnames from the Census 2010](https://www.census.gov/topics/population/genealogy/data.html)
- [Social Security Administration First Names Database](https://data.world/len/us-first-names-database)


## Some Interesting StackOverflow Answers

Posted under the user name Aaron:

- [Golang Enumerations](https://stackoverflow.com/questions/14426366/what-is-an-idiomatic-way-of-representing-enums-in-go/56807462#56807462)
- [Parametric Cubic Equation and Bisection Routine](https://stackoverflow.com/questions/31102754/find-intersection-of-ax-and-by-in-complex-plane-plus-corr-x-and-y/31225836#31225836) (Matplotlib)
- [Deploying Django to AWS WSGIPATH Refers to a File That does not Exist](https://stackoverflow.com/questions/29395875/deploying-django-to-aws-wsgipath-refers-to-a-file-that-does-not-exist/29981741#29981741)

## Appendix C: Some Tags

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


