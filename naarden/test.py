from naarden.webapp import Model
from naarden.webapp import Node
from naarden.webapp import QueueFrontier
# importing required library
import itertools

model = Model(1)

# nodes input from user
nodes_to_find = ['A','G']

model.search(nodes_to_find)

model.remove_bidirectional_nodes()

model.solutions











# create a set of pair nodes
nodes_to_find = list(pairwise(nodes_to_find))

# for each pair of node find the best path
for pair_nodes in nodes_to_find:    
    solutions.append(model.solve(pair_nodes))

solutions

final = []
for solution in solutions:
    l = (list(pairwise(solution)))
    final += l


# remove one bidirectional node example: [('A','B') ('B','A')] return [('A','B')]
for node in final:
    rev_node = node[::-1]
    for node in final:
        if rev_node == node:
            final.remove(rev_node)
final

s = pairwise(['D', 'B', 'A', 'C', 'H'])
s = set(s)
s.add(('A','C'))
s


node_A = Node('A', None, None)
node_B = Node('B', None, None)
node_C = Node('C', None, None)


frontier.add(node_A)
frontier.add(node_B)
frontier.add(node_C)

frontier.frontier

node = frontier.remove()
print(node)
#model.num_tables

neighbors_A = model.neighbors(node_A);
neighbors_B = model.neighbors(node_B);

for n in neighbors_A:
    print(f'\n Node:{n.state} \n Key:{n.key}\n Parent:{n.parent.state}')
 
for n in neighbors_B:
    print(f'\n Node:{n.state} \n Key:{n.key}\n Parent:{n.parent.state}')
 
neighbors_A += neighbors_B

for n in neighbors_A:
       print(f'\n Node:{n.state} \n Key:{n.key}\n Parent:{n.parent.state}')
 
frontier.frontier += ['a']

frontier.frontier

[True if n in ['A','B','C'] else False for n in ['A','B']]