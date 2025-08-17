#!/bin/bash

echo "PDF Text Modifier - Setup Script"
echo "================================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Error: Node.js is not installed. Please install Node.js version 14 or higher."
    echo "Visit: https://nodejs.org/"
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 14 ]; then
    echo "Error: Node.js version 14 or higher is required. Current version: $(node -v)"
    exit 1
fi

echo "✓ Node.js $(node -v) is installed"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "Error: npm is not installed."
    exit 1
fi

echo "✓ npm $(npm -v) is installed"

# Create necessary directories
echo "Creating directories..."
mkdir -p uploads
mkdir -p outputs
echo "✓ Directories created"

# Install dependencies
echo "Installing Node.js dependencies..."
npm install

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "✗ Failed to install dependencies"
    exit 1
fi

# Check if Python is available (optional)
if command -v python3 &> /dev/null; then
    echo "✓ Python 3 is available"
    echo "Installing Python dependencies..."
    pip3 install PyPDF2 pdfplumber reportlab 2>/dev/null || echo "Note: Python dependencies installation failed (optional)"
else
    echo "Note: Python 3 not found (optional for command-line tools)"
fi

# Make scripts executable
chmod +x pdf_text_modifier.py
chmod +x pdf_text_modifier.js

echo ""
echo "Setup completed successfully!"
echo ""
echo "To start the application:"
echo "1. Start the API server: npm run dev"
echo "2. In another terminal, start the React app: npm start"
echo "3. Open http://localhost:3000 in your browser"
echo ""
echo "For command-line usage:"
echo "- Python: python3 pdf_text_modifier.py --help"
echo "- Node.js: node pdf_text_modifier.js --help"
echo ""
echo "Happy PDF modifying! 🎉"