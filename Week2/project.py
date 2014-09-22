"""
Provided code for Application portion of Module 2
"""

# general imports
import urllib2
import random
import time
import math
import application
import random
from application import compute_resilience
import matplotlib.pyplot as plt
import time 

# CodeSkulptor import
#import simpleplot
#import codeskulptor
# codeskulptor.set_timeout(60)

# Desktop imports
import matplotlib.pyplot as plt


#
# Provided code

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph


def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)


def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)

    order = []
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node

        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order


#
# Code for loading computer network graph
NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"


def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[: -1]

    print "Loaded graph with", len(graph_lines), "nodes"

    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1: -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

#
# My Code

def load_graph_offline(file_addr):
    """
    Offline load graph file
    """
    graph_file = open(file_addr)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[: -1]

    print "Loaded graph with", len(graph_lines), "nodes"

    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1: -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

def random_order(graph):
    """
    Generate a random node order from a graph
    """

    nodes = graph.keys()
    random.shuffle(nodes)

    return nodes

def make_er_graph(num_nodes, p):
    """
    Generate ER graph
    """

    if num_nodes > 0:
        result_dict = {node: set([]) for node in range(num_nodes)}
        node_list = result_dict.keys()
        for node in node_list:
            others = node_list[:]
            others.pop(node)
            for other_node in others:
                if random.random() < p:
                    result_dict[node].add(other_node)
                    result_dict[other_node].add(node)

    return result_dict

class UPATrial:
    """
    Simple class to encapsulate optimizated trials for the UPA algorithm
    
    Maintains a list of node numbers with multiple instance of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a UPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_nodes trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that each node number
        appears in correct ratio
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for _ in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        for dummy_idx in range(len(new_node_neighbors)):
            self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors

def make_complete_graph(num_nodes):
    """
    Generate full connected directed graph

    :para num_nodes: Graph node number
    """
    result_dict = {}

    if num_nodes > 0:
        node_list = [node for node in range(0, num_nodes)]
        for node in node_list:
            others = node_list[:]
            others.pop(node)
            result_dict[node] = set(others)

    return result_dict

def UPA(n, m):
    """
    Implemention of UPA algorithm
    """
    graph = make_complete_graph(m)
    trial = UPATrial(m)

    for node in range(m, n):
        new_set = trial.run_trial(m)
        graph[node] = new_set
        for edge_node in new_set:
            graph[edge_node].add(node)

    return graph

#ex_graph = load_graph_off(NETWORK_URL)
# ex_graph = load_graph_offline("alg_rf7.txt")
# er_graph = make_er_graph(1347, 0.0017164333)
# upa_graph = UPA(1347, 2)

# ex_rand = random_order(ex_graph)
# er_rand = random_order(er_graph)
# upa_rand = random_order(upa_graph)

# ex_resilience = compute_resilience(ex_graph, ex_rand)
# er_resilience = compute_resilience(er_graph, er_rand)
# upa_resilience = compute_resilience(upa_graph, upa_rand)

# # Results Plot
# plt.title("Resilience Results Plot")
# plt.plot([num for num in range(len(ex_rand)+1)], ex_resilience, '-b', label='Graph')
# plt.plot([num for num in range(len(er_rand)+1)], er_resilience, '-r', label='ER Graph')
# plt.plot([num for num in range(len(upa_rand)+1)], upa_resilience, '-g', label='UPA Graph')    
# plt.legend(loc='upper right')
# plt.show()

# 
# Fast Target order

def fast_targeted_order(ugraph):
    """
    Fast Target Order Implemention
    """
    order = []
    num_nodes = len(ugraph)
    new_graph = copy_graph(ugraph)
    degree_sets = [set() for node in new_graph.keys()]
    distribution = {}

    for node, edge in new_graph.items():
        if len(edge) not in distribution:
            distribution[len(edge)] = set([node])
        else:
            distribution[len(edge)].add(node)

    for degree in range(num_nodes):
        if degree in distribution:
            degree_sets[degree] = distribution[degree]

    for degree in range(num_nodes-1, -1, -1):
        while degree_sets[degree] != set():
            dmax_node = degree_sets[degree].pop()

            for neighbor in new_graph[dmax_node]:
                neigh_deg = len(new_graph[neighbor])
                degree_sets[neigh_deg].remove(neighbor)
                degree_sets[neigh_deg-1].add(neighbor)

            order.append(dmax_node)
            delete_node(new_graph, dmax_node)

    return order

def timming(func):
    time_list = []
    for num_nodes in range(10, 1000, 10):
        upa_graph_now = UPA(num_nodes, 5)

        start_t = time.clock()
        func(upa_graph_now)
        end_t = time.clock()

        time_list.append(end_t - start_t)

    return time_list

timming_nodes = [node for node in range(10, 1000, 10)]

# plt.title("Timing in Desktop Python")
# plt.xlabel("upa_The number of nodes")
# plt.ylabel("time")
# plt.plot(timming_nodes, timming(targeted_order), '-r', label='targeted_order')
# plt.plot(timming_nodes, timming(fast_targeted_order), '-b', label='fast_targeted_order')
# plt.show()


# Question 4
ex_graph = load_graph_offline("alg_rf7.txt")
er_graph = make_er_graph(1347, 0.0017164333)
upa_graph = UPA(1347, 2)

ex_rand = fast_targeted_order(ex_graph)
er_rand = fast_targeted_order(er_graph)
upa_rand = fast_targeted_order(upa_graph)

ex_resilience = compute_resilience(ex_graph, ex_rand)
er_resilience = compute_resilience(er_graph, er_rand)
upa_resilience = compute_resilience(upa_graph, upa_rand)

# # Results Plot
plt.title('Three Graph Resilience result with fast_targeted_order')
plt.plot([num for num in range(len(ex_rand)+1)], ex_resilience, '-b', label='Graph')
plt.plot([num for num in range(len(er_rand)+1)], er_resilience, '-r', label='ER Graph')
plt.plot([num for num in range(len(upa_rand)+1)], upa_resilience, '-g', label='UPA Graph')    
plt.legend(loc='upper right')
plt.show()





