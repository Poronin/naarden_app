# Entry point for the application.
from os import remove
from naarden import app    # For application discovery by the 'flask' command.
from naarden import views  # For import side-effects of setting up routes.
from naarden.models import Relationships
import json
import collections

class Node():
    """ Create a new Node (Table) """
    def __init__(self, state, key, parent):
        self.state = state # name of the table
        self.key = key # not required
        self.parent = parent


class StackFrontier():
    def __init__(self):
        self.frontier = []
    
    def add(self, node):
        self.frontier.append(node)
    
    def remove(self):
        try:
            self.frontier.pop(-1)
        except KeyError:
            print("Frontier empty")

    def empty(self):
        return len(self.frontier) == 0
    
    def contains_state(self, state):
        return any(state == node.state for node in self.frontier)

    
class Model():
    def __init__(self, user:int):
        row = Relationships.query.filter_by(user_id=user).first()
        self.file = json.loads(row.file)
        self.solutions = [] # list of solutions (all possible paths)
        self.num_tables = len(self.file)
        #self.num_relations = len(relation for table in self.file for relation in table if relation)

    def neighbors(self, node):
        neighbord = None
        # find node name from file to posteriory find its neigthbors
        for from_node in self.file[node]:
            neighbords = []
            if node.state==from_node['from']['table']:
                neighbord = Node(state=from_node['to']['table'], key=from_node['to']['key'], parent=from_node['from']['table'])
                neighbords.append(neighbord)
                return neighbords
        return None

    def optimal_solution(self, nodes_to_find, solutions):
        """ Returns the smalles list that contains all nodes present in nodes_to_find """
        # sort the list of possible solutions (another lists) based on the sortest path (so smallest)
        sorted_solutions = sorted(solutions , key=lambda l: len(l))
        # solution found!, if all nodes are present in the solution
        for solution in sorted_solutions:
            if all(True if n in solution else False for n in nodes_to_find):
                return solution
        return None 

    def validate_solution(self, nodes_to_find, solution):
        """ Returns True if it is a valid solution. Otherwise, False. 
            True; all variables from nodes_to_find are present in solution
        """
        return all(True if n in solution else False for n in nodes_to_find)

    def solve(self, nodes_to_find):

        solution = []

        #add first node
        for new_start in nodes_to_find:
            start = Node(new_start, None, None)
            frontier = StackFrontier()
            self.explored = set()
            frontier.add(start)

            while True:
                
                if frontier.empty():
                    raise "there is not relations between nodes"  # type: ignore

                # get a node from a frontier
                node = frontier.remove()

                # add this node as explored node
                self.explored.add(node.state)  # type: ignore

                _neighbors = self.neighbors(node.state)  # type: ignore
                if len(solution) > 0 and not _neighbors:
                    self.solutions.append(solution)
                    solution = []
                else:
                    # find its neighbors and add frontier if was not explored yet
                    for _neighbord in self.neighbors(node.state):  # type: ignore
                        if _neighbord.state not in self.explored:
                            solution.append(_neighbord)
                            frontier.add(_neighbord)

        return None