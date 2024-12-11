# README

## **Proyek: Textualize**

### **Deskripsi Singkat**
Textualize adalah sebuah proyek berbasis cloud yang bertujuan untuk menyediakan layanan API yang dapat:
- Merangkum teks panjang menjadi teks yang lebih singkat.
- Mengunggah gambar beserta metadata (judul dan deskripsi) ke penyimpanan cloud.
- Mengelola data pengguna dan autentikasi menggunakan database.

Proyek ini memanfaatkan Python Flask untuk model Machine Learning, Express.js untuk backend utama, serta berbagai layanan Google Cloud Platform (GCP) untuk deployment.

---

### **Fitur Utama**
1. **Endpoint Summarize (Flask):**
   - Merangkum teks lebih dari 10 kata menjadi teks yang lebih singkat.
   - Mengembalikan pesan error jika teks kurang dari 10 kata.

2. **Endpoint Upload (Express.js):**
   - Mengunggah file gambar ke Google Cloud Storage.
   - Menyimpan metadata (URL gambar, judul, deskripsi) ke MySQL.

3. **Endpoint Items (Express.js):**
   - Mengambil semua data gambar dan metadata dari database.
   - Mendukung pengambilan data berdasarkan user ID.

4. **Endpoint Autentikasi (Express.js):**
   - **Register:** Mendaftarkan pengguna baru.
   - **Login:** Mengotentikasi pengguna.
   - **Logout:** Menghapus sesi pengguna.

---

### **Teknologi yang Digunakan**
- **Backend:**
  - Python Flask
  - Express.js (Node.js)

- **Database:**
  - Google Cloud SQL (MySQL)

- **Penyimpanan File:**
  - Google Cloud Storage

- **Deployment:**
  - Docker, Docker Hub
  - Google Cloud Run

---

### **Cara Instalasi dan Menjalankan Proyek**

#### **1. Menjalankan Flask API**
1. Clone repository ini.
2. Masuk ke direktori proyek Flask.
3. Install dependensi:
   ```bash
   pip install -r requirements.txt
   ```
4. Jalankan server lokal:
   ```bash
   python app.py
   ```

#### **2. Menjalankan Express.js API**
1. Masuk ke direktori proyek Express.
2. Install dependensi:
   ```bash
   npm install
   ```
3. Jalankan server lokal:
   ```bash
   npm start
   ```

#### **3. Deployment dengan Docker**
1. Build Docker image:
   ```bash
   docker build -t <nama-image> .
   ```
2. Push image ke Docker Hub:
   ```bash
   docker push <username-dockerhub>/<nama-image>
   ```
3. Deploy ke Google Cloud Run:
   - Buka Google Cloud Console.
   - Pilih Cloud Run, buat service baru, dan gunakan image dari Docker Hub.

---

### **Endpoint API**

#### **1. Endpoint Summarize (Flask)**
- **URL:** `/summarize`
- **Method:** POST
- **Request Body:**
  ```json
  {
    "text": "<teks panjang>"
  }
  ```
- **Response Sukses:**
  ```json
  {
    "status": "success",
    "summary": "<ringkasan teks>"
  }
  ```
- **Response Error:**
  ```json
  {
    "status": "error",
    "message": "Teks harus lebih dari 10 kata."
  }
  ```

#### **2. Endpoint Upload (Express.js)**
- **URL:** `/upload`
- **Method:** POST
- **Request Body:**
  - Form Data:
    - `file`: file gambar
    - `title`: string
    - `description`: string
- **Response Sukses:**
  ```json
  {
    "status": "success",
    "data": {
      "url": "<public URL gambar>",
      "title": "<judul>",
      "description": "<deskripsi>"
    }
  }
  ```

#### **3. Endpoint Items (Express.js)**
- **URL:** `/items`
- **Method:** GET
- **Response Sukses:**
  ```json
  {
    "status": "success",
    "data": [
      {
        "id": 1,
        "url": "<public URL>",
        "title": "<judul>",
        "description": "<deskripsi>"
      }
    ]
  }
  ```

#### **4. Endpoint Autentikasi (Express.js)**
- **Register:**
  - **URL:** `/register`
  - **Method:** POST
  - **Request Body:**
    ```json
    {
      "email": "<email>",
      "username": "<username>",
      "password": "<password>",
      "confirm_password": "<konfirmasi password>"
    }
    ```

- **Login:**
  - **URL:** `/login`
  - **Method:** POST
  - **Request Body:**
    ```json
    {
      "username": "<username>",
      "password": "<password>"
    }
    ```

- **Logout:**
  - **URL:** `/logout`
  - **Method:** POST

---

### **Struktur Database**
- **Tabel:** `items`
  - Kolom:
    - `id` (integer, primary key, auto increment)
    - `url` (string, public URL gambar)
    - `title` (string)
    - `description` (string)
- **Tabel:** `users`
  - Kolom:
    - `id` (integer, primary key, auto increment)
    - `email` (string, unique)
    - `username` (string, unique)
    - `password` (hashed string)

---

### **Dokumentasi Tambahan**
- **API Documentation:** [Postman Documentation](https://documenter.getpostman.com/view/27063468/2sAYBbepKT)

---