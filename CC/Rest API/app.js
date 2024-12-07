const express = require('express');
const multer = require('multer');
const { Storage } = require('@google-cloud/storage');
const mysql = require('mysql2');
const path = require('path');
const axios = require('axios');
const app = express();
const port = 3000;

const db = mysql.createConnection({
    host: '10.118.96.3',
    user: 'root',
    password: '',
    database: 'db_textualize',
    port: 3306
});

db.connect((err) => {
    if (err) {
        console.error('Error connecting to the database:', err.message);
        return;
    }
    console.log('Connected to MySQL database');
});

const storage = new Storage({ keyFilename: 'gcp-key.json' });
const bucketName = 'capstone-textualize-bucket';
const bucket = storage.bucket(bucketName);

app.use(express.urlencoded({ extended: true }));
app.use(express.json());

app.post('/upload', upload.single('image'), (req, res) => {
    const { title, description } = req.body;

    if (!req.file) {
        return res.status(400).json({ 
            message: 'File tidak ditemukan',
            status: 'error',
        });
    }

    const blob = bucket.file(Date.now() + path.extname(req.file.originalname));
    const blobStream = blob.createWriteStream({
        resumable: false,
        contentType: req.file.mimetype,
    });

    blobStream.on('error', (err) => {
        console.error('Error uploading file to GCS:', err.message);
        res.status(500).json({ 
            message: 'Error upload file ke GCS',
            status: 'error',
        });
    });

    blobStream.on('finish', () => {
        const publicUrl = `https://storage.googleapis.com/${bucketName}/${blob.name}`;

        const query = 'INSERT INTO items (url, judul, deskripsi) VALUES (?, ?, ?)';
        db.query(query, [publicUrl, title, description], (err, result) => {
            if (err) {
                console.error('Error inserting data into database:', err.message);
                res.status(500).json({
                    message: 'Gagal menyimpan data ke database',
                    status: 'error',
                })
                return;
            }

            res.status(200).send({
                message: 'File berhasil diunggah dan data berhasil disimpan',
                status: 'success',
                data: {
                    id: result.insertId,
                    url: publicUrl,
                    title,
                    description,
                },
            });
        });
    });

    blobStream.end(req.file.buffer);
});

app.post('/summarize', upload.none(), async (req, res) => {
    let text;

    if (req.is('application/x-www-form-urlencoded')) {
        text = req.body.text;
    } else if (req.is('application/json')) {
        text = req.body.text;
    } else if (req.is('multipart/form-data')) {
        text = req.body.text;
    }

    if (!text) {
        return res.status(400).json({ 
            message: 'Text Kosong',
            status: 'error',
        });
    }

    try {
        const response = await axios.post('https://textualize-model-api-1012438187384.asia-southeast2.run.app/summarize', 
            new URLSearchParams({ text }), {
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            });

        const { message, status } = response.data;
        
        res.status(200).json({
            message: 'Berhasil mengirim permintaan summarization',
            data: {
                result: message,
            },
            status: status,
        });
    } catch (error) {
        console.error('Error during summarization request:', error.message);
        res.status(500).json({ 
            message: 'Gagal mengirim permintaan summarization',
            status: 'error',
        });
    }
});

app.get('/items', (req, res) => {
    const query = 'SELECT * FROM items';

    db.query(query, (err, results) => {
        if (err) {
            console.error('Error fetching items from database:', err.message);
            return res.status(500).json({
                message: 'Gagal mengambil data dari database',
                status: 'error',
            });
        }

        res.status(200).json({
            message: 'Data items berhasil diambil',
            status: 'success',
            data: results,
        });
    });
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
