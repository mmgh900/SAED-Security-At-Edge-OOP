# Importing necessary libraries
import enchant
from nltk.corpus import wordnet, stopwords


# Definition of the QueryExpansionUnit class
class QueryExpansionUnit:
    def __init__(self, model):
        # Initializing instance variables
        self.english_checker = enchant.Dict("en_US")  # Spell checker for English words
        self.stop_words = set(stopwords.words('english'))  # Set of English stopwordss
        self.embedding_model = model

    # Method to tokenize a given query, removing stopwords
    def tokenize_query(self, query):
        return [word for word in query.lower().split(" ") if word not in self.stop_words]

    # Method to get synonyms for a given word using WordNet
    def get_synonyms(self, word):
        synonyms = []
        # Loop through WordNet synsets for the given word
        for syn in wordnet.synsets(word):
            # Loop through lemmas in each synset
            for lemma in syn.lemmas():
                # Add unique synonyms to the list
                if lemma.name() not in synonyms:
                    synonyms.append(lemma.name())
        return synonyms

    # Method to calculate similarity scores between query words and context words using word embeddings
    def calculate_similarity_scores(self, synonyms_dict, context):
        dict_score_context = {}
        avg_score_keeper = []
        # Loop through each query word and its synonyms
        for qw, eqw in synonyms_dict.items():
            sum_score_expanded_query_words = []
            # Loop through each synonym of the query word
            for eachword in eqw:
                l = 0
                # Calculate similarity score between the synonym and each context word
                for conw in context:
                    try:
                        l += self.embedding_model.similarity(eachword, conw)
                    except:
                        l += 0
                sum_score_expanded_query_words.append(l)
            # Calculate average similarity score for each query word
            avg_score_keeper.append(sum(sum_score_expanded_query_words) / len(sum_score_expanded_query_words))
            dict_score_context[qw] = sum_score_expanded_query_words
        return dict_score_context, avg_score_keeper

    # Method to filter synonyms based on similarity scores
    def purify_synonyms_dict(self, dict_score_context, avg_score_keeper, synonyms_dict):
        purified_synonyms_dict = {}
        i = -1
        # Loop through query words and their scores
        for key, score in dict_score_context.items():
            i += 1
            la = []
            # Filter synonyms based on similarity scores and average score
            for s in score:
                if (s >= avg_score_keeper[i]):
                    a = score.index(s)
                    la.append(synonyms_dict[key][a])
            purified_synonyms_dict[key] = la
        return purified_synonyms_dict

    # Method to expand a given query by finding synonyms for each word
    def expand_query(self, query, context):
        # Tokenize the query and remove stopwords
        tokenized_query = self.tokenize_query(query)
        # Dictionary to store synonyms for each word in the query
        synonyms_dict = {}
        # Loop through each word in the tokenized query
        for word in tokenized_query:
            # Check if the word is a valid English word
            if self.english_checker.check(word):
                # Get synonyms for the word using WordNet
                synonyms_dict[word] = self.get_synonyms(word)

        # Calculate similarity scores between query words and context words
        dict_score_context, avg_score_keeper = self.calculate_similarity_scores(synonyms_dict, context)

        # Filter synonyms based on similarity scores
        purified_synonyms_dict = self.purify_synonyms_dict(dict_score_context, avg_score_keeper, synonyms_dict)

        return purified_synonyms_dict
