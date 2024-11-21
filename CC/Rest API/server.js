const express = require('express');
const cors = require('cors');
const app = express();

// import routes
const ocrRoute = require('./routes/ocr/route');  // route OCR
const summarizeRoute = require('./routes/summarize/route');  // route Summarization

// middleware
app.use(cors());
app.use(express.json());

// route default
app.get('/', (req, res) => {
    res.send('Server berjalan! Tambahkan endpoint untuk request.');
});

// pake route OCR dan summarization
app.use('/api/ocr', ocrRoute);  // route OCR diawali dengan '/api/ocr'
app.use('/api/summarize', summarizeRoute);  // route summarization diawali dengan '/api/summarize'

app.listen(8080, () => {
    console.log('Server berjalan di port 8080');
});
