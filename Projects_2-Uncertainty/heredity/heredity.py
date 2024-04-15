import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """

    # In order to avoid big tree of if, using a if for each case, I decided to work with dictionaries.

    # Dictionary for the chance of a parent giving a gene, depending of their gene
    parents_genes_prob = {
        1: {
            # Considered the one having the gene
            "gene1": {
                "passing": 1 - PROBS["mutation"],
                "not": PROBS["mutation"],
            },
            # Considered the one not having the gene
            "gene2": {
                "passing": PROBS["mutation"],
                "not": 1 - PROBS["mutation"],
            },
        },

        2: {
            "gene1": {
                "passing": 1 - PROBS["mutation"],
                "not": PROBS["mutation"],
            },

            "gene2": {
                "passing": 1 - PROBS["mutation"],
                "not": PROBS["mutation"],
            },
        },

        0: {
            "gene1": {
                "passing": PROBS["mutation"],
                "not": 1 - PROBS["mutation"],
            },

            "gene2": {
                "passing": PROBS["mutation"],
                "not": 1 - PROBS["mutation"],
            }
        },

    }

    # intializing the probability dictionary for each person in the family
    chances = dict()

    # initializing the gene count dictionary for each person in the family
    gene_count = dict()
    for key in people.keys():
        chances[key] = 1
        if key in one_gene:
            gene_count[key] = 1
        elif key in two_genes:
            gene_count[key] = 2
        else:
            gene_count[key] = 0

    # finding the probability of each person
    for person_info in people.values():
        name = person_info["name"]
        mother = person_info["mother"]
        father = person_info["father"]
        # trait = person_info["trait"] - wasn't used.

        # Could've also used:
        # name, mother, father, trait = person_info.values()

        # If father and mother is unknown
        if mother == None:
            # use uncoditional probability
            if name in have_trait:
                chances[name] = (chances[name] *
                                 PROBS["gene"][gene_count[name]] *
                                 PROBS["trait"][gene_count[name]][True])
            else:
                chances[name] = (chances[name] *
                                 PROBS["gene"][gene_count[name]] *
                                 PROBS["trait"][gene_count[name]][False])

        # if the parents are known
        else:

            # Initializing the chance of each gene matchup
            gene_match = 1

            # If this person is in the one_gene list
            if gene_count[name] == 1:

                # Since this can be done by receiving the gene by the mother or the father, this will be split in two.
                gene_match1 = 1
                gene_match2 = 1

                # Chances of getting the gene from the mother and not from the father
                gene_match1 = (gene_match1 *
                               ((parents_genes_prob[gene_count[mother]]["gene1"]["passing"] + parents_genes_prob[gene_count[mother]]["gene2"]["passing"])/2) *
                               ((parents_genes_prob[gene_count[father]]["gene1"]["not"] + parents_genes_prob[gene_count[father]]["gene2"]["not"])/2))

                # Chances of getting the gene from the father and not from the mother
                gene_match2 = (gene_match2 *
                               ((parents_genes_prob[gene_count[mother]]["gene1"]["not"] + parents_genes_prob[gene_count[mother]]["gene2"]["not"])/2) *
                               ((parents_genes_prob[gene_count[father]]["gene1"]["passing"] + parents_genes_prob[gene_count[father]]["gene2"]["passing"])/2))

                # the actual change of the son/daugher having 1 gene is the sum of the chances of both cases
                gene_match = gene_match1 + gene_match2

            # If this person is in the two_genes list, they must receive a gene from both parents
            elif gene_count[name] == 2:
                gene_match = (gene_match *
                              ((parents_genes_prob[gene_count[mother]]["gene1"]["passing"] + parents_genes_prob[gene_count[mother]]["gene2"]["passing"])/2) *
                              ((parents_genes_prob[gene_count[father]]["gene1"]["passing"] + parents_genes_prob[gene_count[father]]["gene2"]["passing"])/2))

            # If this person is not in any gene list, they must not receive a gene from any parents
            else:
                gene_match = (gene_match *
                              ((parents_genes_prob[gene_count[mother]]["gene1"]["not"] + parents_genes_prob[gene_count[mother]]["gene2"]["not"])/2) *
                              ((parents_genes_prob[gene_count[father]]["gene1"]["not"] + parents_genes_prob[gene_count[father]]["gene2"]["not"])/2))

            # multipling their chance of having this gene by the chance of having(or not) the trait
            if name in have_trait:
                chances[name] = chances[name] * gene_match * PROBS["trait"][gene_count[name]][True]
            else:
                chances[name] = chances[name] * gene_match * PROBS["trait"][gene_count[name]][False]

    joint_probs = 1

    # getting the joint probability for this family.
    for name in chances.keys():
        joint_probs = joint_probs * chances[name]

    return joint_probs

    raise NotImplementedError


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    for person in probabilities:
        if person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        else:
            probabilities[person]["gene"][0] += p
        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p

    # raise NotImplementedError


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """

    # To normalize (make sure their sum is equal to 1)
    # all we have to do is to sum all probabilities, get the sum and then divide each probabily by that sum

    for person in probabilities:

        # for the genes
        total_gene = (probabilities[person]["gene"][0]
                      + probabilities[person]["gene"][1]
                      + probabilities[person]["gene"][2])

        probabilities[person]["gene"][0] = probabilities[person]["gene"][0]/total_gene
        probabilities[person]["gene"][1] = probabilities[person]["gene"][1]/total_gene
        probabilities[person]["gene"][2] = probabilities[person]["gene"][2]/total_gene

        # for the trait
        total_trait = (probabilities[person]["trait"][True] +
                       probabilities[person]["trait"][False])

        probabilities[person]["trait"][True] = probabilities[person]["trait"][True]/total_trait
        probabilities[person]["trait"][False] = probabilities[person]["trait"][False]/total_trait

    # raise NotImplementedError


if __name__ == "__main__":
    main()
