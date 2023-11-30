from typing import List, Dict, Tuple
import enchant
from nltk.corpus import wordnet, stopwords

class QueryExpansionUnit:
    def __init__(self, model):
        """
        Initialize the QueryExpansionUnit.

        Initializes instance variables including the word embedding model.

        Args:
            model: The word embedding model.
        """
        self.english_checker = enchant.Dict("en_US")
        self.stop_words = set(stopwords.words('english'))
        self.embedding_model = model

    def tokenize_query(self, query: str) -> List[str]:
        """
        Tokenize a given query, removing stopwords.

        Args:
            query (str): The input query.

        Returns:
            List[str]: List of tokenized words.
        """
        return [word for word in query.lower().split(" ") if word not in self.stop_words]

    def get_synonyms(self, word: str) -> List[str]:
        """
        Get synonyms for a given word using WordNet.

        Args:
            word (str): The input word.

        Returns:
            List[str]: List of synonyms for the given word.
        """
        synonyms = []
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                if lemma.name() not in synonyms:
                    synonyms.append(lemma.name())
        return synonyms

    def calculate_similarity_scores(self, synonyms_dict: Dict[str, List[str]], context: List[str]) -> Tuple[Dict[str, List[float]], List[float]]:
        """
        Calculate similarity scores between query words and context words using word embeddings.

        Args:
            synonyms_dict (Dict[str, List[str]]): Dictionary of query words and their synonyms.
            context (List[str]): List of context words.

        Returns:
            Tuple[Dict[str, List[float]], List[float]]: Tuple containing a dictionary of similarity scores for each
            query word and a list of average scores.
        """
        dict_score_context = {}
        avg_score_keeper = []

        for qw, eqw in synonyms_dict.items():
            sum_score_expanded_query_words = []

            for eachword in eqw:
                l = 0
                for conw in context:
                    try:
                        l += self.embedding_model.similarity(eachword, conw)
                    except:
                        l += 0
                sum_score_expanded_query_words.append(l)

            avg_score_keeper.append(sum(sum_score_expanded_query_words) / len(sum_score_expanded_query_words))
            dict_score_context[qw] = sum_score_expanded_query_words

        return dict_score_context, avg_score_keeper

    def purify_synonyms_dict(self, dict_score_context: Dict[str, List[float]], avg_score_keeper: List[float], synonyms_dict: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """
        Filter synonyms based on similarity scores.

        Args:
            dict_score_context (Dict[str, List[float]]): Dictionary of similarity scores for each query word.
            avg_score_keeper (List[float]): List of average scores.
            synonyms_dict (Dict[str, List[str]]): Dictionary of query words and their synonyms.

        Returns:
            Dict[str, List[str]]: Dictionary containing purified synonyms for each query word.
        """
        purified_synonyms_dict = {}
        i = -1

        for key, score in dict_score_context.items():
            i += 1
            la = []

            for s in score:
                if s >= avg_score_keeper[i]:
                    a = score.index(s)
                    la.append(synonyms_dict[key][a])

            purified_synonyms_dict[key] = la

        return purified_synonyms_dict

    def expand_query(self, query: str, context: List[str]) -> Dict[str, List[str]]:
        """
        Expand a given query by finding synonyms for each word.

        Args:
            query (str): The input query.
            context (List[str]): List of context words.

        Returns:
            Dict[str, List[str]]: Dictionary containing synonyms for each word in the query.
        """
        tokenized_query = self.tokenize_query(query)
        synonyms_dict = {}

        for word in tokenized_query:
            if self.english_checker.check(word):
                synonyms_dict[word] = self.get_synonyms(word)

        dict_score_context, avg_score_keeper = self.calculate_similarity_scores(synonyms_dict, context)
        purified_synonyms_dict = self.purify_synonyms_dict(dict_score_context, avg_score_keeper, synonyms_dict)

        return purified_synonyms_dict
