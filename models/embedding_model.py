from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer("BAAI/bge-large-en-v1.5")

def get_embedding(text: str):
    return embedding_model.encode(
        "passage: " + text,
        normalize_embeddings=True
    ).tolist()

def get_query_embedding(text: str):
    return embedding_model.encode(
        "query: " + text,
        normalize_embeddings=True
    ).tolist()


#"all-MiniLM-L6-v2"
#first i used model