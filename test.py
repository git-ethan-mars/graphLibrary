import time
import unittest
from Graph import Graph


class TestGraphMethods(unittest.TestCase):

    def test_connect(self):
        graph = Graph(6)
        incident = [[3, 4], [3, 5], [1, 2, 1]]
        for i in incident:
            graph.connect(*i)
        for edge in graph.edges:
            print(edge.start.node_number, edge.finish.node_number)
        for i in incident:
            assert graph.has_edge(*i)


class TestAlgorithms(unittest.TestCase):
    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print(f"{self.id()}: {t}")

    def test_bellman_ford_simple_graph(self):
        graph = Graph(5)
        graph.connect(1, 2, 2)
        graph.connect(1, 3, 1)
        graph.connect(3, 2, -1)
        graph.connect(2, 4, 3)
        graph.connect(3, 4, 2)
        result = graph.bellman_ford(1)
        self.assertDictEqual(result, {0: float('inf'), 1: 0, 2: 0, 3: 1, 4: 3})

    def test_bellman_ford_with_negative_weight_cycle(self):
        graph = Graph(3)
        graph.connect(1, 2, -1)
        graph.connect(2, 1, -1)
        with self.assertRaises(ValueError):
            graph.bellman_ford(1)
            graph.bellman_ford(2)

    def test_bellman_ford_long_chain(self):
        graph = Graph(10 ** 3)
        for i in range(1, 10 ** 3 - 1):
            graph.connect(i, i + 1, i)
        result = graph.bellman_ford(1)
        expected_value = {0: float('inf')}
        k = 0
        for i in range(1, 10 ** 3):
            expected_value[i] = k
            k += i
        self.assertDictEqual(result, expected_value)

    def test_bfs(self):
        incident = [[0, 1], [0, 2], [1, 2], [1, 3], [2, 4], [3, 4]]
        graph = Graph(5)
        for i in incident:
            graph.connect(*i)
        self.assertDictEqual(graph.dfs(1),{1: 0, 0: 1, 2: 1, 3: 1, 4: 2})

    def test_dfs(self):
        incident = [[0,1], [0,2], [1,2], [1,3], [2,4], [3,4]]
        graph = Graph(5)
        for i in incident:
            graph.connect(*i)
        self.assertDictEqual(graph.dfs(1),{1: 0, 0: 1, 2: 1, 3: 1, 4: 2})

if __name__ == '__main__':
    unittest.main()
