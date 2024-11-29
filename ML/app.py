import os
import requests
import logging
from flask import Flask, request, jsonify
from keras.models import load_model
from doctr.models import ocr_predictor
from google.cloud import storage
import numpy as np

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ganti URL untuk download summarization model ke GCS bucket
MODEL_URL = "https://storage.googleapis.com/textualize-model/tf_model.h5"
MODEL_PATH = "tf_model.h5"

# download model summarization jika belum ada
if not os.path.exists(MODEL_PATH):
    try:
        logger.info("Downloading summarization model from GCS...")
        response = requests.get(MODEL_URL, timeout=30)
        response.raise_for_status()  # cek kalau ada error HTTP
        with open(MODEL_PATH, "wb") as f:
            f.write(response.content)
        logger.info("Summarization model downloaded from GCS.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error downloading summarization model from GCS: {e}")
        exit(1)  # stop aplikasi kalau model gagal didownload

# load summarization model
summarization_model = load_model(MODEL_PATH)


# inisialisasi OCR model
ocr_model = ocr_predictor(
    det_arch='db_resnet50', reco_arch='crnn_mobilenet_v3_small', 
    pretrained=True, assume_straight_pages=False, detect_orientation=True, 
    disable_crop_orientation=True, disable_page_orientation=True, 
    straighten_pages=True
)

app = Flask(__name__)

@app.route('/ocr', methods=['POST'])
def ocr():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        file = request.files['image']
        image = file.read()
        result = ocr_model([image])
        return jsonify({"text": result.export()})
    except Exception as e:
        logger.error(f"Error in OCR: {e}")
        return jsonify({"error": "OCR processing failed"}), 500

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.json
        if 'text' not in data:
            return jsonify({"error": "No text provided"}), 400

        input_text = data['text']
        # pastikan input_text berbentuk array numpy (atau format sesuai model)
        prediction = summarization_model.predict(np.array([input_text]))
        return jsonify({"summary": prediction})
    except Exception as e:
        logger.error(f"Error in summarization: {e}")
        return jsonify({"error": "Summarization processing failed"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
