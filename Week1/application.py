"""
Provided code for Application portion of Module 1

"""

# general imports
import urllib2
import matplotlib.pyplot as plt
import random

# Set timeout for CodeSkulptor if necessary
#import codeskulptor
#codeskulptor.set_timeout(20)


###################################
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

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

def compute_in_degrees(digraph):
    """
    Compute in-degree of each node in digraph
    """
    keys = digraph.keys()   
    result_dict = {node:0 for node in keys}

    for node in keys:
        for head in digraph[node]:
            result_dict[head] += 1
    
    return result_dict

def in_degree_distribution(digraph):
    """
    Compute in degree distribution of digraph
    """
    compute_graph = compute_in_degrees(digraph)
    keys = compute_graph.keys()
    result_dict = {num:0 for num in range(0, len(keys))}
    sum_num = 0.0

    for node in keys:
        in_degree = compute_graph[node]
        result_dict[in_degree] += 1
        sum_num += in_degree

    for node in result_dict.keys():
        if result_dict[node] == 0:
            del result_dict[node]
        else:
            result_dict[node] = result_dict[node]/sum_num
    
    return result_dict

def dict2list(raw_dict):
    keys = raw_dict.keys()
    values = [raw_dict[key] for key in keys]

    return [keys, values]

# Question_1
# citation_graph = load_graph(CITATION_URL)
# in_degree_citation_graph = in_degree_distribution(citation_graph)
# distribution = dict2list(in_degree_citation_graph)

# plt.loglog(distribution[0], distribution[1], 'ro')
# plt.xlabel('in degree')
# plt.ylabel('frequency')
# plt.title("Application 1 in-degree distribution graph")
# plt.show()

# Question_2
# def New_ER(node_num, p):

# Question_3
# edge_sum = 0
# count_graph = compute_in_degrees(load_graph(CITATION_URL))
# for key in count_graph.keys():
#     edge_sum += count_graph[key]
# print edge_sum
# m = edge_sum/len(count_graph.keys())
    
# Question_4
"""
My slow version, abandoned
"""
# def DPA(n, m):
#     """
#     Implemention of DPA algorithm
#     """
#     graph = make_complete_graph(m)

#     for node in range(m, n):
#         # print "node finished"
#         # in_degree_sum = sum([sum(graph[idx]) for idx in graph.keys()])
#         # new_set = set([])
#         # for node_1 in graph.keys():
#         #     rand_num = random.random()
#         #     bound = (sum(graph[node_1]) + 1.0)/(in_degree_sum + len(graph.keys()))
#         #     if rand_num > bound:
#         #         new_set.add(node_1)
#         # graph[node] = new_set

#     return graph

class DPATrial:
    """
    Simple class to encapsulate optimized trials for DPA algorithm
    
    Maintains a list of node numbers with multiple instances of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a DPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]

    def run_trial(self, num_nodes):
        """
        Conduct num_node trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that the number of instances of
        each node number is in the same ratio as the desired probabilities
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for dummy_idx in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors

def DPA(n, m):
    """
    Implemention of DPA algorithm
    """
    graph = make_complete_graph(m)
    trial = DPATrial(m)

    for node in range(m, n):
        print 1
        new_set = trial.run_trial(node)
        graph[node] = new_set

    return graph

DPA_graph = DPA(27770, 13)
in_degree_DPA_graph = in_degree_distribution(DPA_graph)
DPA_list = dict2list(in_degree_DPA_graph)
print DPA_list

plt.loglog(DPA_list[0], DPA_list[1], 'bo')
plt.xlabel('in degree')
plt.ylabel('frequency')
plt.title("DPA in-degree distribution graph")
plt.show()



