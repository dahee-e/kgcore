import dhg.random as dr
import numpy as np

# Define the sizes for the hypergraphs
sizes = [4000, 8000, 12000, 16000, 20000]

# Loop over the sizes
for size in sizes:
    hypergraph = dr.uniform_hypergraph_Gnm(100, 10000, size)

    hypergraph_strings = [','.join(map(str, edge)) for edge in hypergraph.e]

    # Save the hypergraph to a file
    with open(f'hypergraph_{size}.txt', 'w') as f:
        for line in hypergraph.e:
            for x in line :
                if isinstance(x, tuple):
                    s = ','.join(map(str, x))
                    f.write(f'{s}\n')

