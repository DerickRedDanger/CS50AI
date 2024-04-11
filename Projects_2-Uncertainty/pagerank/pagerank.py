import os
import random
import re
import sys
import copy

# For debugging purposes
from termcolor import colored
#

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    # Starting a dict for all pages in corpus and their probability
    all_pages = dict()

    # getting the set of all page the current page has a link to
    link = set()

    # initializing all_page and getting link
    for current, links in corpus.items():
        all_pages[current] = 0
        if page == current:
            link = links

    # Number of pages the current page has a link to
    n_links = len(link)

    # number of total pages in corpus
    n_all_pages = len(all_pages)

    # if this page isn't linked to another, consider it's linked to all (even itself)
    if n_links == 0:
        n_links = n_all_pages

    
    # probability of choosing a linked page
    links_chance = damping_factor/(n_links)

    # probability of choosing a page at random
    all_pages_chance = (1-damping_factor)/n_all_pages

    for pages in all_pages.keys():
        all_pages[pages] += all_pages_chance

        # if this page have links
        if n_links != n_all_pages:

            # pages is one of these links
            if pages in link:
                all_pages[pages] += links_chance

        # if this page didn't have links, it's linked to all pages
        else:
            all_pages[pages] += links_chance

    #print(f" All pages chance = {all_pages}")
    return all_pages

    raise NotImplementedError

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Dictionary holding all pages and their rank
    all_pages_rank = dict()

    for page in corpus.keys():
        all_pages_rank[page] = 0

    # List holding all pages to be used in random function
    # They don't work directly on dicts, so it's better to create a list to hold the values
    all_pages = list(all_pages_rank.keys())
        
    samples = 0
    increase = 1/n
    page=''

    while samples < n:
        if samples == 0:
            page = random.choice(all_pages)
            all_pages_rank[page] += increase

        else:
            links_chances= transition_model(corpus,page,damping_factor)
            links = list(links_chances.keys())
            chances = list(links_chances.values())
            # choices returns a list(with 1 element in this case),
            # so we picking only the element of that list
            page = random.choices(links, chances)[0]
            all_pages_rank[page] += increase


        samples += 1

    return all_pages_rank

    raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # List holding all pages to be used in random function
    # They don't work directly on dicts, so it's better to create a list to hold the values
    all_pages = list(corpus.keys())

    # Dictionary holding all pages and their rank 
    # for the initial(and later former) interaction
    all_pages_rank_past_interaction = dict()

    # probability of choosing a page at random
    all_pages_chance = (1-damping_factor)/len(all_pages)

    # initializing the page rank of all pages
    initial_Rank = 1/len(corpus)
    for page in corpus.keys():
        all_pages_rank_past_interaction[page] = initial_Rank

    # variable to check if the difference is within the acceptable error
    acceptable_error = False

    # Making a deepy copy of the initial dictionary
    all_pages_rank_new_interaction = copy.deepcopy(all_pages_rank_past_interaction) 

    # Sanity check:
    # checking if the sum of all ranks are equal to 1 
    # (not nescessary anymore, leaving for safety sake)
    Sanity_check = 0
    #

    while acceptable_error != True:
        acceptable_error = True
        Sanity_check = 0

        # looping throught each page
        for current in all_pages_rank_new_interaction.keys():

            # Initializing their rank
            all_pages_rank_new_interaction[current] = all_pages_chance
            
            # Variable to hold the sum of the rank based on the other pages
            total_sum = 0
            for pages,values in corpus.items():

                # If this page doesn't have a link to another page
                # It's considered that it has a link to all pages(including itself)
                if len(values) == 0:
                    n_links = len(corpus)
                    total_sum += all_pages_rank_past_interaction[pages]/n_links
                
                # If this page has links, check current page is one of them
                elif current in values:
                    n_links = len(values)
                    # If it's, add this part of the rank to total_sum
                    total_sum += all_pages_rank_past_interaction[pages]/n_links

            # Multiply the total by the damping factor and add it to current's page rank
            all_pages_rank_new_interaction[current] += damping_factor * total_sum
            # Sum the current page's rank to the sanity check
            Sanity_check += all_pages_rank_new_interaction[current]

        # Check if any of the difference is highest then the acceptable
        for page in all_pages_rank_new_interaction.keys():
            difference = all_pages_rank_new_interaction[page] - all_pages_rank_past_interaction[page]

            # If it's, repeat the while again.
            if not 0.001 > difference > -0.001:
                acceptable_error = False

        # set the past interaction to the current interaction and repeat the cicle
        # utill the error is withing acceptable parameters
        all_pages_rank_past_interaction = copy.deepcopy(all_pages_rank_new_interaction) 

        # If sanity check is not equal to one, break and report error.
        if not 1.002>Sanity_check > 0.998:
            print(f"sanity = {Sanity_check}")
            break

    return all_pages_rank_new_interaction
    
    raise NotImplementedError


if __name__ == "__main__":
    main()
