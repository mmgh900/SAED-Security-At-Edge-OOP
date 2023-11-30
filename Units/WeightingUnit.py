from typing import Dict, List
import enchant
import gensim
from nltk.corpus import stopwords


class WeightingUnit:
    def __init__(self, search_interest: str, model: gensim.models.KeyedVectors):
        """
        Initialize the WeightingUnit.

        Initializes instance variables including the search interest keyword and embedding model.

        Args:
            search_interest (str): The search interest keyword.
            model (gensim.models.KeyedVectors): The word embedding model.
        """
        self.english_checker = enchant.Dict("en_US")
        self.stop_words = set(stopwords.words('english'))
        self.search_interest = search_interest
        self.embedding_model = model

    def calculate_blue_zone_weights(self, C_clustered: Dict[str, List[str]]) -> Dict[str, float]:
        """
        Calculate weights for individual words in the blue zone (context).

        Args:
            C_clustered (Dict[str, List[str]]): Dictionary of context words and their occurrences.

        Returns:
            Dict[str, float]: Dictionary containing words and their weights in the blue zone.
        """
        weight_context = {}
        for key, w in C_clustered.items():
            for ww in w:
                if len(ww) == 1 and not self.english_checker.check(ww):
                    weight_context[ww] = 1
                else:
                    weight_context[ww] = (1 / len(w))
        return weight_context

    def calculate_red_zone_weights(self, Q_prime: List[str], N: List[str], Q: str) -> Dict[str, float]:
        """
        Assign weights to different types of keywords in the red zone.

        Args:
            Q_prime (List[str]): Keywords from the query.
            N (List[str]): Named entities.
            Q (str): Search interest keyword.

        Returns:
            Dict[str, float]: Dictionary containing words and their weights in the red zone.
        """
        weighted_keywords = {}

        for i in Q_prime:
            weighted_keywords[i] = 0.0001

        for i in N:
            weighted_keywords[i] = 1

        weighted_keywords[Q] = 1
        return weighted_keywords

    def calculate_yellow_zone_weights(self, purified_synonyms_dict: Dict[str, List[str]]) -> Dict[str, float]:
        """
        Calculate new weights for expanded query words based on similarity to the search interest keyword.

        Args:
            purified_synonyms_dict (Dict[str, List[str]]): Dictionary of purified synonyms.

        Returns:
            Dict[str, float]: Dictionary containing words and their weights in the yellow zone.
        """
        new_weight_expanded_query = {}

        for key, li in purified_synonyms_dict.items():
            for w in li:
                sim_score = self.embedding_model.similarity(w, self.search_interest)
                new_weight_expanded_query[w] = sim_score

        return new_weight_expanded_query

    def weight_keywords(self, C_clustered: Dict[str, List[str]], Q_prime: List[str], N: List[str], Q: str,
                        P: Dict[str, List[str]]) -> Dict[str, float]:
        """
        Combine weights for different types of keywords and context words.

        Args:
            C_clustered (Dict[str, List[str]]): Dictionary of context words and their occurrences.
            Q_prime (List[str]): Keywords from the query.
            N (List[str]): Named entities.
            Q (str): Search interest keyword.
            P (Dict[str, List[str]]): Purified synonyms dictionary.

        Returns:
            Dict[str, float]: Combined dictionary of words and their weights.
        """
        weighted_keywords = self.calculate_red_zone_weights(Q_prime, N, Q)
        weight_context = self.calculate_blue_zone_weights(C_clustered)
        new_weight_expanded_query = self.calculate_yellow_zone_weights(P)

        combined_dict = {**new_weight_expanded_query, **weighted_keywords, **weight_context}
        return combined_dict
