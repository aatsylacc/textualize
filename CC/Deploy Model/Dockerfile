# Menggunakan image Python sebagai base image
FROM python:3.12-slim

# Menetapkan working directory di dalam container
WORKDIR /app

# Menyalin semua file dari direktori lokal ke dalam container
COPY . /app

# Menginstal dependencies yang ada di requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Menyediakan port untuk aplikasi Flask (default: 5000)
EXPOSE 5000

# Menjalankan aplikasi Flask
CMD ["python", "app.py"]