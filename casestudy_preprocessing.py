def preprocess_data(aacy_file, output_file):
    # Process aacy file
    result = {}
    with open(aacy_file, 'r') as f:
        for line in f:
            author_ids = line.strip().split()[:-2]
            conference_id = line.strip().split()[-2]
            year = line.strip().split()[-1]

            if (conference_id, year) not in result:
                result[(conference_id, year)] = set()

            for author_id in author_ids:
                result[(conference_id, year)].add(author_id)

    # Write the result to output file
    with open(output_file, 'w') as f:
        for author_set in result.values():
            authors = ', '.join(sorted(author_set))
            f.write(f"{authors}\n")


# Example usage
preprocess_data('D:/Data/kg_core/case/aacy.txt', 'D:/Data/kg_core/case/network.hyp')
