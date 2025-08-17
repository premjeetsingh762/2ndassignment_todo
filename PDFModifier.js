import React, { useState, useRef } from 'react';
import './PDFModifier.css';

const PDFModifier = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [extractedText, setExtractedText] = useState({});
  const [modifications, setModifications] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [outputMessage, setOutputMessage] = useState('');
  const fileInputRef = useRef(null);

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file);
      setOutputMessage('');
    } else {
      setOutputMessage('Please select a valid PDF file.');
    }
  };

  const extractTextFromPDF = async () => {
    if (!selectedFile) {
      setOutputMessage('Please select a PDF file first.');
      return;
    }

    setIsProcessing(true);
    setOutputMessage('Extracting text from PDF...');

    try {
      const formData = new FormData();
      formData.append('pdf', selectedFile);

      const response = await fetch('/api/extract-text', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setExtractedText(data.textContent);
        setOutputMessage('Text extracted successfully!');
      } else {
        setOutputMessage('Error extracting text from PDF.');
      }
    } catch (error) {
      setOutputMessage('Error: ' + error.message);
    } finally {
      setIsProcessing(false);
    }
  };

  const addModification = () => {
    const newMod = {
      id: Date.now(),
      type: 'replace',
      oldText: '',
      newText: '',
      page: 1
    };
    setModifications([...modifications, newMod]);
  };

  const updateModification = (id, field, value) => {
    setModifications(modifications.map(mod => 
      mod.id === id ? { ...mod, [field]: value } : mod
    ));
  };

  const removeModification = (id) => {
    setModifications(modifications.filter(mod => mod.id !== id));
  };

  const generateModifiedPDF = async () => {
    if (!selectedFile || modifications.length === 0) {
      setOutputMessage('Please select a PDF file and add modifications.');
      return;
    }

    setIsProcessing(true);
    setOutputMessage('Generating modified PDF...');

    try {
      const formData = new FormData();
      formData.append('pdf', selectedFile);
      formData.append('modifications', JSON.stringify(modifications));

      const response = await fetch('/api/generate-pdf', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'modified_' + selectedFile.name;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        setOutputMessage('Modified PDF generated and downloaded successfully!');
      } else {
        setOutputMessage('Error generating modified PDF.');
      }
    } catch (error) {
      setOutputMessage('Error: ' + error.message);
    } finally {
      setIsProcessing(false);
    }
  };

  const addTextModification = () => {
    const newMod = {
      id: Date.now(),
      type: 'add',
      text: '',
      page: 1,
      x: 100,
      y: 100
    };
    setModifications([...modifications, newMod]);
  };

  return (
    <div className="pdf-modifier">
      <h2>PDF Text Modifier</h2>
      
      <div className="file-upload-section">
        <input
          type="file"
          accept=".pdf"
          onChange={handleFileSelect}
          ref={fileInputRef}
          style={{ display: 'none' }}
        />
        <button 
          onClick={() => fileInputRef.current.click()}
          className="upload-btn"
        >
          Select PDF File
        </button>
        {selectedFile && (
          <span className="file-name">{selectedFile.name}</span>
        )}
      </div>

      {selectedFile && (
        <div className="actions-section">
          <button 
            onClick={extractTextFromPDF}
            disabled={isProcessing}
            className="action-btn"
          >
            Extract Text
          </button>
        </div>
      )}

      {Object.keys(extractedText).length > 0 && (
        <div className="text-preview">
          <h3>Extracted Text Preview</h3>
          {Object.entries(extractedText).map(([pageNum, text]) => (
            <div key={pageNum} className="page-text">
              <h4>Page {pageNum}</h4>
              <div className="text-content">
                {text.length > 300 ? text.substring(0, 300) + '...' : text}
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="modifications-section">
        <h3>Text Modifications</h3>
        <div className="modification-buttons">
          <button onClick={addModification} className="mod-btn">
            Add Text Replacement
          </button>
          <button onClick={addTextModification} className="mod-btn">
            Add New Text
          </button>
        </div>

        {modifications.map((mod) => (
          <div key={mod.id} className="modification-item">
            <div className="mod-header">
              <span className="mod-type">{mod.type === 'replace' ? 'Text Replacement' : 'Add Text'}</span>
              <button 
                onClick={() => removeModification(mod.id)}
                className="remove-btn"
              >
                ×
              </button>
            </div>

            {mod.type === 'replace' ? (
              <div className="mod-fields">
                <div className="field-group">
                  <label>Page:</label>
                  <input
                    type="number"
                    value={mod.page}
                    onChange={(e) => updateModification(mod.id, 'page', parseInt(e.target.value))}
                    min="1"
                  />
                </div>
                <div className="field-group">
                  <label>Old Text:</label>
                  <input
                    type="text"
                    value={mod.oldText}
                    onChange={(e) => updateModification(mod.id, 'oldText', e.target.value)}
                    placeholder="Text to replace"
                  />
                </div>
                <div className="field-group">
                  <label>New Text:</label>
                  <input
                    type="text"
                    value={mod.newText}
                    onChange={(e) => updateModification(mod.id, 'newText', e.target.value)}
                    placeholder="Replacement text"
                  />
                </div>
              </div>
            ) : (
              <div className="mod-fields">
                <div className="field-group">
                  <label>Page:</label>
                  <input
                    type="number"
                    value={mod.page}
                    onChange={(e) => updateModification(mod.id, 'page', parseInt(e.target.value))}
                    min="1"
                  />
                </div>
                <div className="field-group">
                  <label>Text:</label>
                  <input
                    type="text"
                    value={mod.text}
                    onChange={(e) => updateModification(mod.id, 'text', e.target.value)}
                    placeholder="Text to add"
                  />
                </div>
                <div className="field-group">
                  <label>X Position:</label>
                  <input
                    type="number"
                    value={mod.x}
                    onChange={(e) => updateModification(mod.id, 'x', parseFloat(e.target.value))}
                  />
                </div>
                <div className="field-group">
                  <label>Y Position:</label>
                  <input
                    type="number"
                    value={mod.y}
                    onChange={(e) => updateModification(mod.id, 'y', parseFloat(e.target.value))}
                  />
                </div>
              </div>
            )}
          </div>
        ))}

        {modifications.length > 0 && (
          <button 
            onClick={generateModifiedPDF}
            disabled={isProcessing}
            className="generate-btn"
          >
            {isProcessing ? 'Generating...' : 'Generate Modified PDF'}
          </button>
        )}
      </div>

      {outputMessage && (
        <div className={`output-message ${outputMessage.includes('Error') ? 'error' : 'success'}`}>
          {outputMessage}
        </div>
      )}
    </div>
  );
};

export default PDFModifier;