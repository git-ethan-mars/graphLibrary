from collections import deque

from Node import Node
from Edge import Edge


class Graph:
    def __init__(self, nodes_count):
        self.nodes = [Node(i) for i in range(0, nodes_count)]

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

    def dfs(self, node_index):
        return self._dfs(self.nodes[node_index])

    @staticmethod
    def _dfs(start_node):
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

    def bfs(self, node_index):
        visited = set()
        planned = deque([self.nodes[node_index]])
        visited.add(self.nodes[node_index])
        trace = dict()
        trace[self.nodes[node_index].node_number] = 0
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
            if dist[edge.start.node_number] != float("Inf") and dist[edge.start.node_number] + edge.weight < dist[
                edge.finish.node_number]:
                raise ValueError("Graph contains negative weight cycle")
        return dist

    def dijkstra(self, start_node: int):
        not_visited = self.nodes.copy()
        track = dict()
        track[self.nodes[start_node]] = 0
        while True:
            to_open = None
            best_price = float('inf')
            for e in not_visited:
                if e in track and track[e] < best_price:
                    best_price = track[e]
                    to_open = e
            if to_open is None:
                result = dict()
                for x in track:
                    result[x.node_number] = track[x]
                return result

            for e in [x for x in to_open.incident_edges() if x.start == to_open]:
                current_price = track[to_open] + e.weight
                next_node = e.other_node(to_open)
                if (not next_node in track) or track[next_node] > current_price:
                    track[next_node] = current_price

            not_visited.remove(to_open)
