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

    def find_common_node(self, routes: tuple[list[Node], list[Node]] = None) -> tuple[list[Node], list[Node]] | None:
        route_sasha, route_mika = routes if routes is not None else ([self.nodes[0]], [self.nodes[1]])
        panel_sasha: Node = route_sasha[-1]
        panel_mika: Node = route_mika[-1]
        if panel_sasha == panel_mika:
            return routes
        if not panel_sasha.next_nodes or not panel_mika.next_nodes or len(route_sasha) != 1 \
                and (panel_sasha == self.nodes[0] or panel_mika == [self.nodes[1]]):
            return
        for next_sasha in filter(lambda x: x not in route_sasha, panel_sasha.next_nodes):
            possible_route_sasha: list[Node] = route_sasha.copy()
            possible_route_sasha.append(next_sasha)
            for next_mika in filter(lambda x: x not in route_mika, panel_mika.next_nodes):
                possible_route_mika: list[Node] = route_mika.copy()
                possible_route_mika.append(next_mika)
                found_routes = self.find_common_node((possible_route_sasha, possible_route_mika))
                if found_routes is not None:
                    return found_routes

    def find_reachable_nodes(self, starting_node: Node, stack=None, found_paths=None) -> dict[Node, list[list[Node]]]:
        if found_paths is None:
            found_paths = {node: [] for node in self.nodes}
        if stack is None:
            stack = []
        stack.append(starting_node)
        found_paths[starting_node].append(stack)
        if not starting_node.next_nodes:
            return found_paths
        for node in starting_node.next_nodes:
            if node not in stack:
                found_paths = self.find_reachable_nodes(node, stack.copy(), found_paths)
        return found_paths


if __name__ == '__main__':
    edges = []
    with open(argv[1], "r") as file:
        node_amount, edge_amount = map(int, file.readline().strip().split(" "))
        for _ in range(edge_amount):
            edges.append(file.readline().strip().split(" "))
    nodes_ = [Node(uid + 1) for uid in range(node_amount)]
    for edge in edges:
        first, second = map(int, edge)
        nodes_[first - 1].add_edge(nodes_[second - 1])
    graph = Graph(nodes_)
    print(graph.find_common_node())
