# PageRank Project

## Problem Description

The full problem description is available at the following link: [CS50 AI Project 2: PageRank](https://cs50.harvard.edu/ai/2024/projects/2/pagerank/).

## Introduction

This project aims to create an algorithm similar to Google's PageRank, which identifies important or high-quality pages to prioritize in search results. The task involves implementing the algorithm using two approaches: the random surfer model and the iterative algorithm.

## Utilization

1. **Navigate to the Pagerank folder**:
   ```bash
   cd pagerank
   ```
2. **Run the script**:
   ```bash
   python pagerank.py corpus
   ```
   where `corpus` can be `corpus0`, `corpus1`, or `corpus2`, each being a folder containing a number of HTML pages.

The terminal will then show the rank of each page based on both methods.

## Background

Search engines like Google rank pages based on their importance, calculated by the number and quality of incoming links. A page linked by other important pages is ranked higher. The PageRank algorithm quantifies this importance using two models:

### Random Surfer Model

This model simulates a surfer who randomly clicks on links. The probability that the surfer ends up on a page defines its PageRank. If the surfer encounters a page with no links or gets stuck in a loop, they will randomly jump to another page with a damping factor \(d\) (usually 0.85). The process is as follows:

1. Start at a random page.
2. With probability \(d\), follow a random link on the current page.
3. With probability \(1-d\), jump to any page in the corpus.

### Iterative Algorithm

This approach uses a recursive formula to calculate the PageRank:


    PR(p) = (1-d)/N + d * Sum (PR(i)/ Nºlinks(i))


where:
- \(d\) is the damping factor.
- \(N\) is the total number of pages in the corpus.
- \(i\) ranges over all pages that have a link to page \(p\)
- \(PR(i)\) is the PageRank of page \(i\).
- \(Nºlinks(i)\) is the number of links on page \(i\).

The algorithm iteratively updates the PageRank of each page until the values converge.

## Understanding

This project includes three corpus directories and the `pagerank.py` file. Each corpus contains a set of HTML pages linked to one another, from simple to complex structures. The `pagerank.py` file contains the main logic.

### Key Functions in `pagerank.py`

- **`main`**: Expects a command-line argument (directory of the corpus) and processes it using `crawl`.
- **`crawl`**: Parses HTML files in the directory and returns a dictionary representing the corpus.
- **`sample_pagerank`**: Implements the random surfer model to compute PageRank.
- **`iterate_pagerank`**: Uses the iterative formula to compute PageRank.

### Tasks Completed

- Implemented `transition_model`, `sample_pagerank`, and `iterate_pagerank`.

## Specifications

### `transition_model`

- **Arguments**: `corpus`, `page`, `damping_factor`
- **Returns**: Probability distribution dictionary over which page a random surfer visits next.
- **Logic**:
  - With probability `damping_factor`, randomly choose a link on the current page.
  - With probability `1 - damping_factor`, randomly choose any page.
  - If no outgoing links, consider the page linked to all pages.

### `sample_pagerank`

- **Arguments**: `corpus`, `damping_factor`, `n` (number of samples)
- **Returns**: Dictionary of PageRank values.
- **Logic**:
  - First sample: random page.
  - Subsequent samples: based on previous sample's transition model.

### `iterate_pagerank`

- **Arguments**: `corpus`, `damping_factor`
- **Returns**: Dictionary of PageRank values.
- **Logic**:
  - Initialize each page rank to `1/N`.
  - Update ranks iteratively using the PageRank formula until values converge.
```

Feel free to make any additional changes or let me know if there's anything else you'd like to include!