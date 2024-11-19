from flask import Flask, request, jsonify
from google.cloud import storage
import numpy as np
import cv2
from doctr.models import ocr
from PIL import Image
import io

app = Flask(__name__)

# inisialisasi Google Cloud Storage client
storage_client = storage.Client()
bucket_name = "nama-bucket-anda"  # ganti dengan nama bucket kamu
bucket = storage_client.get_bucket(bucket_name)

# inisialisasi OCR model dari Doctr
ocr_model = ocr.deserialize("craft_mlt_keras")  # kamu bisa sesuaikan dengan model yang kamu pilih

@app.route("/upload", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # upload ke Cloud Storage
    blob = bucket.blob(file.filename)
    blob.upload_from_file(file)

    image_uri = f"gs://{bucket_name}/{file.filename}"

    # eksekusi OCR di gambar
    ocr_text = detect_text_from_image(image_uri)

    # simpan hasil OCR ke Firestore atau return ke frontend
    return jsonify({"ocr_text": ocr_text})

def detect_text_from_image(image_uri):
    # ambil gambar dari Cloud Storage
    blob = bucket.blob(image_uri.split("gs://")[1])
    image_bytes = blob.download_as_bytes()

    # ubah bytes ke format image dengan PIL dan konversi ke format numpy array
    image = Image.open(io.BytesIO(image_bytes))
    image_np = np.array(image)

    # lakukan OCR dengan Doctr
    result = ocr_model.predict([image_np])

    # ambil teks dari hasil OCR
    ocr_result = result[0].pages[0].extract_text()

    return ocr_result

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
