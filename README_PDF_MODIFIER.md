# PDF Text Modifier Tool

A comprehensive Python tool for extracting, modifying, and regenerating PDF text content. Supports both regular text-based PDFs and image-based PDFs using OCR (Optical Character Recognition).

## Features

- **Text Extraction**: Extract text from regular PDF files
- **OCR Support**: Extract text from image-based PDFs using Tesseract OCR
- **Text Modification**: Replace specific text patterns with new content
- **PDF Generation**: Create new PDFs with modified text
- **Interactive Mode**: User-friendly interactive interface
- **Command Line Interface**: Scriptable command-line usage
- **Auto-detection**: Automatically switches to OCR when needed

## Installation

### Prerequisites

Make sure you have Python 3.7+ installed on your system.

### System Dependencies

```bash
# On Ubuntu/Debian:
sudo apt update
sudo apt install python3-venv python3-pip tesseract-ocr poppler-utils

# On macOS (with Homebrew):
brew install tesseract poppler

# On Windows:
# Download and install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
# Download and install Poppler from: https://blog.alivate.com.au/poppler-windows/
```

### Python Environment Setup

```bash
# Create virtual environment
python3 -m venv pdf_env

# Activate virtual environment
source pdf_env/bin/activate  # On Linux/Mac
# or
pdf_env\Scripts\activate     # On Windows

# Install Python dependencies
pip install PyPDF2 reportlab Pillow pytesseract pdf2image
```

## Quick Start

### 1. Create a Sample PDF for Testing

```bash
python3 create_sample_pdf.py
```

### 2. Run Interactive Mode

```bash
python3 pdf_text_modifier.py --interactive
```

### 3. Run Examples

```bash
python3 example_usage.py
```

## Usage

### Interactive Mode

The easiest way to use the tool:

```bash
python3 pdf_text_modifier.py --interactive
```

This will guide you through:
1. Selecting your PDF file
2. Choosing OCR options
3. Previewing extracted text
4. Defining text modifications
5. Specifying output location

### Command Line Usage

#### Basic text replacement:
```bash
python3 pdf_text_modifier.py input.pdf output.pdf --find "old text" --replace "new text"
```

#### Multiple replacements:
```bash
python3 pdf_text_modifier.py input.pdf output.pdf \
    --find "Company A" --replace "Company B" \
    --find "$100" --replace "$200"
```

#### Force OCR mode:
```bash
python3 pdf_text_modifier.py input.pdf output.pdf --ocr --find "old" --replace "new"
```

#### Just show help:
```bash
python3 pdf_text_modifier.py --help
```

### Programmatic Usage

```python
from pdf_text_modifier import PDFTextModifier

# Initialize the modifier
modifier = PDFTextModifier()

# Define text modifications
modifications = {
    "Old Company Name": "New Company Name",
    "$99.99": "$149.99",
    "2023": "2024"
}

# Process the PDF
success = modifier.process_pdf(
    input_pdf="original.pdf",
    output_pdf="modified.pdf", 
    modifications=modifications,
    use_ocr=False  # Set to True for image-based PDFs
)

if success:
    print("PDF modification completed successfully!")
```

## Examples

### Example 1: Business Document Updates

```python
modifications = {
    "Acme Corporation": "TechCorp Industries",
    "2023 Annual Report": "2024 Annual Report",
    "CEO John Smith": "CEO Jane Doe",
    "$1,000,000": "$1,200,000"
}
```

### Example 2: Price Updates

```python
modifications = {
    "$299.99": "$349.99",
    "$499.99": "$549.99", 
    "Special Offer": "Limited Time Offer"
}
```

### Example 3: Contact Information Updates

```python
modifications = {
    "123 Main Street": "456 Innovation Drive",
    "(555) 123-4567": "(555) 987-6543",
    "info@oldcompany.com": "info@newcompany.com"
}
```

## File Structure

```
├── pdf_text_modifier.py     # Main PDF modification tool
├── create_sample_pdf.py     # Generate sample PDFs for testing
├── example_usage.py         # Usage examples and demonstrations
├── README_PDF_MODIFIER.md   # This documentation
└── pdf_env/                 # Virtual environment (created after setup)
```

## How It Works

1. **Text Extraction**: The tool first tries to extract text directly from the PDF using PyPDF2
2. **OCR Fallback**: If little or no text is found, it automatically switches to OCR mode using pdf2image and pytesseract
3. **Text Modification**: Applies your specified text replacements using string substitution
4. **PDF Generation**: Creates a new PDF with the modified text using ReportLab
5. **Formatting**: Preserves basic document structure and formatting

## Supported PDF Types

- **Text-based PDFs**: Standard PDFs with selectable text
- **Image-based PDFs**: Scanned documents, images converted to PDF
- **Mixed PDFs**: Documents with both text and images
- **Multi-page documents**: Handles documents with any number of pages

## Limitations

- Complex formatting (tables, charts, complex layouts) may not be perfectly preserved
- Images and graphics are not preserved in the output PDF
- OCR accuracy depends on image quality and text clarity
- Very large PDFs may require more processing time

## Troubleshooting

### Common Issues

1. **"No text could be extracted"**
   - Try running with `--ocr` flag
   - Ensure the PDF contains readable text or images

2. **OCR not working**
   - Verify Tesseract is installed: `tesseract --version`
   - Check that poppler-utils is installed for PDF to image conversion

3. **Permission errors**
   - Ensure you have read access to input PDF
   - Ensure you have write access to output location

4. **Import errors**
   - Activate the virtual environment: `source pdf_env/bin/activate`
   - Reinstall dependencies: `pip install -r requirements.txt`

### Getting Help

Run with verbose output to see detailed processing information:
```bash
python3 pdf_text_modifier.py input.pdf output.pdf --find "old" --replace "new" -v
```

## Advanced Usage

### Custom PDF Formatting

You can modify the `create_new_pdf` method in `PDFTextModifier` class to customize:
- Page size (letter, A4, etc.)
- Font styles and sizes  
- Spacing and margins
- Headers and footers

### Batch Processing

Create a script to process multiple PDFs:

```python
import os
from pdf_text_modifier import PDFTextModifier

modifier = PDFTextModifier()
modifications = {"old": "new"}

for filename in os.listdir("input_pdfs/"):
    if filename.endswith(".pdf"):
        input_path = f"input_pdfs/{filename}"
        output_path = f"output_pdfs/modified_{filename}"
        modifier.process_pdf(input_path, output_path, modifications)
```

## License

This tool is provided as-is for educational and practical use. Make sure to comply with any licensing terms of the underlying libraries (PyPDF2, ReportLab, etc.).

## Contributing

Feel free to extend and improve this tool! Some areas for enhancement:
- Better formatting preservation
- Support for more complex document structures
- Batch processing GUI
- Additional output formats
- Regular expression support for pattern matching