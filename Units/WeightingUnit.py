# Importing necessary libraries
import enchant
import gensim
from nltk.corpus import stopwords


# Definition of the WeightingUnit class
class WeightingUnit:
    def __init__(self, search_interest, model):
        # Initializing instance variables
        self.english_checker = enchant.Dict("en_US")  # Spell checker for English words
        self.stop_words = set(stopwords.words('english'))  # Set of English stopwords
        self.search_interest = search_interest  # Search interest keyword
        self.embedding_model = model

    # Method to calculate weights for individual words in the context
    def calculate_blue_zone_weights(self, C_clustered):
        weight_context = {}
        # Loop through the dictionary of context words and their occurrences
        for key, w in C_clustered.items():
            for ww in w:
                # Assign weight based on word length and English spell checking
                if len(ww) == 1 and not self.english_checker.check(ww):
                    weight_context[ww] = 1
                else:
                    weight_context[ww] = (1 / len(w))
        return weight_context

    # Method to assign weights to different types of keywords
    def calculate_red_zone_weights(self, Q_prime, N, Q):
        weighted_keywords = {}
        # Assign a small weight to context words (C)
        for i in Q_prime:
            weighted_keywords[i] = .0001
        # Assign a higher weight to news-related words (N)
        for i in N:
            weighted_keywords[i] = 1
        # Assign a high weight to the search interest keyword (Q)
        weighted_keywords[Q] = 1
        return weighted_keywords

    # Method to calculate new weights for expanded query words based on similarity to search interest keyword
    def calculate_yellow_zone_weights(self, purified_synonyms_dict):
        new_weight_expanded_query = {}
        # Loop through purified synonyms dictionary
        for key, li in purified_synonyms_dict.items():
            # Loop through synonyms and calculate similarity to search interest keyword
            for w in li:
                sim_score = self.embedding_model.similarity(w, self.search_interest)
                new_weight_expanded_query[w] = sim_score
        return new_weight_expanded_query

    # Method to combine weights for different types of keywords and context words
    def weight_keywords(self, C_clustered, Q_prime, N, Q, P):

        # Calculate weights for different types of keywords
        weighted_keywords = self.calculate_red_zone_weights(Q_prime, N, Q)

        # Calculate weights for context words
        weight_context = self.calculate_blue_zone_weights(C_clustered)

        # Calculate new weights for expanded query words based on similarity to search interest keyword
        new_weight_expanded_query = self.calculate_yellow_zone_weights(P)

        # Combine all weights into a single dictionary
        combined_dict = {**new_weight_expanded_query, **weighted_keywords, **weight_context}
        return combined_dict

