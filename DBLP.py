import re
import pandas as pd
from collections import OrderedDict
from collections import Counter, defaultdict
print(0)
# Load the CSV file (adjust the path to your CSV file)
papers = pd.read_csv('d3_2021_12.csv')
print(1)
# Extract unique fields from fieldsOfStudy
fields_set = set()
for fields in papers['fieldsOfStudy'].dropna():
    cleaned_fields = re.findall(r'[a-z]+', fields.lower().replace(' ', ''))
    fields_set.update(field.strip() for field in cleaned_fields)
print(2)
# Map fields to integers (1-based indexing)
field_to_int = OrderedDict({'Misc': 0})
field_to_int.update({field: i + 1 for i, field in enumerate(sorted(fields_set))})
print(3)
# Count fields per author to determine their primary field
author_field_counts = defaultdict(Counter)
for index, paper in papers.iterrows():
    # Select the first field as the primary field for the paper
    fields = paper['fieldsOfStudy']
    if isinstance(fields, str) and pd.notna(fields):
        fields = fields.split(',')
        primary_field = fields[0].strip()
        primary_field = re.sub(r'[\[\]\'"]', '', primary_field).strip().lower().replace(' ', '')
    else:
        primary_field = 'Misc'
        # Get the list of author IDs
    authors = paper['authors']
    if isinstance(authors, str) and pd.notna(authors):  # Check if 'authors' is a valid string
        author_ids = re.findall('[0-9]+', authors)
    else:
        continue
    # Update field counts for each author
    for author_id in author_ids:
        author_field_counts[author_id.strip()][primary_field] += 1
print(4)
# Create a mapping from string author IDs to integer IDs
unique_author_ids = list(author_field_counts.keys())
sorted_unique_author_ids = sorted(unique_author_ids)
author_id_to_int = {author_id: i + 1 for i, author_id in enumerate(sorted_unique_author_ids)}
# re.findall(r'[a-z]+', fields.lower().replace(' ', ''))
# for index, paper in papers.iterrows():
#
#     print(f"Paper {index}: number of authors = {len(paper['authors'].split(','))}, authors = {paper['authors']}, author ids = {re.findall('[0-9]+',paper['authors'])}")
#     author_ids = set(author_id.strip() for author_id in paper['id'].split(','))
#     sorted_author_ids = sorted(author_ids)
#     # int_ids = [author_id_to_int[author_id] for author_id in sorted_author_ids]
print(5)
# Write the dataset to a file
with open('dataset.txt', 'w') as f:
    # Write vertices
    f.write("# Vertex\n")
    for author_id in sorted(author_field_counts.keys()):  # Sorting is optional for consistency
        int_id = author_id_to_int[author_id]
        field_counts = author_field_counts[author_id]
        primary_field = max(field_counts, key=field_counts.get)
        if primary_field not in field_to_int:
            primary_field = 'Misc'
        label = field_to_int[primary_field]
        f.write(f"v {int_id} {label}\n")

    # Write simplices
    f.write("# Simplex\n")
    for index, paper in papers.iterrows():
        # Get unique, sorted author IDs for the simplex
        author_ids = set(author_id.strip() for author_id in re.findall('[0-9]+',paper['authors']))
        sorted_author_ids = sorted(author_ids)
        # Map to integer IDs
        int_ids = [author_id_to_int[author_id] for author_id in sorted_author_ids]
        # Get the primary field and its label
        fields = paper['fieldsOfStudy'].split(',')
        primary_field = fields[0].strip()
        primary_field = re.sub(r'[\[\]\'"]', '', primary_field).strip().lower().replace(' ', '')
        if primary_field not in field_to_int:
            primary_field = 'Misc'
        label = field_to_int[primary_field]
        # Write simplex with space-separated integer IDs
        simplex_str = " ".join(map(str, int_ids)) + " - " + str(label)
        f.write(f"{simplex_str}\n")
print(6)
with open('field_mappings.txt', 'w') as f:
    for field, number in field_to_int.items():
        f.write(f"{field}: {number}\n")
print("Dataset has been written to 'dataset.txt'.")
# print(papers)
# print(papers.columns)