const express = require('express');
const multer = require('multer');
const { Storage } = require('@google-cloud/storage');
const mysql = require('mysql2');
const path = require('path');
const axios = require('axios');
const bcrypt = require('bcryptjs');
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

const upload = multer({
    storage: multer.memoryStorage(),
    limits: { fileSize: 5 * 1024 * 1024 },
});

app.use(express.urlencoded({ extended: true }));
app.use(express.json());

app.post('/register', upload.none(), async (req, res) => {
    const { email, username, password, confirmPassword } = req.body;

    if (!email || !username || !password || !confirmPassword) {
        return res.status(400).json({
            status: 'error',
            message: 'field tidak boleh kosong',
            data: null
        });
    }

    if (password !== confirmPassword) {
        return res.status(400).json({
            status: 'error',
            message: 'password dan konfirmasi password berbeda',
            data: null
        });
    }

    const checkQuery = 'SELECT * FROM users WHERE email = ? OR username = ?';
    db.query(checkQuery, [email, username], async (err, results) => {
        if (err) {
            console.error('Error querying database:', err.message);
            return res.status(500).json({
                status: 'error',
                message: 'internal server error',
                data: null
            });
        }

        if (results.length > 0) {
            return res.status(409).json({
                status: 'error',
                message: 'email or username sudah terpakai',
                data: null
            });
        }

        const hashedPassword = bcrypt.hashSync(password, 10);

        const insertQuery = 'INSERT INTO users (email, username, password) VALUES (?, ?, ?)';
        db.query(insertQuery, [email, username, hashedPassword], (err, result) => {
            if (err) {
                console.error('Error inserting user into database:', err.message);
                return res.status(500).json({
                    status: 'error',
                    message: 'internal server error',
                    data: null
                });
            }

            res.status(201).json({
                status: 'success',
                message: 'berhasil registrasi',
                data: { 
                    id: result.insertId,
                    email: email,
                    username: username
                }
            });
        });
    });
});

app.post('/login', upload.none(), (req, res) => {
    const { username, password } = req.body;

    if (!username || !password) {
        return res.status(400).json({
            status: 'error',
            message: 'field tidak boleh kosong',
            data: null
        });
    }

    // Query untuk memeriksa user berdasarkan username atau email
    const query = 'SELECT id, username, email, password FROM users WHERE username = ? OR email = ?';
    db.query(query, [username, username], async (err, results) => {
        if (err) {
            console.error('Error querying database:', err.message);
            return res.status(500).json({
                status: 'error',
                message: 'internal server error',
                data: null
            });
        }

        if (results.length === 0) {
            return res.status(401).json({
                status: 'error',
                message: 'username atau password salah',
                data: null
            });
        }

        const user = results[0];

        const isPasswordValid = bcrypt.compareSync(password, user.password);
        if (!isPasswordValid) {
            return res.status(401).json({
                status: 'error',
                message: 'username atau password salah',
                data: null
            });
        }

        res.status(200).json({
            status: 'success',
            message: 'login berhasil',
            data: {
                id: user.id,
                username: user.username,
                email: user.email
            }
        });
    });
});

app.post('/logout', (req, res) => {
    res.status(200).json({
        status: 'success',
        message: 'logout berhasil',
        data: null
    });
});

app.post('/upload', upload.single('image'), (req, res) => {
    const { title, description, userId } = req.body;

    if (!req.file) {
        return res.status(400).json({ 
            message: 'file tidak ditemukan',
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
            message: 'error upload file ke GCS',
            status: 'error',
        });
    });

    blobStream.on('finish', () => {
        const publicUrl = `https://storage.googleapis.com/${bucketName}/${blob.name}`;

        const query = 'INSERT INTO items (url, judul, deskripsi, user_id) VALUES (?, ?, ?, ?)';
        db.query(query, [publicUrl, title, description, userId], (err, result) => {
            if (err) {
                console.error('Error inserting data into database:', err.message);
                res.status(500).json({
                    message: 'gagal menyimpan data ke database',
                    status: 'error',
                })
                return;
            }

            res.status(200).send({
                message: 'file berhasil diunggah dan data berhasil disimpan',
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
            message: 'text Kosong',
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
            message: 'berhasil mengirim permintaan summarization',
            data: {
                result: message,
            },
            status: status,
        });
    } catch (error) {
        console.error('Error during summarization request:', error.message);
        res.status(500).json({ 
            message: 'gagal mengirim permintaan summarization',
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
                message: 'gagal mengambil data dari database',
                status: 'error',
            });
        }

        res.status(200).json({
            message: 'data items berhasil diambil',
            status: 'success',
            data: results,
        });
    });
});

app.get('/items/:user_id', (req, res) => {
    const { user_id } = req.params;

    if (!user_id) {
        return res.status(400).json({
            message: 'user_id tidak disediakan',
            status: 'error',
        });
    }

    const query = 'SELECT * FROM items WHERE user_id = ?';

    db.query(query, [user_id], (err, results) => {
        if (err) {
            console.error('Error fetching items from database:', err.message);
            return res.status(500).json({
                message: 'gagal mengambil data dari database',
                status: 'error',
            });
        }

        res.status(200).json({
            message: 'data items berhasil diambil',
            status: 'success',
            data: results,
        });
    });
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
