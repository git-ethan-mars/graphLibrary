from collections import deque

from Node import Node
from Edge import Edge


class Graph:
    def __init__(self, nodes_count):
        self.nodes = [Node(i) for i in range(0, nodes_count)]

    def length(self):
        return len(self.nodes)

    def get_node(self, index):
        return self.nodes[index]

    def connect(self, index1, index2, weight=1):
        return Node.connect(self.nodes[index1], self.nodes[index2], weight, self)

    @staticmethod
    def delete(edge):
        Node.disconnect(edge)

    def has_edge(self, index1, index2, weight=1):
        return {index1, index2} in [{edge.start.node_number, edge.finish.node_number} for edge in
                                    [edge for edge in self.edges if edge.weight == weight]]

    @property
    def edges(self) -> Edge:
        l = []
        for elem in ([node.incident_edges() for node in self.nodes]):
            for i in elem:
                l.append(i)
        return set(l)

    @staticmethod
    def make_graph(incident_nodes):
        graph = Graph(max(incident_nodes) + 1)
        for i in range(0, len(incident_nodes) - 1, 2):
            graph.connect(incident_nodes[i], incident_nodes[i + 1])
        return graph

    @staticmethod
    def make_weighted_graph(incident_nodes):
        temp = []
        for i in range(len(incident_nodes)):
            if i % 3 == 2:
                temp.append(incident_nodes[i])
        incident_nodes = temp
        graph = Graph(max(temp) + 1)
        for i in range(0, len(incident_nodes) - 1, 3):
            graph.connect(incident_nodes[i], incident_nodes[i + 1], incident_nodes[i + 2])
        return graph

    def _dfs(self,start_node):
        visited = set()
        planned = [start_node]
        visited.add(start_node)
        trace = dict()
        trace[start_node.node_number] = 0
        while len(planned) != 0:
            current = planned.pop()
            for edge in current.incident_edges():
                incident_node = edge.other_node(current)
                if incident_node not in visited:
                    trace[incident_node.node_number] = trace[current.node_number] + edge.weight
                    planned.append(incident_node)
                    visited.add(incident_node)
        return trace

    def dfs(self, node_index):
        return self._dfs(self.nodes[node_index])

    def bfs(self, node_index):
        return self._dfs(self.nodes[node_index])

    def _bfs(self, start_node):
        visited = set()
        planned = deque(start_node)
        visited.add(start_node)
        trace = dict()
        trace[start_node.node_number] = 0
        while len(planned) != 0:
            current = planned.popleft()
            for edge in current.incident_edges():
                incident_node = edge.other_node(current)
                if incident_node not in visited:
                    trace[incident_node.node_number] = trace[current.node_number] + edge.weight
                    planned.append(incident_node)
                    visited.add(incident_node)
        return trace

    def bellman_ford(self, start_node: int):
        dist = dict()
        for node in self.nodes:
            dist[node.node_number] = float("Inf")
        dist[start_node] = 0
        for i in range(len(self.nodes) - 1):
            for edge in self.edges:
                if dist[edge.start.node_number] != float("Inf") and dist[edge.start.node_number] + edge.weight < dist[
                    edge.finish.node_number]:
                    dist[edge.finish.node_number] = dist[edge.start.node_number] + edge.weight
        for edge in self.edges:
            if dist[edge.start.node_number] != float("Inf") and dist[edge.start.node_number] + edge.weight < dist[edge.finish.node_number]:
                raise ValueError("Graph contains negative weight cycle")
        return dist

class OldGraph:
    def __init__(self):
        self._edges = dict()
        self._node = set()

    def add_edge(self, start_node, end_node, weight=0):
        self._node.add(start_node)
        self._node.add(end_node)
        if not start_node in self._edges.keys():
            self._edges[start_node] = set()
        if not end_node in self._edges.keys():
            self._edges[end_node] = set()
        self._edges[start_node].add((end_node, weight))

    def get_edges(self):
        return self._edges
