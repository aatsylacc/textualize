# Gunakan image berbasis TensorFlow
FROM tensorflow/tensorflow:latest-py3

# Set lingkungan kerja
WORKDIR /app

# Salin file aplikasi
COPY . /app

# Instal dependensi
RUN pip install --no-cache-dir doctr[tf] flask requests keras

# Inisialisasi dan cache model OCR selama build
RUN python -c "from doctr.models import ocr_predictor; ocr_predictor(det_arch='db_resnet50', reco_arch='crnn_mobilenet_v3_small', pretrained=True, assume_straight_pages=False, detect_orientation=True, disable_crop_orientation=True, disable_page_orientation=True, straighten_pages=True)"

# Jalankan aplikasi Flask
CMD ["python", "app.py"]