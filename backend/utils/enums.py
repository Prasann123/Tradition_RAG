from enum import Enum

class SearchType(Enum):
    KNN_BETA = "knnBeta"         # MongoDB Atlas vector search (beta)
    KNN_VECTOR = "knnVector"     # MongoDB Atlas vector search (vector)
    APPROXIMATE = "approximate"  # Approximate nearest neighbor search
    MMR = "mmr"                  # Maximal Marginal Relevance reranking
    BM25 = "bm25"                # BM25 keyword-based search (for in-memory, not MongoDB Atlas)
    # Add more as needed, e.g., HYBRID = "hybrid"

class IndexMechanism(Enum):
    FLAT = "FLAT"
    HNSW = "HNSW"
    IVF = "IVF"

