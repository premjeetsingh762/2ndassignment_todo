#!/usr/bin/env python3
"""
Create a sample PDF file for testing the PDF text modifier
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def create_sample_pdf():
    """Create a sample PDF with various text content for testing"""
    
    # Create the PDF
    c = canvas.Canvas("sample.pdf", pagesize=A4)
    width, height = A4
    
    # Page 1
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 50, "Sample PDF Document")
    
    c.setFont("Helvetica", 14)
    c.drawString(50, height - 100, "This is a sample PDF file created for testing the PDF text modifier.")
    c.drawString(50, height - 130, "It contains various types of text that can be modified.")
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 180, "Page 1 Content:")
    
    c.setFont("Helvetica", 12)
    lines = [
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.",
        "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum.",
        "",
        "This text can be replaced: OLD_TEXT_HERE",
        "Another replaceable text: ANOTHER_OLD_TEXT",
        "",
        "Contact Information:",
        "Email: old.email@example.com",
        "Phone: (555) 123-4567",
        "Address: 123 Old Street, Old City, OC 12345"
    ]
    
    y_position = height - 220
    for line in lines:
        c.drawString(50, y_position, line)
        y_position -= 20
    
    # Page 2
    c.showPage()
    
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 50, "Page 2 - Additional Content")
    
    c.setFont("Helvetica", 12)
    lines_page2 = [
        "This is the second page of our sample PDF.",
        "It contains more text that can be modified or replaced.",
        "",
        "Product Information:",
        "Product Name: Old Product Name",
        "Price: $99.99",
        "Description: This is an old product description that needs updating.",
        "",
        "Company Details:",
        "Company: Old Company Name",
        "Founded: 1990",
        "Industry: Technology",
        "",
        "This text should be replaced: REPLACE_ME",
        "And this one too: ANOTHER_REPLACEMENT"
    ]
    
    y_position = height - 100
    for line in lines_page2:
        c.drawString(50, y_position, line)
        y_position -= 20
    
    # Page 3
    c.showPage()
    
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 50, "Page 3 - Final Content")
    
    c.setFont("Helvetica", 12)
    lines_page3 = [
        "This is the final page of our sample document.",
        "It demonstrates various text patterns that can be modified.",
        "",
        "Summary:",
        "Total pages: 3",
        "Total words: Multiple",
        "Purpose: Testing PDF text modification",
        "",
        "Test patterns:",
        "Pattern 1: test_pattern_1",
        "Pattern 2: test_pattern_2",
        "Pattern 3: test_pattern_3",
        "",
        "End of document."
    ]
    
    y_position = height - 100
    for line in lines_page3:
        c.drawString(50, y_position, line)
        y_position -= 20
    
    # Save the PDF
    c.save()
    print("Sample PDF created: sample.pdf")
    print("This file can be used to test the PDF text modifier functionality.")

if __name__ == "__main__":
    create_sample_pdf()