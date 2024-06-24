
# Parse Project

## Problem Description
The full problem description is available at the following link:  [CS50 AI Project 6 - Parser](https://cs50.harvard.edu/ai/2024/projects/6/parser/)

## Introduction

This project aims to create a parsing program capable of extracting noun phrases from sentences.

This is achieved by utilizing the Natural Language Toolkit's (NLTK) context-free grammar while manually writing the rules for the non-terminals. While this serves as practice and experience, it has limited use in general applications.

## Utilization

1. Navigate to the `parser` directory:
   ```bash
   cd parser
   ```
2. Install the required packages (only needs to be done once):
   ```bash
   pip3 install -r requirements.txt
   ```
3. Run the following command in the terminal to parse a specific sentence:
   ```bash
   python parse.py sentences/[Sentence.txt]  # For example, sentences/10.txt
   ```
4. Alternatively, run the program and input sentences manually:
   ```bash
   python parse.py
   ```
   The terminal will then prompt for a sentence. After entering a sentence, the program will attempt to parse it. (Note: These rules were manually created with specific sentences in mind and may not work if the words used aren't covered by the grammar rules.)

5. If the sentence is grammatically correct, the program will return a tree showing the sentence's structure and its noun phrases. For example, this program parses sentences like "His Thursday chuckled in a paint."
6. If the sentence isn't grammatically correct, the program will return "could not parse sentence." For example, the sentence "Armchair on the sat Holmes" would not be parsed.

## Background

Parsing, the process of determining the structure of a sentence, is a common task in natural language processing. Parsing is useful for understanding sentence meaning and extracting information from sentences. Specifically, extracting noun phrases from a sentence helps understand what the sentence is about.

In this project, we use the context-free grammar formalism to parse English sentences to determine their structure. In context-free grammar, rewriting rules transform symbols into other symbols. The objective is to start with a non-terminal symbol S (representing a sentence) and apply context-free grammar rules until a complete sentence of terminal symbols (words) is generated. For example, the rule S -> N V means that the S symbol can be rewritten as N V (a noun followed by a verb). With the rules N -> "Holmes" and V -> "sat", we can generate the sentence "Holmes sat."

## Understanding

The `sentences` directory contains a number of text files, each with an English sentence. The goal of this project was to write a parser that can parse all these sentences.

In `parse.py`, the context-free grammar rules are defined at the top of the file. These rules generate terminal and non-terminal symbols.

The main function accepts a sentence input, either from a file or via user input. The sentence is preprocessed and parsed according to the context-free grammar defined in the file. The resulting trees are printed out, and all the “noun phrase chunks” are printed as well using the `np_chunk` function.

My task was to write the rules for parsing these sentences, and implement the `preprocess` and `np_chunk` functions.

## Specification

### `preprocess`

- Accepts a sentence as input and returns a lowercased list of its words.
- Any word that doesn’t contain at least one alphabetic character (e.g., "." or "28") is excluded from the returned list.

### `np_chunk`

- Accepts a tree representing the syntax of a sentence and returns a list of all the noun phrase chunks in that sentence.
- A “noun phrase chunk” is defined as a noun phrase that doesn’t contain other noun phrases within it. More formally, a noun phrase chunk is a subtree of the original tree labeled NP that does not contain other noun phrases as subtrees. For example, if "the home" is a noun phrase chunk, then "the armchair in the home" is not a noun phrase chunk, as the latter contains the former as a subtree.
- Returns a list of `nltk.Tree` objects, where each element has the label NP.
```

Feel free to make any additional changes or let me know if there's anything else you'd like to include!