import os
import uuid


from models.whisper_model import whisper_model
from models.embedding_model import get_embedding
from db.chroma_db import collection

UPLOAD_FOLDER = "uploads/audio"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

TRANSCRIPT_FILE = r"C:\Users\febin\Desktop\ospyn_interns\segment_text.txt"

def process_audio_file(file):
    audio_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(audio_path)

    segments, _ = whisper_model.transcribe(audio_path, language="en")
    segments = list(segments)

    chunks = []
    current_text = ""
    start_time = None
    segment_id = 1

    for segment in segments:
        if start_time is None:
            start_time = segment.start

        text = segment.text.strip()

# force split on important interview questions
        question_triggers = [
         "salary",
            "how much",
         "benefits",
            "working hours",
         "join",
            "full-time",
         "part-time"
        ]

        if any(q in text.lower() for q in question_triggers) and current_text:
           chunks.append({
               "segment_id": segment_id,
               "text": current_text.strip(),
               "start_time": start_time,
               "end_time": segment.start
         })
           segment_id += 1
           current_text = ""
           start_time = segment.start

        current_text += " " + text


        if len(current_text.split()) >= 25:
            chunks.append({
                "segment_id": segment_id,
                "text": current_text.strip(),
                "start_time": start_time,
                "end_time": segment.end
            })
            segment_id += 1
            current_text = ""
            start_time = None

    if current_text.strip():
        chunks.append({
            "segment_id": segment_id,
            "text": current_text.strip(),
            "start_time": start_time,
            "end_time": segments[-1].end
        })

    documents = [c["text"] for c in chunks]

    metadatas = [{
        "start_time": c["start_time"],
        "end_time": c["end_time"],
        "segment_id": c["segment_id"]
    } for c in chunks]



    
    # ✅ CORRECT embedding generation
    def enrich_text(text):
        return f"Interview transcript information: {text}"

    embeddings = [get_embedding(enrich_text(doc)) for doc in documents]

    collection.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=[str(uuid.uuid4()) for _ in chunks]
    )

    # ===============================
    # SAVE TRANSCRIPT TO TEXT FILE
    # ===============================
    with open(TRANSCRIPT_FILE, "a", encoding="utf-8") as f:
        f.write("\n==============================\n")
        f.write(f"Audio File: {file.filename}\n")
        f.write("==============================\n\n")

        for c in chunks:
            line = (
                f"[Segment {c['segment_id']} | "
                f"{c['start_time']:.2f}s - {c['end_time']:.2f}s]\n"
                f"{c['text']}\n\n"
            )
            f.write(line)
