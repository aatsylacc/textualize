const express = require('express');
const summarizeHandler = require('../../routes/summarize/handler');
const router = express.Router();

// route untuk handle request Summarize
router.post('/', summarizeHandler);

module.exports = router;
