from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")


def generate_embedding(text):
    return model.encode(text, normalize_embeddings=True)
