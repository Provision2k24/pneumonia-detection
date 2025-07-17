import React, { useState } from 'react';
import './App.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUpload } from '@fortawesome/free-solid-svg-icons';

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState(false);
  const [previewUrl, setPreviewUrl] = useState(null);

  const handleUpload = (e) => {
    const uploadedFile = e.target.files[0];
    if (uploadedFile) {
      setFile(uploadedFile);
      setToast(true);
      setPreviewUrl(URL.createObjectURL(uploadedFile));
      setTimeout(() => setToast(false), 3000);
    }
  };

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:5000/api/analyze', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="main-frame">
      {toast && <div className="toast">Upload Success ✅</div>}

      {!result ? (
        <div className="card">
          <h2 className="title">AI Pneumonia Detector</h2>
          <label htmlFor="file-upload" className="upload-label">
            <FontAwesomeIcon icon={faUpload} className="upload-icon" />
            <span>Click to Upload X-ray Image</span>
          </label>
          <input
            type="file"
            id="file-upload"
            accept="image/*"
            onChange={handleUpload}
            style={{ display: 'none' }}
          />
          {file && (
            <button className="analyze-btn" onClick={handleAnalyze} disabled={loading}>
              {loading ? 'Analyzing...' : 'Analyze'}
            </button>
          )}
        </div>
      ) : (
        <div className="card result-card">
          <h2 className="result-title">Prediction Result</h2>
          <div className="result-body">
            <div className="result-info">
              <p><strong>Diagnosis:</strong> {result.diagnosis}</p>
              <p><strong>Confidence:</strong> {result.confidence.toFixed(2)}%</p>
            </div>
            <div className="result-image">
              <img src={previewUrl} alt="Uploaded X-ray" />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
