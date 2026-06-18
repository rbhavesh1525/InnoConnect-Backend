from sklearn.metrics.pairwise import cosine_similarity


def find_similar(query_embedding, embeddings, top_k=5):
    scores = cosine_similarity([query_embedding], embeddings)[0]
    top_idx = scores.argsort()[::-1][:top_k]

    return top_idx, scores
