#!/usr/bin/env python3
"""
PDF Text Modifier - Extract, modify, and regenerate PDF text content
Supports both text-based PDFs and PDFs with images containing text (OCR)
"""

import os
import sys
from pathlib import Path
import argparse
from typing import List, Dict, Optional

try:
    import PyPDF2
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.units import inch
    from PIL import Image
    import pytesseract
    from pdf2image import convert_from_path
except ImportError as e:
    print(f"Error importing required libraries: {e}")
    print("Please make sure all dependencies are installed:")
    print("pip install PyPDF2 reportlab Pillow pytesseract pdf2image")
    sys.exit(1)


class PDFTextModifier:
    """A class to handle PDF text extraction, modification, and regeneration."""
    
    def __init__(self):
        self.extracted_text = ""
        self.modified_text = ""
        self.pages_text = []
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from a PDF file."""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                self.pages_text = []
                
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    self.pages_text.append(page_text)
                    text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
                
                self.extracted_text = text
                return text
                
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""
    
    def extract_text_from_images_in_pdf(self, pdf_path: str) -> str:
        """Extract text from images in PDF using OCR."""
        try:
            # Convert PDF to images
            images = convert_from_path(pdf_path)
            text = ""
            self.pages_text = []
            
            for page_num, image in enumerate(images):
                # Perform OCR on each page image
                page_text = pytesseract.image_to_string(image)
                self.pages_text.append(page_text)
                text += f"\n--- Page {page_num + 1} (OCR) ---\n{page_text}\n"
            
            self.extracted_text = text
            return text
            
        except Exception as e:
            print(f"Error extracting text from images in PDF: {e}")
            return ""
    
    def modify_text(self, text: str, modifications: Dict[str, str]) -> str:
        """Modify text based on provided substitutions."""
        modified = text
        
        for old_text, new_text in modifications.items():
            modified = modified.replace(old_text, new_text)
        
        self.modified_text = modified
        return modified
    
    def create_new_pdf(self, output_path: str, text: str, page_size=letter):
        """Create a new PDF with the modified text."""
        try:
            doc = SimpleDocTemplate(output_path, pagesize=page_size)
            styles = getSampleStyleSheet()
            normal_style = styles['Normal']
            title_style = styles['Title']
            
            story = []
            
            # Split text by pages if page markers exist
            if "--- Page" in text:
                pages = text.split("--- Page")[1:]  # Skip empty first element
                
                for i, page_content in enumerate(pages):
                    # Remove page number marker
                    content = page_content.split("---\n", 1)
                    if len(content) > 1:
                        page_text = content[1].strip()
                    else:
                        page_text = page_content.strip()
                    
                    if page_text:
                        # Add page title
                        story.append(Paragraph(f"Page {i + 1}", title_style))
                        story.append(Spacer(1, 0.2*inch))
                        
                        # Add page content
                        paragraphs = page_text.split('\n\n')
                        for para in paragraphs:
                            if para.strip():
                                story.append(Paragraph(para.strip(), normal_style))
                                story.append(Spacer(1, 0.1*inch))
                        
                        # Add page break except for last page
                        if i < len(pages) - 1:
                            story.append(Spacer(1, 0.5*inch))
            else:
                # No page markers, treat as single document
                paragraphs = text.split('\n\n')
                for para in paragraphs:
                    if para.strip():
                        story.append(Paragraph(para.strip(), normal_style))
                        story.append(Spacer(1, 0.1*inch))
            
            doc.build(story)
            print(f"New PDF created successfully: {output_path}")
            
        except Exception as e:
            print(f"Error creating new PDF: {e}")
    
    def process_pdf(self, input_pdf: str, output_pdf: str, modifications: Dict[str, str], use_ocr: bool = False):
        """Complete workflow to process a PDF."""
        print(f"Processing PDF: {input_pdf}")
        
        # Extract text
        if use_ocr:
            print("Extracting text using OCR...")
            text = self.extract_text_from_images_in_pdf(input_pdf)
        else:
            print("Extracting text from PDF...")
            text = self.extract_text_from_pdf(input_pdf)
            
            # If no text found, try OCR
            if not text.strip() or len(text.strip()) < 50:
                print("Little or no text found. Trying OCR...")
                text = self.extract_text_from_images_in_pdf(input_pdf)
        
        if not text.strip():
            print("No text could be extracted from the PDF.")
            return False
        
        print(f"Extracted {len(text)} characters from PDF")
        
        # Modify text
        print("Applying modifications...")
        modified_text = self.modify_text(text, modifications)
        
        # Create new PDF
        print(f"Creating new PDF: {output_pdf}")
        self.create_new_pdf(output_pdf, modified_text)
        
        return True


def interactive_mode():
    """Interactive mode for PDF text modification."""
    modifier = PDFTextModifier()
    
    print("=== PDF Text Modifier - Interactive Mode ===")
    
    # Get input PDF
    while True:
        input_pdf = input("Enter the path to your PDF file: ").strip()
        if os.path.exists(input_pdf):
            break
        print("File not found. Please enter a valid path.")
    
    # Ask about OCR
    use_ocr = input("Use OCR for image-based text? (y/n, default: auto-detect): ").strip().lower() == 'y'
    
    # Extract text first to show user
    print("\nExtracting text from PDF...")
    if use_ocr:
        text = modifier.extract_text_from_images_in_pdf(input_pdf)
    else:
        text = modifier.extract_text_from_pdf(input_pdf)
        if not text.strip() or len(text.strip()) < 50:
            print("Little text found. Switching to OCR...")
            text = modifier.extract_text_from_images_in_pdf(input_pdf)
    
    if not text.strip():
        print("No text could be extracted from the PDF.")
        return
    
    print(f"\n--- Extracted Text Preview (first 500 chars) ---")
    print(text[:500] + ("..." if len(text) > 500 else ""))
    print(f"\nTotal characters extracted: {len(text)}")
    
    # Get modifications
    modifications = {}
    print("\n--- Text Modifications ---")
    print("Enter text substitutions (press Enter with empty 'find' to finish):")
    
    while True:
        find_text = input("Text to find: ").strip()
        if not find_text:
            break
        replace_text = input("Replace with: ").strip()
        modifications[find_text] = replace_text
        print(f"Added: '{find_text}' -> '{replace_text}'")
    
    if not modifications:
        print("No modifications specified. Creating copy of original text.")
    
    # Get output path
    default_output = input_pdf.replace('.pdf', '_modified.pdf')
    output_pdf = input(f"Output PDF path (default: {default_output}): ").strip()
    if not output_pdf:
        output_pdf = default_output
    
    # Process the PDF
    success = modifier.process_pdf(input_pdf, output_pdf, modifications, use_ocr)
    
    if success:
        print(f"\n✅ Success! Modified PDF saved as: {output_pdf}")
    else:
        print("\n❌ Failed to process PDF.")


def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(description="Modify text content in PDF files")
    parser.add_argument("input_pdf", nargs='?', help="Input PDF file path")
    parser.add_argument("output_pdf", nargs='?', help="Output PDF file path")
    parser.add_argument("--ocr", action="store_true", help="Force OCR mode for image-based text")
    parser.add_argument("--find", action="append", help="Text to find (can be used multiple times)")
    parser.add_argument("--replace", action="append", help="Text to replace with (must match --find)")
    parser.add_argument("--interactive", "-i", action="store_true", help="Run in interactive mode")
    
    args = parser.parse_args()
    
    # Interactive mode
    if args.interactive or not args.input_pdf:
        interactive_mode()
        return
    
    # Command line mode
    if not args.output_pdf:
        args.output_pdf = args.input_pdf.replace('.pdf', '_modified.pdf')
    
    # Build modifications dictionary
    modifications = {}
    if args.find and args.replace:
        if len(args.find) != len(args.replace):
            print("Error: Number of --find and --replace arguments must match")
            sys.exit(1)
        modifications = dict(zip(args.find, args.replace))
    
    # Process PDF
    modifier = PDFTextModifier()
    success = modifier.process_pdf(args.input_pdf, args.output_pdf, modifications, args.ocr)
    
    if success:
        print(f"✅ Success! Modified PDF saved as: {args.output_pdf}")
    else:
        print("❌ Failed to process PDF.")
        sys.exit(1)


if __name__ == "__main__":
    main()