"""
Coursera Week 1 Projects
"""
EX_GRAPH0 = {0:set([1, 2]), 1:set([]), 2:set([])}

EX_GRAPH1 = {0:set([1, 4, 5]), 1:set([2, 6]), 2:set([3]), 3:set([0]), 4:set([1]), 5:set([2]), 6:set([])}

EX_GRAPH2 = {0:set([1, 4, 5]), 1:set([2, 6]), 2:set([3, 7]), 3:set([7]), 4:set([1]), 5:set([2]), 6:set([]), 7:set([3]), 8:set([1, 2]), 9:set([0, 3, 4, 5, 6, 7])}

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

	for node in keys:
		in_degree = compute_graph[node]
		result_dict[in_degree] += 1
	
	for node in result_dict.keys():
		if result_dict[node] == 0:
			del result_dict[node]
	
	return result_dict



