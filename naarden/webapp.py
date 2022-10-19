# Entry point for the application.
from lib2to3.pytree import NodePattern
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
        if self.empty():
            raise Exception("Frontier empty")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


    def empty(self):
        return len(self.frontier) == 0
    
    #def contains_state(self, state):
    #    return any(state == node.state for node in self.frontier)

    
class Model():
    def __init__(self, user:int):
        row = Relationships.query.filter_by(user_id=user).first()
        self.file = json.loads(row.file)
        self.solutions = [] # list of solutions (all possible paths)
        self.num_tables = len(self.file)
        #self.num_relations = len(relation for table in self.file for relation in table if relation)

    def neighbors(self, node): # states
        """ Gets state's node and return its neighbors nodes """
        neighbor = None
        neighbors = []
        # find node name from file to posteriory find its neigthbors
        try:
            for from_node in self.file[node.state]:
                neighbor = Node(state=from_node['to']['table'], key=from_node['to']['key'], parent=node)
                neighbors.append(neighbor)
            return neighbors
        except KeyError:
            print(f'Branch ends in Node {node.state}.')

    

    def _optimal_solution(self, nodes_to_find, solutions): # states
        """ Returns the smalles list that contains all nodes states present in nodes_to_find """
        # sort the list of possible solutions (another lists) based on the sortest path (so smallest)
        sorted_solutions = sorted(solutions , key=lambda l: len(l))
        # solution found!, if all nodes are present in the solution
        for solution in sorted_solutions:
            if all(True if n in solution else False for n in nodes_to_find):
                return solution
        return None 

    def _validate_solution(self, nodes_to_find, solution): # states
        """ Returns True if it is a valid solution. Otherwise, False. 
            True; all variables from nodes_to_find are present in solution
        """
        return all(True if n in solution else False for n in nodes_to_find)

    def solve(self, nodes_to_find):
        
        solution = []

        if len(nodes_to_find) == 1:
            return nodes_to_find[0]

        # add first node
        for new_start in nodes_to_find:
            start = Node(new_start, None, None)
            frontier = StackFrontier()
            self.explored = set()
            frontier.add(start)

            print(f'Start branch node: {start.state}')

            while True:
                
                if frontier.empty():
                    print("Finished. there is no more relations between nodes")
                    break

                # get a node from a frontier
                node = frontier.remove()

                print(f'Explore node: {node.state}')

                # add this node as explored node
                self.explored.add(node.state)

                # from this node find a neighbors nodes
                _neighbors = self.neighbors(node)

                if _neighbors:
                    # remove explore nodes from the neighbors
                    neighbors = [n for n in _neighbors if n.state not in self.explored]
                    
                    frontier.frontier += neighbors

                    #for neighbors in neighbors:
                    #    frontier.add(neighbors)
                else:
                    # end of a branch. Possible solution.
                    while True:
                        solution.append(node.state)
                        if node.parent is None:
                            break
                        node = node.parent
                    
                    solution.reverse()
                    print(f'Posible solution: {solution}')
                    if self._validate_solution(nodes_to_find, solution):
                        print(f'Valid solution: {solution}')
                        self.solutions.append(solution)
                    solution = []

        print(f'Final solution: {self.solutions}')
        return self.solutions