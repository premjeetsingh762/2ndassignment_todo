# PDF Text Modifier

A comprehensive tool for modifying text contents in PDF files and generating new ones. This application provides multiple interfaces including command-line tools, a web API, and a React-based web interface.

## Features

- **Text Extraction**: Extract text from PDF files with page-by-page breakdown
- **Text Replacement**: Replace specific text strings within PDFs
- **Text Addition**: Add new text at specific coordinates on PDF pages
- **Multiple Interfaces**: Command-line, Node.js API, and web interface
- **Cross-platform**: Works on Windows, macOS, and Linux
- **File Size Support**: Handles PDFs up to 10MB

## Installation

### Prerequisites

- Node.js (version 14 or higher)
- Python 3.7+ (for Python scripts)
- npm or yarn

### Quick Start

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   ```

4. **Open your browser** and navigate to `http://localhost:3000`

## Usage

### Web Interface (Recommended)

1. Open the application in your browser
2. Click on the "PDF Text Modifier" tab
3. Upload a PDF file using the "Select PDF File" button
4. Click "Extract Text" to see the current text content
5. Add modifications:
   - **Text Replacement**: Replace existing text with new text
   - **Add Text**: Add new text at specific coordinates
6. Click "Generate Modified PDF" to create and download the new PDF

### Command Line Interface

#### Python Version

```bash
# Extract text from PDF
python pdf_text_modifier.py input.pdf output.pdf --extract

# Replace text
python pdf_text_modifier.py input.pdf output.pdf --replace "old text" "new text"

# Add text at specific position
python pdf_text_modifier.py input.pdf output.pdf --add-text "Hello World" 1 100 100

# Save modifications to JSON file
python pdf_text_modifier.py input.pdf output.pdf --replace "old" "new" --save-modifications mods.json

# Load modifications from JSON file
python pdf_text_modifier.py input.pdf output.pdf --load-modifications mods.json
```

#### Node.js Version

```bash
# Extract text from PDF
node pdf_text_modifier.js input.pdf output.pdf --extract

# Replace text
node pdf_text_modifier.js input.pdf output.pdf --replace "old text" "new text"

# Add text at specific position
node pdf_text_modifier.js input.pdf output.pdf --add-text "Hello World" 1 100 100

# Save modifications to JSON file
node pdf_text_modifier.js input.pdf output.pdf --replace "old" "new" --save-modifications mods.json

# Load modifications from JSON file
node pdf_text_modifier.js input.pdf output.pdf --load-modifications mods.json
```

### API Endpoints

The application includes a REST API server running on port 3001:

#### Extract Text
```bash
POST /api/extract-text
Content-Type: multipart/form-data

Body: pdf file
```

#### Generate Modified PDF
```bash
POST /api/generate-pdf
Content-Type: multipart/form-data

Body: 
- pdf file
- modifications (JSON string)
```

#### Health Check
```bash
GET /api/health
```

## File Structure

```
pdf-text-modifier/
├── App.js                 # Main React application
├── App.css               # Main application styles
├── PDFModifier.js        # PDF modifier React component
├── PDFModifier.css       # PDF modifier styles
├── pdf_text_modifier.py  # Python PDF modifier script
├── pdf_text_modifier.js  # Node.js PDF modifier script
├── server.js             # Express API server
├── package.json          # Node.js dependencies
└── README.md            # This file
```

## API Examples

### Using curl

```bash
# Extract text
curl -X POST -F "pdf=@input.pdf" http://localhost:3001/api/extract-text

# Generate modified PDF
curl -X POST \
  -F "pdf=@input.pdf" \
  -F 'modifications=[{"type":"replace","oldText":"old","newText":"new","page":1}]' \
  http://localhost:3001/api/generate-pdf \
  --output modified.pdf
```

### Using JavaScript

```javascript
// Extract text
const formData = new FormData();
formData.append('pdf', pdfFile);

const response = await fetch('/api/extract-text', {
  method: 'POST',
  body: formData
});

const data = await response.json();
console.log(data.textContent);

// Generate modified PDF
const modifications = [
  {
    type: 'replace',
    oldText: 'old text',
    newText: 'new text',
    page: 1
  },
  {
    type: 'add',
    text: 'New text',
    page: 1,
    x: 100,
    y: 100
  }
];

const formData = new FormData();
formData.append('pdf', pdfFile);
formData.append('modifications', JSON.stringify(modifications));

const response = await fetch('/api/generate-pdf', {
  method: 'POST',
  body: formData
});

const blob = await response.blob();
// Handle the downloaded PDF blob
```

## Configuration

### Environment Variables

- `PORT`: Server port (default: 3001)
- `NODE_ENV`: Environment mode (development/production)

### File Upload Limits

- Maximum file size: 10MB
- Allowed file types: PDF only

## Troubleshooting

### Common Issues

1. **"Module not found" errors**: Run `npm install` to install dependencies
2. **Port already in use**: Change the PORT environment variable
3. **File upload fails**: Check file size and ensure it's a valid PDF
4. **Text extraction fails**: Some PDFs may have embedded text that's difficult to extract

### Debug Mode

Run the server in debug mode:
```bash
DEBUG=* npm run dev
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Create an issue in the repository

## Changelog

### Version 1.0.0
- Initial release
- Text extraction and replacement
- Web interface
- Command-line tools
- REST API
- Support for multiple PDF formats