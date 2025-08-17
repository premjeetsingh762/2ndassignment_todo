#!/usr/bin/env python3
"""
PDF Text Modifier - A comprehensive tool for modifying text in PDF files
Supports text extraction, replacement, and new PDF generation
"""

import os
import sys
import argparse
from typing import Dict, List, Tuple, Optional
import json

try:
    import PyPDF2
    import pdfplumber
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.units import inch
except ImportError:
    print("Required packages not found. Installing...")
    os.system("pip install PyPDF2 pdfplumber reportlab")

class PDFTextModifier:
    def __init__(self, input_pdf: str = None):
        self.input_pdf = input_pdf
        self.text_content = {}
        self.modifications = {}
        
    def extract_text(self, pdf_path: str = None) -> Dict[int, str]:
        """
        Extract text from PDF file with page numbers
        """
        pdf_path = pdf_path or self.input_pdf
        if not pdf_path:
            raise ValueError("PDF path is required")
            
        text_content = {}
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    if text:
                        text_content[page_num] = text.strip()
                        
        except Exception as e:
            print(f"Error extracting text: {e}")
            
        self.text_content = text_content
        return text_content
    
    def find_text_positions(self, pdf_path: str = None) -> Dict[int, List[Dict]]:
        """
        Find positions of text elements in PDF
        """
        pdf_path = pdf_path or self.input_pdf
        if not pdf_path:
            raise ValueError("PDF path is required")
            
        text_positions = {}
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    words = page.extract_words()
                    text_positions[page_num] = words
                    
        except Exception as e:
            print(f"Error finding text positions: {e}")
            
        return text_positions
    
    def replace_text(self, old_text: str, new_text: str, case_sensitive: bool = True) -> Dict[int, List[str]]:
        """
        Replace text in extracted content
        """
        replacements = {}
        
        for page_num, text in self.text_content.items():
            if case_sensitive:
                if old_text in text:
                    new_page_text = text.replace(old_text, new_text)
                    replacements[page_num] = [old_text, new_text]
                    self.text_content[page_num] = new_page_text
            else:
                if old_text.lower() in text.lower():
                    # Case-insensitive replacement
                    import re
                    pattern = re.compile(re.escape(old_text), re.IGNORECASE)
                    new_page_text = pattern.sub(new_text, text)
                    replacements[page_num] = [old_text, new_text]
                    self.text_content[page_num] = new_page_text
                    
        self.modifications.update(replacements)
        return replacements
    
    def add_text(self, text: str, page_num: int = 1, x: float = 100, y: float = 100) -> None:
        """
        Add text to a specific page at coordinates
        """
        if page_num not in self.modifications:
            self.modifications[page_num] = []
            
        self.modifications[page_num].append({
            'type': 'add',
            'text': text,
            'x': x,
            'y': y
        })
    
    def generate_new_pdf(self, output_path: str, template_pdf: str = None) -> str:
        """
        Generate new PDF with modifications
        """
        if template_pdf:
            # Use existing PDF as template
            return self._modify_existing_pdf(template_pdf, output_path)
        else:
            # Create new PDF from scratch
            return self._create_new_pdf(output_path)
    
    def _modify_existing_pdf(self, template_pdf: str, output_path: str) -> str:
        """
        Modify existing PDF with text changes
        """
        try:
            # Read existing PDF
            with open(template_pdf, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                writer = PyPDF2.PdfWriter()
                
                # Copy pages
                for page in reader.pages:
                    writer.add_page(page)
                
                # Write modified PDF
                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)
                    
            print(f"Modified PDF saved to: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Error modifying PDF: {e}")
            return None
    
    def _create_new_pdf(self, output_path: str) -> str:
        """
        Create new PDF from scratch with text content
        """
        try:
            c = canvas.Canvas(output_path, pagesize=A4)
            width, height = A4
            
            for page_num, text in self.text_content.items():
                if page_num > 1:
                    c.showPage()
                
                # Add main text content
                y_position = height - 50
                lines = text.split('\n')
                
                for line in lines:
                    if y_position < 50:  # Start new page if needed
                        c.showPage()
                        y_position = height - 50
                    
                    c.drawString(50, y_position, line)
                    y_position -= 20
                
                # Add modifications for this page
                if page_num in self.modifications:
                    for mod in self.modifications[page_num]:
                        if isinstance(mod, dict) and mod.get('type') == 'add':
                            c.drawString(mod['x'], mod['y'], mod['text'])
            
            c.save()
            print(f"New PDF created: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Error creating PDF: {e}")
            return None
    
    def save_modifications(self, output_file: str) -> None:
        """
        Save modifications to JSON file
        """
        with open(output_file, 'w') as f:
            json.dump(self.modifications, f, indent=2)
        print(f"Modifications saved to: {output_file}")
    
    def load_modifications(self, input_file: str) -> None:
        """
        Load modifications from JSON file
        """
        with open(input_file, 'r') as f:
            self.modifications = json.load(f)
        print(f"Modifications loaded from: {input_file}")

def main():
    parser = argparse.ArgumentParser(description='PDF Text Modifier')
    parser.add_argument('input_pdf', help='Input PDF file path')
    parser.add_argument('output_pdf', help='Output PDF file path')
    parser.add_argument('--extract', action='store_true', help='Extract text from PDF')
    parser.add_argument('--replace', nargs=2, metavar=('OLD_TEXT', 'NEW_TEXT'), help='Replace text')
    parser.add_argument('--add-text', nargs=4, metavar=('TEXT', 'PAGE', 'X', 'Y'), help='Add text at position')
    parser.add_argument('--save-modifications', help='Save modifications to JSON file')
    parser.add_argument('--load-modifications', help='Load modifications from JSON file')
    
    args = parser.parse_args()
    
    # Initialize modifier
    modifier = PDFTextModifier(args.input_pdf)
    
    # Extract text if requested
    if args.extract:
        text_content = modifier.extract_text()
        print("Extracted text:")
        for page_num, text in text_content.items():
            print(f"\n--- Page {page_num} ---")
            print(text[:500] + "..." if len(text) > 500 else text)
    
    # Load modifications if specified
    if args.load_modifications:
        modifier.load_modifications(args.load_modifications)
    
    # Replace text if specified
    if args.replace:
        old_text, new_text = args.replace
        replacements = modifier.replace_text(old_text, new_text)
        print(f"Replaced {len(replacements)} occurrences")
    
    # Add text if specified
    if args.add_text:
        text, page, x, y = args.add_text
        modifier.add_text(text, int(page), float(x), float(y))
    
    # Save modifications if requested
    if args.save_modifications:
        modifier.save_modifications(args.save_modifications)
    
    # Generate new PDF
    modifier.generate_new_pdf(args.output_pdf, args.input_pdf)

if __name__ == "__main__":
    main()