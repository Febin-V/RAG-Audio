from pydoc import doc
from models.embedding_model import get_query_embedding
from models.llm_model import ask_huggingface
from db.chroma_db import collection

def process_chat_query(data):
    user_query = data.get("query") if data else None
    if not user_query:
        return {"error": "Query required"}

    # ✅ ADD THIS LINE HERE
    rewritten_query = f"What does '{user_query}' refer to in the audio?"

    # ✅ Use rewritten query for embedding
    query_embedding = [get_query_embedding(rewritten_query)]

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=5
    )
    
    
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context = ""
    for doc, meta in zip(documents, metadatas):
        MAX_WORDS = 40
        short_doc = " ".join(doc.split()[:MAX_WORDS])
        context += f"[{meta['start_time']:.2f}s – {meta['end_time']:.2f}s]\n{short_doc}\n\n"


    prompt = f"""
You are an AI assistant helping a user understand an audio transcript.

Instructions:
- Answer ONLY what is asked
- Use ONE sentence only
- Do NOT add extra details
- Do NOT summarize the transcript
- If the question refers to a number or value, return ONLY that value
- If not found, say: "Not mentioned in the audio"
- Do NOT return full transcript or segments
- Extract ONLY the relevant information
- Do NOT return full transcript or segments
- Extract ONLY the relevant information

Transcript Context:
{context}

User Question:
{user_query}

Final Answer (EXTRACT ONLY, DO NOT REPEAT CONTEXT):
"""


    answer = ask_huggingface(prompt)

    return {
        "answer": answer,
        "references": metadatas
    }
