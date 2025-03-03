import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  // State variables for the file, upload progress, file list, and messages.
  const [file, setFile] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [filesList, setFilesList] = useState([]);
  const [message, setMessage] = useState('');

  // Optionally, set the base URL for your API (change it as needed)
  axios.defaults.baseURL = 'http://localhost:5001';

  // Fetch the list of uploaded files from the backend
  const fetchFiles = async () => {
    try {
      const response = await axios.get('/files');
      setFilesList(response.data);
    } catch (error) {
      console.error('Error fetching files:', error);
      setMessage('Error fetching files.');
    }
  };

  useEffect(() => {
    // Load the file list when the component mounts
    fetchFiles();
  }, []);

  // Handle file selection from the input
  const handleFileChange = (e) => {
    if (e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  // Handle the file upload process
  const handleUpload = async () => {
    if (!file) {
      setMessage('Please select a file first.');
      return;
    }
    setMessage('');
    setUploadProgress(0);

    try {
      // Step 1: Request a pre-signed URL from the backend
      const presignRes = await axios.post('/files/presign', {
        filename: file.name,
        contentType: file.type,
      });
      const { uploadUrl, key } = presignRes.data;

      // Step 2: Upload the file directly to S3 using the pre-signed URL
      await axios.put(uploadUrl, file, {
        headers: {
          'Content-Type': file.type,
        },
        onUploadProgress: (progressEvent) => {
          if (progressEvent.total) {
            const percentCompleted = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
            setUploadProgress(percentCompleted);
          }
        },
      });

      // Step 3: Notify the backend to save file metadata
      await axios.post('/files/metadata', { filename: file.name, key });
      
      setMessage('Upload successful!');
      setFile(null);
      setUploadProgress(0);
      fetchFiles();
    } catch (error) {
      console.error('Upload error:', error);
      setMessage('Upload failed. Check console for details.');
      setUploadProgress(0);
    }
  };

  // Handle file download by requesting a pre-signed GET URL
  const handleDownload = async (fileKey) => {
    try {
      const res = await axios.get(`/files/${fileKey}/download`);
      const { url } = res.data;
      window.open(url, '_blank');
    } catch (error) {
      console.error('Download error:', error);
      setMessage('Download failed.');
    }
  };

  return (
    <div style={{ margin: '20px' }}>
      <h1>Cloud Storage App</h1>
      <div>
        <h2>Upload File</h2>
        <input type="file" onChange={handleFileChange} />
        <button onClick={handleUpload} style={{ marginLeft: '10px' }}>
          Upload
        </button>
        {uploadProgress > 0 && (
          <p>Uploading: {uploadProgress}%</p>
        )}
      </div>
      <div>
        <h2>Uploaded Files</h2>
        {filesList.length === 0 ? (
          <p>No files uploaded yet.</p>
        ) : (
          <ul>
            {filesList.map((item) => (
              <li key={item.FileKey}>
                <strong>{item.FileName}</strong> (Uploaded at{' '}
                {new Date(item.UploadTime * 1000).toLocaleString()})
                <button
                  onClick={() => handleDownload(item.FileKey)}
                  style={{ marginLeft: '10px' }}
                >
                  Download
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
      {message && <p>{message}</p>}
    </div>
  );
}

export default App;
