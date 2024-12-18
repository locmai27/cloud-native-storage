// frontend/src/App.js
import React, { useState, useEffect } from 'react';
import { FileUpload } from './components/FileUpload';
import { FileList } from './components/FileList';
import StorageStats from './components/StorageStats'; // This is correct
import { getFiles } from './services/api';
import './App.css';

const App = () => {
    const [files, setFiles] = useState([]);
    const [stats, setStats] = useState({
        usedStorage: 0,
        totalStorage: 0
    });

    // useEffect(() => {
    //     loadFiles();
    // }, []);

    const loadFiles = async () => {
        try {
            const data = await getFiles();
            setFiles(data.files);
            setStats(data.stats);
        } catch (error) {
            console.error('Failed to load files:', error);
        }
    };

    const handleUploadComplete = (result) => {
        loadFiles();
    };

    const handleFileSelect = async (file) => {
        // Handle file selection/preview
    };

    return (
        <div className="app">
            <header className="app-header">
                <h1>Elastic Large Media Storage</h1>
                <StorageStats stats={stats} />
            </header>
            
            <main className="app-main">
                <FileUpload onUploadComplete={handleUploadComplete} />
                <FileList 
                    files={files} 
                    onFileSelect={handleFileSelect} 
                />
            </main>
        </div>
    );

}

export default App;
