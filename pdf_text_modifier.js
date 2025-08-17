#!/usr/bin/env node
/**
 * PDF Text Modifier - Node.js version
 * A comprehensive tool for modifying text in PDF files
 */

const fs = require('fs');
const path = require('path');

// Check if required packages are installed
const requiredPackages = ['pdf-lib', 'pdf-parse'];
let missingPackages = [];

requiredPackages.forEach(pkg => {
    try {
        require(pkg);
    } catch (e) {
        missingPackages.push(pkg);
    }
});

if (missingPackages.length > 0) {
    console.log(`Installing missing packages: ${missingPackages.join(', ')}`);
    const { execSync } = require('child_process');
    execSync(`npm install ${missingPackages.join(' ')}`, { stdio: 'inherit' });
}

const { PDFDocument, PDFPage, rgb } = require('pdf-lib');
const pdfParse = require('pdf-parse');

class PDFTextModifier {
    constructor(inputPdf = null) {
        this.inputPdf = inputPdf;
        this.textContent = {};
        this.modifications = {};
        this.pdfBytes = null;
    }

    async loadPDF(pdfPath) {
        try {
            this.pdfBytes = fs.readFileSync(pdfPath);
            this.inputPdf = pdfPath;
            return true;
        } catch (error) {
            console.error('Error loading PDF:', error.message);
            return false;
        }
    }

    async extractText(pdfPath = null) {
        const targetPath = pdfPath || this.inputPdf;
        if (!targetPath) {
            throw new Error('PDF path is required');
        }

        try {
            const dataBuffer = fs.readFileSync(targetPath);
            const data = await pdfParse(dataBuffer);
            
            // Split text by pages (approximate)
            const pages = data.text.split('\n\n');
            pages.forEach((pageText, index) => {
                if (pageText.trim()) {
                    this.textContent[index + 1] = pageText.trim();
                }
            });

            return this.textContent;
        } catch (error) {
            console.error('Error extracting text:', error.message);
            return {};
        }
    }

