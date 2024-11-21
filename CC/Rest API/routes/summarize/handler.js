const summarizeHandler = async (req, res) => {
    const { text } = req.body;  // Ambil teks dari request body

    // Proses summarization (misalnya pake model atau library tertentu)
    const summarizedText = `Summarized: ${text}`;  // Ini contoh, ganti dengan logika summarization asli

    res.status(200).send({ summarizedText });
};

module.exports = summarizeHandler;
