#!/usr/bin/env python3
"""
Create a sample PDF for testing the PDF text modifier
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch

def create_sample_pdf(filename="sample.pdf"):
    """Create a sample PDF with various text content."""
    
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    
    story = []
    
    # Title
    title = Paragraph("Sample Document for PDF Text Modification", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 0.3*inch))
    
    # Introduction
    intro = """This is a sample PDF document created for testing the PDF text modification tool. 
    This document contains various types of text that you can practice modifying."""
    story.append(Paragraph(intro, styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Sample content sections
    sections = [
        {
            "title": "Company Information",
            "content": """Company Name: Acme Corporation
Address: 123 Main Street, Anytown, State 12345
Phone: (555) 123-4567
Email: info@acme.com
Website: www.acme.com"""
        },
        {
            "title": "Product Description", 
            "content": """Our flagship product is the Widget 3000, a revolutionary device that 
transforms the way businesses operate. The Widget 3000 offers unprecedented efficiency 
and reliability at an affordable price point of $299.99."""
        },
        {
            "title": "Customer Testimonials",
            "content": """"The Widget 3000 has completely changed our workflow!" - John Smith, CEO
"Amazing product, highly recommended!" - Sarah Johnson, Manager
"Best investment we've made this year." - Mike Davis, Director"""
        },
        {
            "title": "Technical Specifications",
            "content": """Model: Widget 3000
Dimensions: 10" x 8" x 6"
Weight: 2.5 lbs
Power: 120V AC
Warranty: 2 years
Manufactured: Made in USA"""
        }
    ]
    
    for section in sections:
        # Section title
        story.append(Paragraph(section["title"], styles['Heading2']))
        story.append(Spacer(1, 0.1*inch))
        
        # Section content
        story.append(Paragraph(section["content"], styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
    
    # Footer
    footer = """This document was generated automatically for testing purposes. 
You can modify any text in this document using the PDF text modification tool."""
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph(footer, styles['Normal']))
    
    # Build the PDF
    doc.build(story)
    print(f"Sample PDF created: {filename}")

if __name__ == "__main__":
    create_sample_pdf()