import os
from flask import Flask, request, jsonify

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf
from transformers import pipeline, logging

# Menghilangkan logging TensorFlow yang tidak penting
logging.set_verbosity_error()
tf.get_logger().setLevel('ERROR')

# Path model dan tokenizer. Sesuaikan path dengan lokasi folder model
model_path = "textualize_model_T5_multinews"
tokenizer_path = "textualize_model_T5_multinews"

# Load pipeline summarization
summarizer = pipeline("summarization", model=model_path, tokenizer=tokenizer_path, framework="tf")

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
