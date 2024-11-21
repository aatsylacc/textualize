const express = require('express');
const ocrHandler = require('../../routes/ocr/handler');
const router = express.Router();

// route untuk handle request OCR
router.post('/', ocrHandler);

module.exports = router;
