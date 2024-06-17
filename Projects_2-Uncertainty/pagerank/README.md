# Read me

The problem and it's full description is avaliable in the link: 
https://cs50.harvard.edu/ai/2024/projects/2/pagerank/

## Introduction:

This project aims at creating a algorithm similar to Google's pagerank. An algorithm meant to identify the more important or higher quality pages and prioritize them when showing a search result.

Meanwhile the method and formula for this is already know, my task was to utilize those to create a program that would ranks all pages in a corpus by implementing two approaches. By utilizing the random surfer model and the iterative algorithm. Both are explained in understanding.

## Utilization:

* cd inside pagerank folder.

* run in the terminal: python pagerank.py corpus (where corpus can be corpus0,1 or 2. Each being a folder containing a number of html pages)

* The terminal will then show the rank of each page based on each method.

## Background:

When search engines like Google display search results, they do so by placing the more 'important' or higher-quality pager higher in the search results. This is done by ranking a page by the number of pages have that a link toward it. But one could make their page seems more important by create multiple pages that points toward it. 

To counter that, this sistem also weight the rank of the pages that are pointing toward another. In other words, a page is more important when it's linked by other important pages. This definition sounds circular, but there are plenty of strategies to calculating theses rankings.

### Random surfer model:

One of these strategy is to consider the behavior of a hypothetical surfer on the internet who clicks on links at random. Consider the corpus of a web page below, where a arrow between pages indicates a link from one page to another, A two ways arrow indicate both pages have a link to one another.

    page 1 < - > page 2 < - > Page 3
      |                         |
      v                         v
    Page 4       Page 5 < - > Page 6

The random surfer model imagines a surfer who starts with a web page at random, then randomly chooses a link to follow. If the surfer was on page 1, he would randomly choose between page 2 and page 4 to visit next (Duplicated links are treated as one, links to the page itself are ignored). If he chooses page 2, he would then randomly choose between pages 2 and 4 next.

But looking at the example above, if the surfer went to page 6, he'd be forced to choose page 5, then page 6. This would make them keep looping between these two and if he were to go to page 4, he wouldn't have anywhere to go. To counter that, we will give surfer the chance of moving to a random page (including the same page he was on).

As such, a page's PageRank can be described as the probability that a random surfer is on that page at any given time. After all, if there are more links to a particular page, then it’s more likely that a random surfer will end up on that page. Moreover, a link from a more important site is more likely to be clicked on than a link from a less important site that fewer pages link to, so this model handles weighting links by their importance as well.

As to the chances of our surfer to go to a random page, rather then choosing one of the link in the current page, this is decided based on a damping factor d. With the probability d (where it's usually ser to 0.85) being the chance that the surfer will pick a link in the current page. meanwhile the probability 1-d is the chance that the surfer will randomly choose a random page in the corpus(including the current page)

Our random surfer now starts by choosing a page at random, and then, for each additional sample we’d like to generate, chooses a link from the current page at random with probability d, and chooses any page at random with probability 1 - d. If we keep track of how many times each page has shown up as a sample, we can treat the proportion of states that were on a given page as its PageRank.

### Iterative Algorithm

Another option is to use a recursive mathematical expression. Let PR(p) be the PageRank of a given page p: the probability that a random surfer ends up on that page. As to how we define Pr(p), we already know there are two ways for a random surfer to end up un a page

    1. with a probability 1-d, the surfer chose a page at random and ended up on page p.

    2 with a probability d, the surfer followed a link from a page i to a page p.

The first condition is fairly straightforward to express mathematically: it’s 1 - d divided by N, where N is the total number of pages across the entire corpus. This is because the 1 - d probability of choosing a page at random is split evenly among all N possible pages.

For the second condition, we need to consider each possible page i that links to page p. For each of those incoming pages, let NumLinks(i) be the number of links on page i. Each page i that links to p has its own PageRank, PR(i), representing the probability that we are on page i at any given time. And since from page i we travel to any of that page’s links with equal probability, we divide PR(i) by the number of links NumLinks(i) to get the probability that we were on page i and chose the link to page p.

This gives us the following definition for the PageRank for a page p.

    PR(p)= (1-d)/N + d * Sum (PR(i)/ Nºlinks(i))

Where d is the damping fator, N the total number of pages in the corpus, i ranges over all pages that have a link to page p, Nºlinks is the number of links present on page i and Sum symbolizes the sum of all of the probability of all i pages.

As to how we'd calculate the PageRank of each page. We can do it by iteration: starting by assuming all pages have a rank of 1/N. then we use theses PR() in the formula above, calculating the value of each page. Repeating this process, based on the previous PageRanks values, util the values converge (they don't change by more then a small, acceptable amount per intereation).


## Understanding:

This project is composed of three corpus directory and the file pagerank.py. Each of the three corpus have a set of html pages linked to one another, ranging from simple ones to more complexes. The pagerank file contains the logic for this project.

In Pagerank.py, Main is a function that expects a command_line argument, which is the name of a directory of a corpus of pages we'd like to compute the PageRank for. the crawl function takes that directory, parses all of the HTML files and returns a dictionary represents the corpus.

The main function then calls the sample_pagerank and the interate_pagerank. The sample_pagerank function takes as arguments the dictionary generated by crawl, the damping factor and the number of samples to use and, following the random surfer model, should return a dictionary where the keys are each page name and the value the PageRank.

The interate_pagerank takes as argument the dictionary generated by crawl, the damping factor and calculates the PageRank using the interative formula method. Returning a dictionary in the same format as sample_pagerank. it's expected that the output of both functions to be similar for a same corpus.

My task was to complete the implementation of transition_model, sample_pagerank and iterate_pagerank.

## Specification:

### Transition_model:
* accepts three arguments: Corpus, page and damping_factor.
* returns a dictionary representing the probability distribution over which page a random surfer would visit next, given a corpus of pages, a current page and a damping factor

* The return value is a python dictionary with the one key for each page in the corpus and it's value should represent the probability of a random surfer would choose that page next. The values should sum to 1.
    * With the probability damping_factor, the random surfer should randomly choose one of the links in the page
    * With probability 1-damping_factor, the surfer should randomly choose one of all pages
* If page has not outgoing links, then we can consider that it has a links to all pages in the corpus, including itself.

### Sample_pagerank:
* Accepts three arguments: corpus, a damping_factor, and n (the number of samples).
* Returns a dictionary with a key for each page in the corpus, with it's value being the page's estimated PageReank. The values in this dictionary should sum to 1.
* the first sample is generated by choosing a page at random.
* for each of the remaining samples, the next sample is generated from the previous sample based on the previous sample's transition model.
* N is assumed to have a value of at least 1.

### Iterate_pagerank:
* Accepts two arguments: corpus and damping_factor.
* Returns a dictionary with a key for each page in the corpus, with it's value being the page's estimated PageReank. The values in this dictionary should sum to 1.
* Begins by assigning each page a rank of 1/N, where N is the number of pages in the corpus.
* Then repeatedly calculate the new rank based on all of the current rank value, according to the PageRank formula in the "background" section.
    * A page with no link is considered to have a link to every other page (including itself).
* this process is repeated util no PageRank value changes by more then 0.001 between the current rank values and the new one.