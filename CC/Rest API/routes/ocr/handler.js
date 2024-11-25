const axios = require('axios');

const ocrHandler = async (req, res) => {
    const { image_url } = req.body;  // ambil URL gambar dari request body

    // validasi input: cek image_url ada atau engga
    if (!image_url) {
        return res.status(400).json({
            error: true,
            message: 'Image URL is required'
        });
    }

    const cloudRunUrl = 'https://your-cloud-run-url';  // ganti pake URL Cloud Run 

    try {
        // coba kirim request ke Cloud Run untuk OCR
        const response = await axios.post(cloudRunUrl, { image_url });

        // kalo response dari Cloud Run gak OK, throw error
        if (response.status !== 200) {
            throw new Error('Failed to process OCR');
        }

        // kirim hasil OCR ke client
        res.status(200).json({
            error: false,
            message: 'OCR Success',
            data: response.data
        });
    } catch (error) {
        // kalo ada error, log dan kirim response error
        console.error('OCR Error:', error.message);
        res.status(500).json({
            error: true,
            message: 'An error occurred during OCR processing',
            details: error.message
        });
    }
};

module.exports = ocrHandler;
