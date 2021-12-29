class Edge:
    def __init__(self, first, second, weight = 1):
        self.start = first
        self.finish = second
        self.weight = weight

    def is_incident(self, node):
        return self.start == node or self.finish == node

    def other_node(self, node):
        if not self.is_incident(node):
            raise ValueError()
        if self.start == node:
            return self.finish
        return self.start
