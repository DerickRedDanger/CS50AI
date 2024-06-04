# Read me

The problem and it's full description is avaliable in the link: 
https://cs50.harvard.edu/ai/2024/projects/2/heredity/

## Introduction:

This project aim to write an AI that assess the likelihood that a person will have a particular genetic trait. That is done by assessing their parents gene (or, if we lack that knowledge, throught the inconditional probability of a person having theses genes) and utilizing join probability and Bayesian Network to find the chance of each different set up to happen. Ultimally summing and normalizing all of these chances until we find the chance of each separated gene/trait.

## Utilization:

* cd inside heredity folder.

* run in the terminal: python heredity.py data/family.csv (where family can be family0,1 or 2. Each csv containing the data of a small family)

* The terminal will them show the chances of each member of that family to contain 0,1 or 2 genes and the chances of them having the trait or not.

## Background:

Mutated versions of the GJB2 gene are one of the leading causes of hearing impairment in newborns. Each person carries two versions of the gene, so each person has the potential to possess either 0, 1, or 2 copies of the hearing impairment version GJB2. Unless a person undergoes genetic testing, though, it’s not so easy to know how many copies of mutated GJB2 a person has. This is some “hidden state”: information that has an effect that we can observe (hearing impairment), but that we don’t necessarily directly know. After all, some people might have 1 or 2 copies of mutated GJB2 but not exhibit hearing impairment, while others might have no copies of mutated GJB2 yet still exhibit hearing impairment.

Every child inherits one copy of the GJB2 gene from each of their parents. If a parent has two copies of the mutated gene, then they will pass the mutated gene on to the child; if a parent has no copies of the mutated gene, then they will not pass the mutated gene on to the child; and if a parent has one copy of the mutated gene, then the gene is passed on to the child with probability 0.5. After a gene is passed on, though, it has some probability of undergoing additional mutation: changing from a version of the gene that causes hearing impairment to a version that doesn’t, or vice versa.

We can attempt to model all of these relationships by forming a Bayesian Network of all the relevant variables, as in the one below, which considers a family of two parents and a single child.

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

Each person in the family has a Gene random variable representing how many copies of a particular gene (e.g., the hearing impairment version of GJB2) a person has: a value that is 0, 1, or 2. Each person in the family also has a Trait random variable, which is yes or no depending on whether that person expresses a trait (e.g., hearing impairment) based on that gene. There’s an arrow from each person’s Gene variable to their Trait variable to encode the idea that a person’s genes affect the probability that they have a particular trait. Meanwhile, there’s also an arrow from both the mother and father’s Gene random variable to their child’s Gene random variable: the child’s genes are dependent on the genes of their parents.

My task in this project is to use this model to make inferences about a population. Given information about people, who their parents are, and whether they have a particular observable trait (e.g. hearing loss) caused by a given gene, The AI will infer the probability distribution for each person’s genes, as well as the probability distribution for whether any person will exhibit the trait in question.

## Understanding:

This project is composed of the data folder and heredity.py.

Data holds the csv of three families. The first row of each file defines name, mother, father and trait. The following rows contains each member of the family, it's parents and if they have exhibit the traits. Empty cells for parents or traits symbolises that we don't know if they exibit that trait or have information about their parents.

