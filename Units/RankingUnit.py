from typing import List, Dict, Tuple
import enchant
from nltk.corpus import wordnet, stopwords
import configparser
import math
import operator


class RankingUnit:
    def __init__(self, dataset_url):
        self.dataset_url = dataset_url

    def calculate_idf(self, word, document_list):
        """
        Calculate the Inverse Document Frequency (IDF) for a given word in a list of documents.

        Parameters:
        - word (str): The word to calculate IDF for.
        - document_list (list): List of document names.

        Returns:
        - float: The IDF value.
        """
        count = 0
        for document in document_list:
            with open(f"{self.dataset_url}/{document}", "r") as file:
                content = file.read().lower()
                if word in content:
                    count += 1

        return math.log2(len(document_list) / (count + 1))

    def rank_documents(self, document_names, query_weights):
        # Calculate Kendra score for each document
        kendra_scores = {}
        for document_name in document_names:
            with open(f"{self.dataset_url}/{document_name}", "r") as document_file:
                content = document_file.read().lower()
                total_words = len(content.split())
                score = 0
                for term in query_weights.keys():
                    if term in content:
                        score += ((content.count(term) / total_words) * self.calculate_idf(term, document_names) *
                                  query_weights[term])

                kendra_scores[document_name] = score

        # Sort the documents by Kendra score in descending order
        sorted_scores = sorted(kendra_scores.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_scores
