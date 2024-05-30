The problem and it's full description is avaliable in the link: 
https://cs50.harvard.edu/ai/2024/projects/6/parser/

## Introduction:

This project aims at creating a parsing program, that is capable of extracting noun phrase.

This is done by utilizing Natural language tool kit's (NLTK) context-free grammar while manually writing the rules for the Non Terminals. As such, meanwhile this serves for practice and experience, as it's, it doesn't hold much use in general.

## Utilization:

* cd inside parser

* pip3 install -r requirements.txt (only need to be done once)

* Run in the terminal: python parse.py sentences/[Sentence.text] (for example sentences/10.txt)

* Optionally, you can just run the program and give yourself the sentences for it to parse by running: python parse.py

* The terminal will then ask for a sentence, after being given one it will try to parse it. (Remember, these rules were made manually with a focus on the sentences, it may not work if the words you use aren't in the terminal rules)

* If the sentence is grammatically correct, this program will return a tree showing that sentence's structure, and its noun phrases. (For example, this program parses sentences like 'His Thursday chuckled in a paint.')

* If the sentence isn't grammatically correct, the program will return "could not parse sentence". (one example is the sentence "Armchair on the sat Holmes".)

## Background:

A common task in natural language processing is parsing, the process of determining the structure of a sentence. This is useful for a number of reasons: knowing the structure of a sentence can help a computer to better understand the meaning of the sentence, and it can also help the computer extract information out of a sentence. In particular, it’s often useful to extract noun phrases out of a sentence to get an understanding of what the sentence is about.

In this problem, we’ll use the context-free grammar formalism to parse English sentences to determine their structure. In a context-free grammar, we repeatedly apply rewriting rules to transform symbols into other symbols. The objective is to start with a nonterminal symbol S (representing a sentence) and repeatedly apply context-free grammar rules until we generate a complete sentence of terminal symbols (i.e., words). The rule S -> N V, for example, means that the S symbol can be rewritten as N V (a noun followed by a verb). If we also have the rule N -> "Holmes" and the rule V -> "sat", we can generate the complete sentence "Holmes sat.".


## understanding:

There are a number of text files in the sentence directory, each containing an English sentence. This project goal was to write a parser that is able to parse all of these sentences.

At parse.py, we defined the context free grammar rules at the top of the file. There are the rules used to generate terminal symbols and non-terminal symbol.

The main function accepts a sentence input, either from a file or via user input. The sentence is preprocessed and then parsed according to the context-free grammar defined by the file. The resulting trees are printed out, and all the “noun phrase chunks” are printed as well (via the np_chunk function).

My duty was to write the rules for parsing these sentences, the preprocess and np_chunk functions.

## Specification:

### Preprocess:

* Accepts a sentence as input and returns a lowercased list of its words.

* Any word that doesn’t contain at least one alphabetic character (e.g. . or 28) is excluded from the returned list.

### Np_chunk:

* Accepts a tree representing the syntax of a sentence, and return a list of all the noun phrase chunks in that sentence.

* For this project, a “noun phrase chunk” is defined as a noun phrase that doesn’t contain other noun phrases within it. Put more formally, a noun phrase chunk is a subtree of the original tree whose label is NP and that does not itself contain other noun phrases as subtrees. (For example, if "the home" is a noun phrase chunk, then "the armchair in the home" is not a noun phrase chunk, because the latter contains the former as a subtree.)

* Returns a list of nltk.tree objects, where each element has the label NP.
