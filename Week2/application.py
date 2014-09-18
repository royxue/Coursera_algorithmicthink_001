"""
Week 2 Application
"""
from collections import deque
import random

def bfs_visited(ugraph, start_node):
	"""
	BFS Visited Algorithm
	"""
	queue = deque()
	visited = set([start_node])
	queue.append(start_node)

	while queue:
		node = queue.popleft()
		for neighbor in ugraph[node]:
			if neighbor not in visited:
				visited.add(neighbor)
				queue.append(neighbor)
				
	return visited


def cc_visited(ugraph):
	"""
	CC Visited Algorithm
	"""

	remainings = [node for node in ugraph.keys()]
	component = []

	while remainings:
		node_c = random.choice(remainings)
		connect = bfs_visited(ugraph, node_c)
		component.append(connect)
		for node in connect:
			remainings.remove(node)

	return component

def largest_cc_size(ugraph):
	"""
	Returns largest connected component in ugraph.
	"""
	component = cc_visited(ugraph)
	max_len = 0

	for c_set in component:
		if len(c_set) > max_len:
			max_len = len(c_set)

	return max_len


def compute_resilience(ugraph, attack_order):
	"""
	Compute resilience for ugraph
	"""
	component = []
	component.append(largest_cc_size(ugraph))

	for node in attack_order:
		if node in ugraph.keys():
			for edge in ugraph[node]:
				ugraph[edge].remove(node)
			ugraph.pop(node)

		component.append(largest_cc_size(ugraph))

	return component







