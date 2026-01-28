import chromadb

# Folder where ChromaDB stores data
chroma_client = chromadb.PersistentClient(
    path="./chromadb_store"
)

# Create or load collection
collection = chroma_client.get_or_create_collection(
    name="audio_transcripts_bge_1024"
)
