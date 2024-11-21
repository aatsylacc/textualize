const axios = require('axios');

const ocrHandler = async (req, res) => {
    const { image_url } = req.body;  // ambil URL gambar dari request body
    const cloudRunUrl = 'https://your-cloud-run-url';  // ganti pake URL Cloud Run 

    try {
        const response = await axios.post(cloudRunUrl, { image_url });
        res.status(200).send(response.data);  // balikin hasil OCR ke client
    } catch (error) {
        res.status(500).send({ error: 'OCR failed', details: error.message });
    }
};

module.exports = ocrHandler;
