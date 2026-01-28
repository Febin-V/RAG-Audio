from flask import Flask, render_template, request, jsonify, redirect, url_for

# ===== IMPORTS FROM OTHER FILES =====
from models.whisper_model import whisper_model
from models.embedding_model import embedding_model
from models.llm_model import ask_huggingface
from db.chroma_db import collection
from services.ingestion_service import process_audio_file
from services.chat_service import process_chat_query

# =======================
# 1. FLASK APP
# =======================
app = Flask(__name__)

# =======================
# 2. ROUTES
# =======================

##@app.route("/", methods=["GET"])
##def index():
 ##   return render_template("upload.html")

@app.route("/", methods=["GET"])
def index():
    return render_template("chatbot.html")


#@app.route("/upload", methods=["POST"])
#d#ef upload_audio():
  #  file = request.files.get("audio_file")
    #if not file:
    #    return "No file uploaded", 400

   # process_audio_file(file)
    #return redirect(url_for("query_ui"))
#
@app.route("/upload", methods=["POST"])
def upload_audio():
    file = request.files.get("audio_file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    process_audio_file(file)

    return jsonify({
        "status": "success",
        "message": "Audio processed successfully"
    })

#@app.route("/query", methods=["GET"])
#def query_ui():
  #  return render_template("query.html")


@app.route("/chat", methods=["POST"])
def chat_with_audio():
    data = request.get_json()
    return jsonify(process_chat_query(data))


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "Flask API is working"})


# =======================
# 3. RUN APP
# =======================
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
