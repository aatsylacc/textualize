# Gunakan image berbasis TensorFlow
FROM tensorflow/tensorflow:latest-py3

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED True

# Set lingkungan kerja
WORKDIR /app

# Salin file aplikasi dan requirements.txt
COPY . /app
COPY requirements.txt /app/

# Instal dependensi
RUN pip install --no-cache-dir -r requirements.txt

# Inisialisasi dan cache model OCR selama build
RUN python -c "from doctr.models import ocr_predictor; ocr_predictor(det_arch='db_resnet50', reco_arch='crnn_mobilenet_v3_small', pretrained=True, assume_straight_pages=False, detect_orientation=True, disable_crop_orientation=True, disable_page_orientation=True, straighten_pages=True)"

# Jalankan aplikasi menggunakan Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]