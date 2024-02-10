import csv
import sys
import time
from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    # ---- TODO ---
    """""
    My code starts from here
    """""
    #  if the target is the source it self, the degree = 0
    if source == target:
        return []
    #  to keep tract of how long it took for the code to run
    start_time = time.time()

    """
    Modifications do the util.Node:
    added .parent_movie and .level
    changed .actions to .movie_children

    Node(state, parent, parent_movie, movie_children,level)
    """

    start = Node(source, False, False, neighbors_for_person(source), 0)

    Queue = QueueFrontier()
    actors_explored = set()
    actors_explored.add(start)

    for i in start.movie_children:
        if i[1] != target:
            if i[1] not in actors_explored:
                node = Node(i[1], start, i[0], neighbors_for_person(i[1]), (start.level+1))
                Queue.add(node)
                actors_explored.add(i[1])
        else:
            shortest = []
            shortest.append(i)
            return shortest

    while not Queue.empty():
        node = Queue.remove()
        """""
        For debugging purpose
        print(f"len(Queue) = {len(Queue.frontier)}")
        print(f"node - actor = {node.state} parent = {node.parent.state} parent_movie = {node.parent_movie} Movies/Children = {node.movie_children} level = {node.level}")
        print(f"node = {node}")
        print(f"Degree = {node.level}")
        print (f"level = {node.level}")
        """""
        for i in node.movie_children:
            """""
            For debugging purpose
            print (f"i = {i}")
            print(f"Movie = {i[0]}")
            print(f"child = {i[1]}")
            """""
            if i[1] != target:
                if i[1] not in actors_explored and node.level <= 5:

                    child = Node(i[1], node, i[0], neighbors_for_person(i[1]), (node.level + 1))
                    Queue.add(child)
                    actors_explored.add(i[1])

            else:
                shortest = []
                shortest.append(i)
                x = 0
                while x <= 6:
                    if node.parent != False:
                        shortest.append((node.parent_movie, node.state))
                        node = node.parent

                    else:
                        shortest.reverse()
                        #  to keep tract of how long it took for the code to run
                        end_time = time.time()
                        print(f"Total time of running the code = {end_time - start_time}")
                        return shortest
                    x += 1

    #  to keep tract of how long it took for the code to run
    end_time = time.time()
    print(f"Total time of running the code = {end_time - start_time}")
    return None


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