Heredity.py contains the logic for the Ai. PROBS is a dictionary containing a number of constant representing the uncoditional probability of a person having a number of genes (when we don't have information about their parents), the chance of a person exhibiting a trait depending of the number of genes they have and the probability of a gene mutating when being passed from parents to their children.

Main function Loads data from a csv file into the dictionary people

People matps each person's name to another dictionary containing information about them.

Main also defines a dictionary of probabilities, with all probabilities initially set to 0. This is what the project compute: For each person, the Ai will calculate the probability distribution over how many copies of the gene they have, as well as wheter they have the trait or not.probabilities["Harry"]["gene"][1], for example, will be the probability that Harry has 1 copy of the gene, and probabilities["Lily"]["trait"][False] will be the probability that Lily does not exhibit the trait.

we’re looking to calculate these probabilities based on some evidence: given that we know certain people do or do not exhibit the trait, we’d like to determine these probabilities. My task in this project was to implement three functions to do just that: joint_probability to compute a joint probability, update to add the newly computed joint probability to the existing probability distribution, and then normalize to ensure all probability distributions sum to 1 at the end.

## Specification:

### Joint_probability:

Takes as inpute a dictionary of people, along with data about who has how many copies of each genes, and who exhibits the trait. This function returns the join probability of all those events taking place.

* The function accepts four inputs: people, one_gene, two_gene and have_trait.

  * people is a dictionary of people as described in the “Understanding” section. The keys represent names, and the values are dictionaries that contain mother and father keys. 
  * one_gene is a set of all people for whom we want to compute the probability that they have one copy of the gene.
  * two_genes is a set of all people for whom we want to compute the probability that they have two copies of the gene.
  * have_trait is a set of all people for whom we want to compute the probability that they have the trait.
  * For any person not in one_gene or two_genes, we would like to calculate the probability that they have no copies of the gene; and for anyone not in have_trait, we would like to calculate the probability that they do not have the trait.
* For anyone with no parents listed in the data set, use the probability distribution PROBS["gene"] to determine the probability that they have a particular number of the gene.
* For anyone with parents in the data set, each parent will pass one of their two genes on to their child randomly, and there is a PROBS["mutation"] chance that it mutates (goes from being the gene to not being the gene, or vice versa).

### Update:

adds a new joint distribution probability to the existing probability distributions in probabilities.

* accepts five values as inputs:probabilities, one_gene, two_genes, have_trait, and p.
  * probabilities is a dictionary of people as described in the “Understanding” section. Each person is mapped to a "gene" distribution and a "trait" distribution.
  * p is the probability returned from the joint distribution.
* For each person person in probabilities, the function should update the probabilities[person]["gene"] distribution and probabilities[person]["trait"] distribution by adding p to the appropriate value in each distribution. All other values should be left unchanged.
* The function does not return any value: it just updates the probabilities dictionary.

### Normalize:
updates a dictionary of probabilities such that each probability distribution is normalized (i.e., sums to 1, with relative proportions the same).
* This functions accepts a single value: Probabilities
* For both of the distributions for each person in probabilities, this function normalize that distribution so that the values in the distribution sum to 1, and the relative values in the distribution are the same.
* The function does not return any value: it just updates the probabilities dictionary.

## Example of joint probabilty:
To help you understand how joint probabilities is calculated, I’ve included below the example from Cs50Ai.

Consider the following value for people:

    {
      'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None},

    'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True},

    'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False}
      }

We will here show the calculation of joint_probability(people, {"Harry"}, {"James"}, {"James"}). Based on the arguments, one_gene is {"Harry"}, two_genes is {"James"}, and have_trait is {"James"}. This therefore represents the probability that: Lily has 0 copies of the gene and does not have the trait, Harry has 1 copy of the gene and does not have the trait, and James has 2 copies of the gene and does have the trait.

We start with Lily (the order that we consider people does not matter, so long as we multiply the correct values together, since multiplication is commutative). Lily has 0 copies of the gene with probability 0.96 (this is PROBS["gene"][0]). Given that she has 0 copies of the gene, she doesn’t have the trait with probability 0.99 (this is PROBS["trait"][0][False]). Thus, the probability that she has 0 copies of the gene and she doesn’t have the trait is 0.96 * 0.99 = 0.9504.

Next, we consider James. James has 2 copies of the gene with probability 0.01 (this is PROBS["gene"][2]). Given that he has 2 copies of the gene, the probability that he does have the trait is 0.65. Thus, the probability that he has 2 copies of the gene and he does have the trait is 0.01 * 0.65 = 0.0065.

Finally, we consider Harry. What’s the probability that Harry has 1 copy of the gene? There are two ways this can happen. Either he gets the gene from his mother and not his father, or he gets the gene from his father and not his mother. 

His mother Lily has 0 copies of the gene, so Harry will get the gene from his mother with probability 0.01 (this is PROBS["mutation"]), since the only way to get the gene from his mother is if it mutated; conversely, Harry will not get the gene from his mother with probability 0.99. 

His father James has 2 copies of the gene, so Harry will get the gene from his father with probability 0.99 (this is 1 - PROBS["mutation"]), but will get the gene from his mother with probability 0.01 (the chance of a mutation). 

Both of these cases can be added together to get 0.99 * 0.99 + 0.01 * 0.01 = 0.9802, the probability that Harry has 1 copy of the gene.

Given that Harry has 1 copy of the gene, the probability that he does not have the trait is 0.44 (this is PROBS["trait"][1][False]). So the probability that Harry has 1 copy of the gene and does not have the trait is 0.9802 * 0.44 = 0.431288.

Therefore, the entire joint probability is just the result of multiplying all of these values for each of the three people: 0.9504 * 0.0065 * 0.431288 = 0.0026643247488.