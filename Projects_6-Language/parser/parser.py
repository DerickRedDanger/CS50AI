import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> S S | S Conj S | NP VP NP | NP VP | NP VP PP NP | VP NP PP NP | VP NP | NP VP PP | NP VP NP PP | PP PP

AP -> Adj | Adj AP
NP -> N | Det N | Det AP N | Det N Adv | Det N | Det AP N | Det AP N
PP -> P NP | P
VP -> V | Adv V | V Adv
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    lower_case_sentence = sentence.lower()
    processsed_sentence = nltk.word_tokenize(lower_case_sentence)

    # creating a list with words that contain at least one alphabetic character
    cleaned_sentence = [word for word in processsed_sentence if any(letter.isalpha() for letter in word)]

    return cleaned_sentence

    raise NotImplementedError


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    # Getting all subtrees with the label == 'NP'
    chunks = list(tree.subtrees(lambda t: t.label() == "NP"))

    np_chunks = []
    for chunk1 in chunks:
        append = True

        # Not appending chunks that have other chunks in them.
        for chunk2 in chunks:
            if chunk1 != chunk2 and chunk2 in chunk1.subtrees():
                append = False
                break

        if append:
            np_chunks.append(chunk1)

    return np_chunks

    raise NotImplementedError


if __name__ == "__main__":
    main()
