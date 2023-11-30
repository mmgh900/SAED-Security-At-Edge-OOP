# Initialize the searcher with your directory
from Units.SearchUnit import SearchUnit

searcher = SearchUnit('Dataset/BBC_dataset/BBC')

# Search for a query
results = searcher.search('company')

# Print the results
for filename in results:
    print(f'Query found in: {filename}')
