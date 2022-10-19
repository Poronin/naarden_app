# Entry point for the application.
from lib2to3.pytree import NodePattern
from os import remove
from naarden import app    # For application discovery by the 'flask' command.
from naarden import views  # For import side-effects of setting up routes.
from naarden.models import Relationships
import json
import collections
import itertools


class Node():
    """ Create a new Node (Table) """
    def __init__(self, state, key, parent):
        self.state = state # name of the table
        self.key = key # not required
        self.parent = parent


class QueueFrontier():
    def __init__(self):
        self.frontier = []
    
    def add(self, node):
        self.frontier.append(node)
    
    def remove(self):
        if self.empty():
            raise Exception("Frontier empty")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
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

    def pairwise(self, iterable):
        "s -> (s0,s1), (s1,s2), (s2, s3), ..."
        a, b = itertools.tee(iterable)
        next(b, None)
        return zip(a, b)

    def get_path(self, pair_node):
        """ Get the shortest path bewteen two nodes """
        max_branch_length = 9999
        solution = []
        solutions = []

        if 2 < len(pair_node) < 1:
            raise Exception("Parameter exptect two values")


        if len(pair_node) == 1:
            return pair_node[0]

        # add first node
        for new_start in pair_node:
            start = Node(new_start, None, None)
            frontier = QueueFrontier()
            self.explored = set()
            branch_length = 0
            frontier.add(start)

            print(f'Start branch node: {start.state}')

            while True:
                
                if frontier.empty():
                    print("Finished. there is no more relations between nodes")
                    break

                # get a node from a frontier
                node = frontier.remove()
                
                if branch_length < max_branch_length:
                    # add this node as explored node
                    self.explored.add(node.state)
                    # from this node find a neighbors nodes
                    _neighbors = self.neighbors(node)
                    # remove explore nodes from the neighbors
                    neighbors = [n for n in _neighbors if n.state not in self.explored]
                    # add them to the frontier
                    frontier.frontier += neighbors

                    # for each new node check if it is a possible path containing the solution.
                    while True:
                        solution.append(node.state)
                        if node.parent is None:
                            break
                        node = node.parent
                    
                    solution.reverse()
                    # branch length
                    branch_length = len(solution)
                    print(f'\tPosible solution: {solution}. Branch num: {branch_length}')
                    
                    if self._validate_solution(pair_node, solution):
                        if len(solution) < max_branch_length:
                            max_branch_length = len(solution)
                        print(f'\t\t\t Valid solution: {solution}\n\t\t\t Max_branch length: {max_branch_length}')
                        solutions.append(solution)
                    solution = []  
                else:
                    print(f'\tExceed max branch length: {node.state}')
                    solution = []
                    break

        print(f'Final solutions: {solutions}')
        return self._optimal_solution(pair_node, solutions)

    def remove_bidirectional_nodes(self):   
        if len(self.solutions)==1:
            return False
        # Remove one bidirectional node example: [('A','B') ('B','A')] return [('A','B')]
        for node in self.solutions:
            rev_node = node[::-1]
            for node in self.solutions:
                if rev_node == node:
                    self.solutions.remove(rev_node)
        return None

    def search(self, nodes_to_find):
        """ Gets a list of nodes and return a path that joins them all based on the model
            It returns a list of tupple where each tupple indicate a join between two nodes """
        unified_paths = []
        
        if len(nodes_to_find) == 1:
            self.solutions = nodes_to_find
            return self.solutions
        
        # create a set of pair nodes. For example: convert ['A','B','C'] into [('A','B') ('B','C')]
        nodes_to_find = list(self.pairwise(nodes_to_find))
        # for each pair of node find the best path
        for pair_nodes in nodes_to_find:    
            self.solutions.append(self.get_path(pair_nodes))

        # create pair set of two. For example: convert ['A','B','C'] into [('A','B') ('B','C')]
        for path in self.solutions:
            p = (list(self.pairwise(path)))
            unified_paths += p
        self.solutions = list(set(unified_paths))
        
        return self.solutions



