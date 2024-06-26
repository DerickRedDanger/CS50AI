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

    # to keep tract of how long it took for the code to run
    start_time = time.time()

    # if the target is the source it self, then degree = 0
    if source == target:
        return []
    
    # Node(state, parent, parent_movie, movie_children,level)
    start = Node(source, False, False, neighbors_for_person(source), 0)

    Queue = QueueFrontier()

    # creating a set with all actors that were already explored
    actors_explored = set()
    actors_explored.add(start)

    # Looping inside all of Movie_children/Person_chieldren pair of the source actor
    # In other world, looping inside the pair that contain the movie the actor starred and another actor present in the same movie
    for movie_person_pair in start.movie_children:

        # If the actor is not the target, and not in the explored list, 
        # create a new node based on him and add to the queue.
        if movie_person_pair[1] != target:
            if movie_person_pair[1] not in actors_explored:
                node = Node(movie_person_pair[1], start, movie_person_pair[0], neighbors_for_person(movie_person_pair[1]), (start.level+1))
                Queue.add(node)
                actors_explored.add(movie_person_pair[1])

        # If the actor is the target, append the pair to shortest and return it.
        else:
            shortest = []
            shortest.append(movie_person_pair)
            return shortest
        
    # If the target was not found in the initial attempt, 
    # repeat the process the process till he is found or the queue is empty.
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
        for movie_person_pair in node.movie_children:
            """""
            For debugging purpose
            print (f"movie_person_pair = {movie_person_pair}")
            print(f"Movie = {movie_person_pair[0]}")
            print(f"child = {movie_person_pair[1]}")
            """""
            if movie_person_pair[1] != target:
                if movie_person_pair[1] not in actors_explored and node.level <= 5:

                    child = Node(movie_person_pair[1], node, movie_person_pair[0], neighbors_for_person(movie_person_pair[1]), (node.level + 1))
                    Queue.add(child)
                    actors_explored.add(movie_person_pair[1])

            # If the target is found, appent the pair to shortest, backtrack throught it's parents
            # appending their pair until reaching the source Actor, then revert the shortest order and return
            else:
                shortest = []
                shortest.append(movie_person_pair)
                x = 0
                while x <= 6:
                    if node.parent != False:
                        shortest.append((node.parent_movie, node.state))
                        node = node.parent

                    else:
                        shortest.reverse()
                        # to keep tract of how long it took for the code to run
                        end_time = time.time()
                        print(f"Total time of running the code = {end_time - start_time}")
                        return shortest
                    x += 1

    # to keep tract of how long it took for the code to run
    end_time = time.time()
    print(f"Total time of running the code = {end_time - start_time}")

    # If the queue is empty and the target wasn't found, return None.
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