    replaceText(oldText, newText, caseSensitive = true) {
        const replacements = {};

        for (const [pageNum, text] of Object.entries(this.textContent)) {
            let newPageText = text;
            let replaced = false;

            if (caseSensitive) {
                if (text.includes(oldText)) {
                    newPageText = text.replace(new RegExp(oldText.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'), newText);
                    replaced = true;
                }
            } else {
                const regex = new RegExp(oldText.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
                if (regex.test(text)) {
                    newPageText = text.replace(regex, newText);
                    replaced = true;
                }
            }

            if (replaced) {
                replacements[pageNum] = [oldText, newText];
                this.textContent[pageNum] = newPageText;
            }
        }

        this.modifications = { ...this.modifications, ...replacements };
        return replacements;
    }

    addText(text, pageNum = 1, x = 100, y = 100) {
        if (!this.modifications[pageNum]) {
            this.modifications[pageNum] = [];
        }

        this.modifications[pageNum].push({
            type: 'add',
            text: text,
            x: x,
            y: y
        });
    }

    async generateNewPDF(outputPath, templatePdf = null) {
        if (templatePdf) {
            return await this.modifyExistingPDF(templatePdf, outputPath);
        } else {
            return await this.createNewPDF(outputPath);
        }
    }

    async modifyExistingPDF(templatePdf, outputPath) {
        try {
            const pdfDoc = await PDFDocument.load(this.pdfBytes);
            const pages = pdfDoc.getPages();

            // Apply modifications to existing pages
            for (const [pageNum, mods] of Object.entries(this.modifications)) {
                const pageIndex = parseInt(pageNum) - 1;
                if (pageIndex < pages.length) {
                    const page = pages[pageIndex];
                    
                    for (const mod of mods) {
                        if (mod.type === 'add') {
                            page.drawText(mod.text, {
                                x: mod.x,
                                y: mod.y,
                                size: 12,
                                color: rgb(0, 0, 0)
                            });
                        }
                    }
                }
            }

            const modifiedPdfBytes = await pdfDoc.save();
            fs.writeFileSync(outputPath, modifiedPdfBytes);
            console.log(`Modified PDF saved to: ${outputPath}`);
            return outputPath;
        } catch (error) {
            console.error('Error modifying PDF:', error.message);
            return null;
        }
    }

    async createNewPDF(outputPath) {
        try {
            const pdfDoc = await PDFDocument.create();
            
            for (const [pageNum, text] of Object.entries(this.textContent)) {
                const page = pdfDoc.addPage([595.28, 841.89]); // A4 size
                const { width, height } = page.getSize();
                
                // Add main text content
                let yPosition = height - 50;
                const lines = text.split('\n');
                
                for (const line of lines) {
                    if (yPosition < 50) {
                        // Start new page if needed
                        const newPage = pdfDoc.addPage([595.28, 841.89]);
                        yPosition = height - 50;
                    }
                    
                    page.drawText(line, {
                        x: 50,
                        y: yPosition,
                        size: 12,
                        color: rgb(0, 0, 0)
                    });
                    yPosition -= 20;
                }
                
                // Add modifications for this page
                if (this.modifications[pageNum]) {
                    for (const mod of this.modifications[pageNum]) {
                        if (mod.type === 'add') {
                            page.drawText(mod.text, {
                                x: mod.x,
                                y: mod.y,
                                size: 12,
                                color: rgb(0, 0, 0)
                            });
                        }
                    }
                }
            }

            const pdfBytes = await pdfDoc.save();
            fs.writeFileSync(outputPath, pdfBytes);
            console.log(`New PDF created: ${outputPath}`);
            return outputPath;
        } catch (error) {
            console.error('Error creating PDF:', error.message);
            return null;
        }
    }

    saveModifications(outputFile) {
        fs.writeFileSync(outputFile, JSON.stringify(this.modifications, null, 2));
        console.log(`Modifications saved to: ${outputFile}`);
    }

    loadModifications(inputFile) {
        this.modifications = JSON.parse(fs.readFileSync(inputFile, 'utf8'));
        console.log(`Modifications loaded from: ${inputFile}`);
    }
}

// Command line interface
async function main() {
    const args = process.argv.slice(2);
    
    if (args.length < 2) {
        console.log(`
Usage: node pdf_text_modifier.js <input_pdf> <output_pdf> [options]

Options:
  --extract                    Extract text from PDF
  --replace <old> <new>        Replace text
  --add-text <text> <page> <x> <y>  Add text at position
  --save-modifications <file>  Save modifications to JSON file
  --load-modifications <file>  Load modifications from JSON file

Examples:
  node pdf_text_modifier.js input.pdf output.pdf --extract
  node pdf_text_modifier.js input.pdf output.pdf --replace "old text" "new text"
  node pdf_text_modifier.js input.pdf output.pdf --add-text "Hello" 1 100 100
        `);
        return;
    }

    const [inputPdf, outputPdf, ...options] = args;
    const modifier = new PDFTextModifier(inputPdf);
    
    // Load PDF
    await modifier.loadPDF(inputPdf);

    // Parse options
    for (let i = 0; i < options.length; i++) {
        const option = options[i];
        
        switch (option) {
            case '--extract':
                const textContent = await modifier.extractText();
                console.log('Extracted text:');
                for (const [pageNum, text] of Object.entries(textContent)) {
                    console.log(`\n--- Page ${pageNum} ---`);
                    console.log(text.length > 500 ? text.substring(0, 500) + '...' : text);
                }
                break;
                
            case '--replace':
                if (i + 2 < options.length) {
                    const oldText = options[i + 1];
                    const newText = options[i + 2];
                    const replacements = modifier.replaceText(oldText, newText);
                    console.log(`Replaced ${Object.keys(replacements).length} occurrences`);
                    i += 2;
                }
                break;
                
            case '--add-text':
                if (i + 4 < options.length) {
                    const text = options[i + 1];
                    const page = parseInt(options[i + 2]);
                    const x = parseFloat(options[i + 3]);
                    const y = parseFloat(options[i + 4]);
                    modifier.addText(text, page, x, y);
                    i += 4;
                }
                break;
                
            case '--save-modifications':
                if (i + 1 < options.length) {
                    modifier.saveModifications(options[i + 1]);
                    i++;
                }
                break;
                
            case '--load-modifications':
                if (i + 1 < options.length) {
                    modifier.loadModifications(options[i + 1]);
                    i++;
                }
                break;
        }
    }

    // Generate new PDF
    await modifier.generateNewPDF(outputPdf, inputPdf);
}

if (require.main === module) {
    main().catch(console.error);
}

module.exports = PDFTextModifier;