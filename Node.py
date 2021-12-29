from Edge import Edge


class Node:
	def __init__(self, node_number):
		self.node_number = node_number
		self.edges = []

	@property
	def incident_nodes(self):
		return [edge.other_node(self) for edge in self.edges]

	def incident_edges(self):
		for edge in self.edges:
			yield edge

	@staticmethod
	def disconnect(edge):
		edge.start.edges.remove(edge)
		edge.To.edges.remove(edge)

	@staticmethod
	def connect(first_node, second_node, weight, graph):
		if first_node not in graph.nodes or second_node not in graph.nodes:
			raise ValueError()
		edge = Edge(first_node, second_node, weight)
		first_node.edges.append(edge)
		second_node.edges.append(edge)
		return edge