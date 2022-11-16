from sys import argv


class Node:
    uid: int
    next_nodes: list

    def __repr__(self) -> str:
        return "Node({})[{}]".format(self.uid, len(self.next_nodes))

    def __str__(self) -> str:
        return "Node({}) -> {}".format(self.uid, [x.uid for x in self.next_nodes])

    def __init__(self, uid: int) -> None:
        self.uid = uid
        self.next_nodes = []

    def add_edge(self, other) -> None:
        assert type(other) == Node
        self.next_nodes.append(other)


class Graph:
    nodes: list[Node]

    def __init__(self, nodes: list[Node]) -> None:
        self.nodes = nodes

    def __str__(self) -> str:
        buffer = ""
        for node in self.nodes:
            buffer += str(node) + "\n"
        return buffer


if __name__ == '__main__':
    edges = []
    with open(argv[1], "r") as file:
        node_amount, edge_amount = map(int, file.readline().strip().split(" "))
        for _ in range(edge_amount):
            edges.append(file.readline().strip().split(" "))
    nodes_ = [Node(uid+1) for uid in range(node_amount)]
    for edge in edges:
        first, second = map(int, edge)
        nodes_[first-1].add_edge(nodes_[second-1])
    graph = Graph(nodes_)
    print(graph)

