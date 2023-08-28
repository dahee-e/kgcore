import networkx as nx
import time
import os

def load_hypergraph(file_path):
    hypergraph = nx.Graph()  # Create an empty hypergraph
    E = list()

    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            # Use set to ignore duplicate values in each line and strip whitespace from node names
            nodes = {node.strip() for node in line.strip().split(',')}
            nodes = {int(x) for x in  nodes}
            hyperedge = set(nodes)  # Use frozenset to represent the hyperedge
            E.append(hyperedge)
            for node in nodes:
                if node not in hypergraph.nodes():
                    hypergraph.add_node(node, hyperedges=list())  # Add a node for each node
                hypergraph.nodes[node]['hyperedges'].append(hyperedge)  # Add the hyperedge to the node's hyperedge set

    return hypergraph, E



def degree(hypergraph, node):
    neighbors = set()
    for hyperedge in hypergraph.nodes[node]['hyperedges']:
        neighbors.update(hyperedge - {node})  # Collect all nodes in the hyperedge except the current node
    return len(neighbors)



def get_induced_subhypergraph(hypergraph, node_set):
    subhypergraph = nx.Graph()
    for node in node_set:
        if node in hypergraph.nodes:
            subhypergraph.add_node(node, hyperedges=[])
            for hyperedge in hypergraph.nodes[node]['hyperedges']:
                p = node_set & set(hyperedge)
                if len(p) >= 2:
                    subhypergraph.add_edges_from([(u, v) for u in p for v in p if u != v])
                    subhypergraph.nodes[node]['hyperedges'].append(p)
    return subhypergraph



def load_set_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        integers = content.split()
        string_set = set(map(str, integers))
    return string_set


def has_at_least_k_neighbors(node, k, hypergraph):
    return degree(hypergraph, node) >= k


def neighbor_pairs_in_g_hyperedges(node, g, hypergraph, E):
    # For each neighbor, count the number of hyperedges containing both
    neighbors = set()
    for hyperedge in hypergraph.nodes[node]['hyperedges']:
        neighbors.update(hyperedge - {node})

    for neighbor1 in neighbors:
        for neighbor2 in neighbors:
            if neighbor1 != neighbor2:
                common_hyperedges = sum(1 for hyperedge in E if neighbor1 in hyperedge and neighbor2 in hyperedge)
                if common_hyperedges < g:
                    return False
    return True


def construct_neighbor_occurrence_map(hypergraph, g):
    neighbor_occurrence_map = {}

    for node in hypergraph.nodes:
        neighbor_counts = {}

        # For each hyperedge containing the current node
        for hyperedge in hypergraph.nodes[node]['hyperedges']:
            # Increment the count for each neighbor in the hyperedge
            for neighbor in hyperedge:
                if neighbor != node:
                    neighbor_counts[neighbor] = neighbor_counts.get(neighbor, 0) + 1

        # Filter neighbors that appear in at least g common hyperedges
        filtered_neighbors = {neighbor: count for neighbor, count in neighbor_counts.items() if count >= g}

        # Add the filtered map to the overall map
        neighbor_occurrence_map[node] = filtered_neighbors

    return neighbor_occurrence_map


def find_kg_core(hypergraph, k, g):

    # Step 2: Initialization
    H = set(hypergraph.nodes())
    neighbor_occurrence_map = construct_neighbor_occurrence_map(hypergraph, g)

    changed = True
    while changed:
        changed = False

        marked_nodes = set()

        for v in H:
            if len(neighbor_occurrence_map.get(v)) < k:
                marked_nodes.add(v)
                changed = True

        for w in marked_nodes:
            H.remove(w)
            neighbour_list = neighbor_occurrence_map.get(w)
            for nid in neighbour_list:
                neighbor_occurrence_map[nid].pop(w)
            hypergraph.remove_node(w)

    return hypergraph.subgraph(H)




# Example usage:
file_path = 'D:/Data/kg_core/paper.hyp'
hypergraph, E = load_hypergraph(file_path)
k = 2  # Example value for k
g = 1  # Example value for g
#for node, neighbors in neighbor_occurrence_map.items():
#    print(f"{node}: {neighbors}")
# Measure the running time
start_time = time.time()
k_g_core = find_kg_core(hypergraph, k, g)
end_time = time.time()
print(k_g_core)
nodes = " ".join(str(node) for node in k_g_core)
print(nodes)

#file_path = 'D:/Data/kg_core/case/network.hyp'
#node_set = load_set_from_file('D:/Data/kg_core/case/20_100_core.dat')
#print(node_set)
#subhypergraph = get_induced_subhypergraph(hypergraph, node_set)

# Print the nodes and hyperedges in the subhypergraph
#print("Nodes:", subhypergraph.nodes)
#print("Hyperedges:", [subhypergraph.nodes[node]['hyperedges'] for node in subhypergraph.nodes])

#sum = 0
#for node in subhypergraph.nodes :
#    print(len(subhypergraph.nodes[node]['hyperedges']))



#num_hyperedges = subhypergraph.number_of_edges()
#print("Number of Hyperedges:", num_hyperedges)