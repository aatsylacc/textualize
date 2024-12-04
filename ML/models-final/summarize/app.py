import os
from flask import Flask, request, jsonify
from transformers import pipeline, logging
from google.cloud import storage

# Menghilangkan logging TensorFlow yang tidak penting
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
logging.set_verbosity_error()

# Konfigurasi Google Cloud Storage
BUCKET_NAME = "textualize-model"
MODEL_FOLDER = "textualize_model_T5_multinews"  
LOCAL_MODEL_PATH = "textualize_model_T5_multinews"  

def download_model_from_gcs(bucket_name, model_folder, local_model_path):
    """Mengunduh model dari Google Cloud Storage ke folder lokal."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=model_folder)  # Semua file di dalam folder

    for blob in blobs:
        # Tentukan path file lokal
        relative_path = blob.name[len(model_folder) + 1:]  # Hilangkan prefix folder
        local_path = os.path.join(local_model_path, relative_path)
        
        # Buat direktori jika belum ada
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        # Download file
        blob.download_to_filename(local_path)
        print(f"Downloaded {blob.name} to {local_path}")

# Unduh model dari GCS jika belum ada di lokal
if not os.path.exists(LOCAL_MODEL_PATH) or not os.listdir(LOCAL_MODEL_PATH):
    print("Downloading model from GCS...")
    download_model_from_gcs(BUCKET_NAME, MODEL_FOLDER, LOCAL_MODEL_PATH)

# Load pipeline summarization
print("Loading summarization model...")
summarizer = pipeline("summarization", model=LOCAL_MODEL_PATH, tokenizer=LOCAL_MODEL_PATH, framework="tf")
print("Model loaded successfully!")

# Flask app
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    """Endpoint default untuk memastikan server aktif"""
    return jsonify({
        "message": "Server berjalan! Gunakan endpoint /summarize untuk merangkum teks."
    })

@app.route("/summarize", methods=["POST"])
def summarize_text():
    """Endpoint untuk merangkum teks"""
    try:
        data = request.get_json()
        text = data.get("text", "")

        # Validasi input
        if not text or len(text.split()) < 10:
            return jsonify({"error": "Input text terlalu pendek. Masukkan teks minimal 10 kata."}), 400

        # Jalankan summarization
        summary = summarizer(text)
        return jsonify({"summary": summary[0]["summary_text"]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Jalankan server Flask
if __name__ == "__main__":
    app.run(debug=True, port=5000)
