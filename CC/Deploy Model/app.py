import os
from flask import Flask, request, jsonify
from transformers import T5Tokenizer, TFT5ForConditionalGeneration
import tensorflow as tf

# Direktori tempat model dan tokenizer berada di lokal
LOCAL_MODEL_PATH = 'textualize_model_T5_multinews'  # Ganti dengan path model lokal Anda

# Memastikan folder lokal ada
if not os.path.exists(LOCAL_MODEL_PATH):
    os.makedirs(LOCAL_MODEL_PATH)

# Load tokenizer dan model dari folder lokal

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Endpoint utama
@app.route('/')
def home():
    return "Server berjalan! Gunakan endpoint /summarize untuk merangkum teks."

# Endpoint /summarize
@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        # Mendapatkan input teks dari form dengan key 'text'
        input_text = request.form.get('text')

        if not input_text:
            return jsonify({"status": "error", "message": "Input text kosong. Masukkan teks terlebih dahulu."}), 400
        
        # Pengecekan jumlah kata dalam input
        if len(input_text.split()) < 10:
            return jsonify({"status": "error", "message": "Input text terlalu pendek. Masukkan teks minimal 10 kata."}), 400

        # Preprocessing input
        input_ids = tokenizer(input_text, return_tensors="tf").input_ids  # TensorFlow tensors

        # Prediksi menggunakan model
        outputs = model.generate(input_ids, max_length=200, min_length=30, num_beams=4)
        summary = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return jsonify({"status": "success", "message": summary}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Menjalankan server
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
