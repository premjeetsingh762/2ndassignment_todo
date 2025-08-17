const express = require('express');
const multer = require('multer');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

// Import our PDF modifier
const PDFTextModifier = require('./pdf_text_modifier.js');

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Configure multer for file uploads
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    const uploadDir = './uploads';
    if (!fs.existsSync(uploadDir)) {
      fs.mkdirSync(uploadDir, { recursive: true });
    }
    cb(null, uploadDir);
  },
  filename: function (req, file, cb) {
    cb(null, Date.now() + '-' + file.originalname);
  }
});

const upload = multer({ 
  storage: storage,
  fileFilter: (req, file, cb) => {
    if (file.mimetype === 'application/pdf') {
      cb(null, true);
    } else {
      cb(new Error('Only PDF files are allowed'), false);
    }
  },
  limits: {
    fileSize: 10 * 1024 * 1024 // 10MB limit
  }
});

// Routes
app.post('/api/extract-text', upload.single('pdf'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No PDF file uploaded' });
    }

    const pdfPath = req.file.path;
    const modifier = new PDFTextModifier(pdfPath);
    
    // Load the PDF
    await modifier.loadPDF(pdfPath);
    
    // Extract text
    const textContent = await modifier.extractText();
    
    // Clean up uploaded file
    fs.unlinkSync(pdfPath);
    
    res.json({ 
      success: true, 
      textContent: textContent,
      message: 'Text extracted successfully'
    });
    
  } catch (error) {
    console.error('Error extracting text:', error);
    
    // Clean up uploaded file if it exists
    if (req.file && fs.existsSync(req.file.path)) {
      fs.unlinkSync(req.file.path);
    }
    
    res.status(500).json({ 
      error: 'Failed to extract text from PDF',
      details: error.message 
    });
  }
});

app.post('/api/generate-pdf', upload.single('pdf'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No PDF file uploaded' });
    }

    if (!req.body.modifications) {
      return res.status(400).json({ error: 'No modifications provided' });
    }

    const pdfPath = req.file.path;
    const modifications = JSON.parse(req.body.modifications);
    
    const modifier = new PDFTextModifier(pdfPath);
    
    // Load the PDF
    await modifier.loadPDF(pdfPath);
    
    // Apply modifications
    for (const mod of modifications) {
      if (mod.type === 'replace') {
        modifier.replaceText(mod.oldText, mod.newText);
      } else if (mod.type === 'add') {
        modifier.addText(mod.text, mod.page, mod.x, mod.y);
      }
    }
    
    // Generate output path
    const outputDir = './outputs';
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }
    
    const outputPath = path.join(outputDir, `modified-${Date.now()}.pdf`);
    
    // Generate modified PDF
    const result = await modifier.generateNewPDF(outputPath, pdfPath);
    
    if (result) {
      // Send the file
      res.download(outputPath, `modified-${req.file.originalname}`, (err) => {
        // Clean up files after sending
        if (fs.existsSync(pdfPath)) {
          fs.unlinkSync(pdfPath);
        }
        if (fs.existsSync(outputPath)) {
          fs.unlinkSync(outputPath);
        }
        
        if (err) {
          console.error('Error sending file:', err);
        }
      });
    } else {
      throw new Error('Failed to generate modified PDF');
    }
    
  } catch (error) {
    console.error('Error generating PDF:', error);
    
    // Clean up uploaded file if it exists
    if (req.file && fs.existsSync(req.file.path)) {
      fs.unlinkSync(req.file.path);
    }
    
    res.status(500).json({ 
      error: 'Failed to generate modified PDF',
      details: error.message 
    });
  }
});

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', message: 'PDF Text Modifier API is running' });
});

// Error handling middleware
app.use((error, req, res, next) => {
  console.error('Server error:', error);
  
  if (error instanceof multer.MulterError) {
    if (error.code === 'LIMIT_FILE_SIZE') {
      return res.status(400).json({ error: 'File too large. Maximum size is 10MB.' });
    }
  }
  
  res.status(500).json({ 
    error: 'Internal server error',
    details: error.message 
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`PDF Text Modifier API server running on port ${PORT}`);
  console.log(`Health check: http://localhost:${PORT}/api/health`);
});

module.exports = app;