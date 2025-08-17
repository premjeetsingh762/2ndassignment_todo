#!/usr/bin/env python3
"""
Example usage of the PDF Text Modifier tool
This script demonstrates various ways to modify PDF text content
"""

import os
import sys
from pdf_text_modifier import PDFTextModifier

def example_1_basic_text_replacement():
    """Example 1: Basic text replacement in a PDF."""
    print("=== Example 1: Basic Text Replacement ===")
    
    # Create sample PDF first
    print("Creating sample PDF...")
    os.system("python3 create_sample_pdf.py")
    
    # Initialize the modifier
    modifier = PDFTextModifier()
    
    # Define text modifications
    modifications = {
        "Acme Corporation": "TechCorp Industries",
        "Widget 3000": "SuperWidget Pro",
        "$299.99": "$399.99",
        "123 Main Street": "456 Innovation Drive",
        "Made in USA": "Made in Canada"
    }
    
    # Process the PDF
    input_pdf = "sample.pdf"
    output_pdf = "sample_modified_basic.pdf"
    
    print(f"Processing {input_pdf}...")
    success = modifier.process_pdf(input_pdf, output_pdf, modifications)
    
    if success:
        print(f"✅ Basic modification complete! Check: {output_pdf}")
    else:
        print("❌ Basic modification failed!")
    
    return success

def example_2_advanced_modifications():
    """Example 2: More advanced text modifications."""
    print("\n=== Example 2: Advanced Text Modifications ===")
    
    modifier = PDFTextModifier()
    
    # More complex modifications
    modifications = {
        "Sample Document for PDF Text Modification": "Professional Business Proposal",
        "This is a sample PDF document created for testing the PDF text modification tool.": 
        "This document presents our comprehensive business solution for your organization.",
        "Company Information": "About Our Organization",
        "Product Description": "Solution Overview", 
        "Customer Testimonials": "Client Success Stories",
        "Technical Specifications": "Product Details",
        "testing purposes": "business presentation purposes"
    }
    
    input_pdf = "sample.pdf"
    output_pdf = "sample_modified_advanced.pdf"
    
    print(f"Processing {input_pdf} with advanced modifications...")
    success = modifier.process_pdf(input_pdf, output_pdf, modifications)
    
    if success:
        print(f"✅ Advanced modification complete! Check: {output_pdf}")
    else:
        print("❌ Advanced modification failed!")
    
    return success

def example_3_command_line_usage():
    """Example 3: Command line usage examples."""
    print("\n=== Example 3: Command Line Usage Examples ===")
    
    print("Here are some command line usage examples:")
    print("\n1. Interactive mode:")
    print("   python3 pdf_text_modifier.py --interactive")
    
    print("\n2. Simple replacement:")
    print('   python3 pdf_text_modifier.py sample.pdf output.pdf --find "Acme Corporation" --replace "TechCorp"')
    
    print("\n3. Multiple replacements:")
    print('   python3 pdf_text_modifier.py sample.pdf output.pdf \\')
    print('       --find "Widget 3000" --replace "SuperWidget" \\')
    print('       --find "$299.99" --replace "$399.99"')
    
    print("\n4. Force OCR mode:")
    print("   python3 pdf_text_modifier.py image_based.pdf output.pdf --ocr --find 'old' --replace 'new'")

def example_4_ocr_demonstration():
    """Example 4: OCR functionality demonstration."""
    print("\n=== Example 4: OCR Functionality ===")
    
    print("For OCR demonstration, you would need a PDF with images containing text.")
    print("The tool automatically detects when OCR is needed and switches to image processing mode.")
    print("OCR is particularly useful for:")
    print("- Scanned documents")
    print("- PDFs created from images")
    print("- Documents where text is embedded as images")

def demonstrate_text_extraction():
    """Demonstrate text extraction without modification."""
    print("\n=== Text Extraction Demo ===")
    
    if not os.path.exists("sample.pdf"):
        print("Creating sample PDF first...")
        os.system("python3 create_sample_pdf.py")
    
    modifier = PDFTextModifier()
    
    print("Extracting text from sample.pdf...")
    text = modifier.extract_text_from_pdf("sample.pdf")
    
    print(f"\nExtracted {len(text)} characters:")
    print("-" * 50)
    print(text[:800] + ("..." if len(text) > 800 else ""))
    print("-" * 50)

def main():
    """Run all examples."""
    print("PDF Text Modifier - Usage Examples")
    print("=" * 50)
    
    # Activate virtual environment for examples
    activate_cmd = "source pdf_env/bin/activate && "
    
    # Run text extraction demo
    demonstrate_text_extraction()
    
    # Run examples
    try:
        example_1_basic_text_replacement()
        example_2_advanced_modifications()
        example_3_command_line_usage()
        example_4_ocr_demonstration()
        
        print("\n" + "=" * 50)
        print("✅ All examples completed successfully!")
        print("\nGenerated files:")
        for filename in ["sample.pdf", "sample_modified_basic.pdf", "sample_modified_advanced.pdf"]:
            if os.path.exists(filename):
                print(f"  - {filename}")
        
        print("\nTo run the tool interactively:")
        print("  source pdf_env/bin/activate")
        print("  python3 pdf_text_modifier.py --interactive")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")

if __name__ == "__main__":
    main()