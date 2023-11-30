import os
import re

class SearchUnit:
    def __init__(self, directory):
        self.directory = directory
        self.documents = self.load_documents()

    def load_documents(self):
        documents = []
        for filename in os.listdir(self.directory):
            if filename.endswith('.txt'):
                with open(os.path.join(self.directory, filename), 'r') as f:
                    documents.append((filename, f.read()))
        return documents

    def search(self, query):
        results = []
        for filename, doc in self.documents:
            if re.search(query, doc):
                results.append(filename)
        return results

    def search_multiple(self, queries):
        results = set()
        for query in queries:
            results.update(self.search(query))
        return list(results)
