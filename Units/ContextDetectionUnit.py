from typing import List, Tuple
import enchant
from pywsd.lesk import simple_lesk
import yake


class ContextDetectionUnit:
    def __init__(self):
        """
        Initialize the ContextDetectionUnit.

        Initializes the instance variable 'english_checker' for English spell checking.
        """
        self.english_checker = enchant.Dict("en_US")

    def categorize_keywords(self, keywords: List[Tuple[str, float]]) -> Tuple[List[str], List[str]]:
        """
        Categorize keywords into context and named entities based on English spell checking.

        Args:
            keywords (List[Tuple[str, float]]): List of keywords with associated scores.

        Returns:
            Tuple[List[str], List[str]]: Tuple containing two lists - context_keywords and named_keywords.
        """
        context_keywords = []
        named_keywords = []

        for keyword in keywords:
            if self.english_checker.check(keyword[0]):
                context_keywords.append(keyword[0])
            else:
                named_keywords.append(keyword[0])

        return context_keywords, named_keywords

    @staticmethod
    def get_definitions(keywords: List[str], query: str) -> List[str]:
        """
        Get definitions for context keywords using Word Sense Disambiguation.

        Args:
            keywords (List[str]): List of context keywords.
            query (str): The input query.

        Returns:
            List[str]: List of definitions for context keywords.
        """
        return [simple_lesk(query, keyword, pos=None).definition() for keyword in keywords]

    @staticmethod
    def extract_keywords_from_query(query: str) -> List[Tuple[str, float]]:
        """
        Extract keywords from the query using YAKE.

        Args:
            query (str): The input query.

        Returns:
            List[Tuple[str, float]]: List of extracted keywords with associated scores.
        """
        keyword_extractor = yake.KeywordExtractor(lan="en", n=1, windowsSize=2, top=5)
        return keyword_extractor.extract_keywords(query)

    @staticmethod
    def extract_keywords_from_definitions(definitions: List[str]) -> List[List[Tuple[str, float]]]:
        """
        Extract keywords from the definitions of context keywords using YAKE.

        Args:
            definitions (List[str]): List of definitions.

        Returns:
            List[List[Tuple[str, float]]]: List of extracted keywords from definitions with associated scores.
        """
        keyword_extractor = yake.KeywordExtractor(lan="en", n=1, windowsSize=2, top=10)
        return [keyword_extractor.extract_keywords(definition) for definition in definitions]

    def get_context(self, query: str) -> Tuple[List[str], dict, List[str], List[str]]:
        """
        Get context information from a given query.

        Args:
            query (str): The input query.

        Returns:
            Tuple[List[str], dict, List[str], List[str]]: Tuple containing context, query keywords contributions,
            keywords from query, and named entities.
        """
        keywords_from_query = self.extract_keywords_from_query(query)
        context_keywords_from_query, named_keywords = self.categorize_keywords(keywords_from_query)
        definitions = self.get_definitions(context_keywords_from_query, query)
        keywords_from_definitions = self.extract_keywords_from_definitions(definitions)

        query_keywords_contribution = {
            context_keywords_from_query[i]: [keyword[0] for keyword in keywords] for i, keywords in
            enumerate(keywords_from_definitions)
        }

        context = [keyword[0] for keywords in keywords_from_definitions for keyword in keywords]

        return context, query_keywords_contribution, context_keywords_from_query, named_keywords
