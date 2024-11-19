# pake image Python
FROM python:3.10-slim

# set working directory di container
WORKDIR /app

# install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# copy semua file ke dalam container
COPY . .

# expose port 8080 untuk Cloud Run
EXPOSE 8080

# jalankan aplikasi
CMD ["python", "main.py"]
