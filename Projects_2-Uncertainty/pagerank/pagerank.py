import os
import random
import re
import sys
from termcolor import colored
import copy

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
    all_pages = dict()
    link = set()

    for current, links in corpus.items():
        all_pages[current] = 0
        if page == current:
            link = links
    
    links_chance = damping_factor/(len(link))
    all_pages_chance = (1-damping_factor)/len(all_pages)

    for pages in all_pages.keys():
        all_pages[pages] += all_pages_chance
        if pages in link:
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
            # choices returns a list, so we picking only the element of that list
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
    initial_Rank = 1/len(corpus)

    all_pages_chance = (1-damping_factor)/len(all_pages)

    for page in corpus.keys():
        all_pages_rank_past_interaction[page] = initial_Rank

    acceptable_error = False
    all_pages_rank_new_interaction = copy.deepcopy(all_pages_rank_past_interaction) 

    # Sanity check:
    Sanity_check = 0
    #
    while acceptable_error != True:
        acceptable_error = True
        Sanity_check = 0

        for page in all_pages_rank_new_interaction.keys():
            all_pages_rank_new_interaction[page] = all_pages_chance
            total_sum = 0
            for pages,values in corpus.items():
                print(f"all_pages_chance = {all_pages_chance}")
                print(f"Damping_factor = {damping_factor}")
                print(f"all_pages_rank_past_interaction[{pages}] = {all_pages_rank_past_interaction[pages]}")
                print(f"len(values) = {len(values)}")
                n_links = len(values)
                if n_links == 0:
                    n_links = len(corpus)
                total_sum = all_pages_rank_past_interaction[pages]/n_links
            print(f"total = {total_sum}")
            print(f"old all_pages_rank_new_interaction[{page}] = {all_pages_rank_new_interaction[page]}")
            all_pages_rank_new_interaction[page] += damping_factor * total_sum
            print(f"new all_pages_rank_new_interaction[{page}] = {all_pages_rank_new_interaction[page]}")
            print(colored(f"The {page}'s rank is = {all_pages_rank_new_interaction[page]}", 'yellow'))
            Sanity_check += all_pages_rank_new_interaction[page]

        # Sanity check
        print(f"Sanity check -> Sum of all ranks = {Sanity_check}")
        #

        for page in all_pages_rank_new_interaction.keys():
            difference = all_pages_rank_new_interaction[page] - all_pages_rank_past_interaction[page]
            print(f"Difference bettwen {page} is {difference}")
            if not 0.001 > difference > -0.001:
                acceptable_error = False

        all_pages_rank_past_interaction = copy.deepcopy(all_pages_rank_new_interaction) 

        if Sanity_check != 1:
            print(f"sanity = {Sanity_check}")
            break

    return all_pages_rank_new_interaction
    
    raise NotImplementedError


if __name__ == "__main__":
    main()
