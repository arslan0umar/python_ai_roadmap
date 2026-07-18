from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class SemanticSearch:
    def __init__(self, notes):
        self.notes = notes
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.embedding = self.model.encode(notes)

    def search(self, query, top_n=3):
        query_embedding = self.model.encode(query)
        score = cosine_similarity([query_embedding], self.embedding)
        matrix_scores = np.array(score)
        top_n_indices = matrix_scores[0].argsort()[::-1][:top_n]
        return top_n_indices, score[0]
    
    def display_results(self, query):
        top_n_indices, scores = self.search(query)
        print(f"\nQuery: \"{query}\"\n")
        for i in top_n_indices:
            print(f"\t[{scores[i]:.2f}] {self.notes[i]}")

notes = [
    "Deadlocks occur when processes wait for each other indefinitely",
    "The banker's algorithm is used for deadlock avoidance",
    "Semaphores are used for process synchronization",
    "A mutex ensures mutual exclusion in critical sections",
    "Page replacement algorithms include LRU, FIFO, and Optimal",
    "Virtual memory allows processes to use more memory than physically available",
    "The dining philosophers problem illustrates synchronization issues",
    "Round robin scheduling gives each process an equal time quantum",
    "RAG stands for Retrieval Augmented Generation in AI systems",
    "Embeddings represent text as dense vectors in high dimensional space",
    "Cosine similarity measures the angle between two vectors",
    "LangChain is a framework for building LLM applications",
    "Cricket is a bat and ball game played between two teams of eleven players",
    "IPL is the Indian Premier League, a professional cricket league",
    "Virat Kohli is one of the best batsmen in modern cricket"
]

searcher = SemanticSearch(notes)
searcher.display_results("how to prevent deadlocks")
searcher.display_results("cricket tournament in India")
searcher.display_results("how do LLMs use text representations")