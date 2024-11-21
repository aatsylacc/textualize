const summarizeHandler = async (req, res) => {
    const { text } = req.body;  // ambil teks dari request body

    // proses summarization (misalnya pake model atau library tertentu)
    const summarizedText = `Summarized: ${text}`;  // ini contoh, ganti dengan logika summarization asli

    res.status(200).send({ summarizedText });
};

module.exports = summarizeHandler;
