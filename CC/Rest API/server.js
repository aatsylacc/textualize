const express = require('express');
const cors = require('cors');
const axios = require('axios');
const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Endpoint default
app.get('/', (req, res) => {
    res.send('Server berjalan! Tambahkan endpoint untuk request.');
});

// Route untuk Summarization
app.post('/api/summarize', async (req, res) => {
    const { text } = req.body;
    console.log("Received text in Express:", text);  // Debug log

    // Validasi input
    if (!text || text.split(' ').length < 10) {
        return res.status(400).json({ error: 'Text is too short. Please provide at least 10 words.' });
    }

    try {
        // Kirim request ke Flask server
        const response = await axios.post('http://127.0.0.1:5000/summarize', { text });

        // Debug log untuk melihat apa yang dikembalikan dari Flask
        console.log("Response from Flask:", response.data);  // Debug log

        if (response.data && response.data.summary) {
            res.json({ summary: response.data.summary });
        } else {
            res.status(500).json({ error: 'Failed to get summary from Flask.' });
        }
    } catch (error) {
        console.error("Error from Flask:", error.message);  // Debug log
        res.status(500).json({ error: 'Failed to process summarization.' });
    }
});

// Jalankan server di port 8080
app.listen(8080, () => {
    console.log('Server berjalan di port 8080');
});
