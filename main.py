
import gensim

from Units.ContextDetectionUnit import ContextDetectionUnit
from Units.QueryExpansionUnit import QueryExpansionUnit
from Units.RankingUnit import RankingUnit
from Units.SearchUnit import SearchUnit
from Units.WeightingUnit import WeightingUnit


Q = 'European Commission'

cdu = ContextDetectionUnit()
C, C_clustered, Q_prime, N = cdu.get_context(Q)

# Load the pre-trained word embeddings model
model = gensim.models.KeyedVectors.load_word2vec_format('./Dataset/GoogleNews-vectors-negative300.bin', binary=True)

qeu = QueryExpansionUnit(model)
P = qeu.expand_query(Q, C)

wu = WeightingUnit('politics', model)
combined_dict = wu.weight_keywords(C_clustered, Q_prime, N, Q, P)

dataset_url = 'Dataset/BBC_dataset/BBC'
searcher = SearchUnit(dataset_url)

# Search for a query
documents_list = searcher.search_multiple(P)

ranker = RankingUnit(dataset_url)
documents_list_ranked = ranker.rank_documents(documents_list, combined_dict)
print(documents_list_ranked)

