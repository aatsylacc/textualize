const axios = require('axios');

const ocrHandler = async (req, res) => {
    const { image_url } = req.body;  // Ambil URL gambar dari request body
    const cloudRunUrl = 'https://your-cloud-run-url';  // Ganti dengan URL Cloud Run kamu

    try {
        const response = await axios.post(cloudRunUrl, { image_url });
        res.status(200).send(response.data);  // Balikin hasil OCR ke client
    } catch (error) {
        res.status(500).send({ error: 'OCR failed', details: error.message });
    }
};

module.exports = ocrHandler;
