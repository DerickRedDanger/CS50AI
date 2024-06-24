# Heredity AI Project

The full problem description is available at this [CS50 AI Project 2: Heredity](https://cs50.harvard.edu/ai/2024/projects/2/heredity/).

## Introduction

This project aims to write an AI that assesses the likelihood that a person will have a particular genetic trait. This is done by evaluating their parents' genes (or, if that information is unavailable, through the unconditional probability of a person having these genes) and utilizing joint probability and Bayesian networks to determine the probability of various genetic configurations. Ultimately, the process involves summing and normalizing these probabilities to find the likelihood of each individual gene/trait.

## Utilization

1. **Navigate to the heredity folder**:
    ```bash
    cd heredity
    ```
2. **Run the program**:
    ```bash
    python heredity.py data/family.csv
    ```
    (where `family` can be `family0`, `family1`, or `family2`. Each CSV contains the data of a small family).

The terminal will then display the probabilities for each family member having 0, 1, or 2 genes and the likelihood of them exhibiting the trait.

## Background

Mutated versions of the GJB2 gene are one of the leading causes of hearing impairment in newborns. Each person carries two copies of the gene, which means they can possess either 0, 1, or 2 copies of the hearing impairment version of GJB2. Without genetic testing, it’s difficult to determine the exact number of mutated GJB2 copies a person has. This information is a “hidden state” that affects observable traits (hearing impairment), but is not directly known. Some individuals may have 1 or 2 copies of the mutated gene without exhibiting hearing impairment, while others with no copies may still exhibit it.

Every child inherits one copy of the GJB2 gene from each parent. If a parent has two copies of the mutated gene, they will pass it on to their child. If a parent has no copies, they will not pass it on. If a parent has one copy, the gene is passed on with a probability of 0.5. After a gene is passed on, it may mutate: changing from a gene that causes hearing impairment to one that doesn’t, or vice versa.

We model these relationships using a Bayesian network. For a family with two parents and one child, the network looks like this:

```
          MotherGene               FatherGene
          {0,1,2}  |                | {0,1,2}
            |      |                |       |
            v      |                |       v
      MotherTrait  |                |  FatherTrait
       {Yes,No}    |                |    {Yes,No}
                   v                v
                        ChildGene
                         {0,1,2}
                            |
                            v
                        ChildTrait
                         {yes,no}
```

Each family member has a `Gene` variable representing the number of GJB2 copies (0, 1, or 2) and a `Trait` variable indicating whether they exhibit the trait (yes or no). Arrows in the network represent dependencies: a person’s genes affect their trait probability, and a child’s genes depend on their parents' genes.

My task in this project is to use this model to infer probabilities for each person's genes and traits based on given data.

## Understanding

The project consists of a `data` folder and `heredity.py`.

- The `data` folder contains CSV files for three families. The first row of each file defines the name, mother, father, and trait. Subsequent rows contain family members, their parents, and trait information. Empty cells indicate unknown parent or trait information.
  
- `heredity.py` contains the AI logic. `PROBS` is a dictionary with constants for unconditional gene probabilities, trait probabilities based on gene count, and gene mutation probabilities.

The main function loads data from a CSV file into the `people` dictionary, which maps each person's name to another dictionary containing their information. The function also initializes a `probabilities` dictionary with all values set to 0. This dictionary stores the computed probabilities for each person's gene count and trait.

We calculate these probabilities based on evidence: given known traits, we determine the probabilities. The project involves implementing three functions: `joint_probability` to compute joint probabilities, `update` to add computed probabilities to the existing distribution, and `normalize` to ensure distributions sum to 1.

## Specification

### `joint_probability`

Computes the joint probability of gene and trait configurations.

- **Inputs:**
  - `people`: dictionary of family members.
  - `one_gene`: set of people with one gene copy.
  - `two_genes`: set of people with two gene copies.
  - `have_trait`: set of people with the trait.

- **Outputs:**
  - Joint probability of the given gene and trait configurations.

### `update`

Adds a new joint probability to existing distributions.

- **Inputs:**
  - `probabilities`: dictionary of people and their gene/trait probabilities.
  - `one_gene`, `two_genes`, `have_trait`: as above.
  - `p`: computed joint probability.

- **Outputs:**
  - Updates the `probabilities` dictionary.

### `normalize`

Normalizes probability distributions so they sum to 1.

- **Inputs:**
  - `probabilities`: dictionary of people and their gene/trait probabilities.

- **Outputs:**
  - Updates the `probabilities` dictionary.

## Example of Joint Probability

Consider the following `people` dictionary:

```python
{
  'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None},
  'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True},
  'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False}
}
```

We calculate `joint_probability(people, {"Harry"}, {"James"}, {"James"})`. This represents the probability that:
- Lily has 0 copies of the gene and does not have the trait.
- Harry has 1 copy of the gene and does not have the trait.
- James has 2 copies of the gene and has the trait.

1. **Lily:**
   - Probability of 0 copies: 0.96 (PROBS["gene"][0])
   - Probability of no trait: 0.99 (PROBS["trait"][0][False])
   - Joint probability: 0.96 * 0.99 = 0.9504

2. **James:**
   - Probability of 2 copies: 0.01 (PROBS["gene"][2])
   - Probability of trait: 0.65 (PROBS["trait"][2][True])
   - Joint probability: 0.01 * 0.65 = 0.0065

3. **Harry:**
   - Probability of 1 copy: 0.9802 (from mutation and inheritance probabilities)
   - Probability of no trait: 0.44 (PROBS["trait"][1][False])
   - Joint probability: 0.9802 * 0.44 = 0.431288

**Overall joint probability:** 0.9504 * 0.0065 * 0.431288 = 0.0026643247488
```

Feel free to make any additional changes or let me know if there's anything else you'd like to include!
