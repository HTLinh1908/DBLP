import pandas as pd
from collections import Counter, defaultdict

# Load the CSV file (adjust the path to your CSV file)
papers = pd.read_csv('d3_2021_12.csv')

# Step 1: Extract unique fields from s2fieldsofstudy
fields_set = set()
for fields in papers['s2fieldsofstudy'].dropna():
    field_list = fields.split(',')
    fields_set.update(field.strip() for field in field_list)

# Step 2: Map fields to integers (1-based indexing)
field_to_int = {field: i + 1 for i, field in enumerate(sorted(fields_set))}

# Step 3: Count fields per author to determine their primary field
author_field_counts = defaultdict(Counter)
for index, paper in papers.iterrows():
    # Select the first field as the primary field for the paper
    fields = paper['s2fieldsofstudy'].split(',')
    primary_field = fields[0].strip()

    # Get the list of author IDs
    author_ids = paper['author_ids'].split(',')

    # Update field counts for each author
    for author_id in author_ids:
        author_field_counts[author_id.strip()][primary_field] += 1

# Step 4 & 5: Write the dataset to a file
with open('dataset.txt', 'w') as f:
    # Write vertices
    f.write("# Vertex\n")
    for author_id in author_field_counts:
        field_counts = author_field_counts[author_id]
        # Get the field with the highest count
        primary_field = max(field_counts, key=field_counts.get)
        label = field_to_int[primary_field]
        f.write(f"v {author_id} {label}\n")

    # Write simplices
    f.write("# Simplex\n")
    for index, paper in papers.iterrows():
        # Get sorted author IDs for consistency
        author_ids = sorted(paper['author_ids'].split(','))
        # Get the primary field and its label
        fields = paper['s2fieldsofstudy'].split(',')
        primary_field = fields[0].strip()
        label = field_to_int[primary_field]
        # Write simplex
        simplex_str = " ".join(author_ids) + " - " + str(label)
        f.write(f"{simplex_str}\n")

with open('field_mappings.txt', 'w') as f:
    for field, number in field_to_int.items():
        f.write(f"{field}: {number}\n")

print("Dataset has been written to 'dataset.txt'.")