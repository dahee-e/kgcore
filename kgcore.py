import networkx as nx
import time
import os
import argparse

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



if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Peeling Algorithm for Hypergraph (k, g)-core")
    parser.add_argument("file_path", help="Path to the network file")
    parser.add_argument("k", type=int, help="Value of k")
    parser.add_argument("g", type=int, help="Value of g")
    args = parser.parse_args()

    # Load hypergraph
    hypergraph, E = load_hypergraph(args.file_path)

    # Measure the running time
    start_time = time.time()
    k_g_core = find_kg_core(hypergraph, args.k, args.g)
    end_time = time.time()

    # Write results to file
    output_dir = os.path.dirname(args.file_path)
    output_filename = f"{args.k}_{args.g}_core.dat"
    output_path = os.path.join(output_dir, output_filename)

    with open(output_path, 'w') as output_file:
        # Write size of nodes
        output_file.write(str(len(k_g_core)) + "\n")
        # Write running time
        output_file.write(f"{end_time - start_time}\n")
        # Write nodes
        nodes = " ".join(str(node) for node in k_g_core)
        output_file.write(nodes + "\n")

    print(f"Results written to {output_path}")