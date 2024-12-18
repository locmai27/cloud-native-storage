// frontend/src/components/FileUpload/index.js
import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { uploadFile } from '../../services/api';
import { formatBytes } from '../../utils/formatters';
import './FileUpload.css';

export const FileUpload = ({ onUploadComplete }) => {
    const [uploadProgress, setUploadProgress] = useState(0);
    const [isUploading, setIsUploading] = useState(false);

    const onDrop = useCallback(async (acceptedFiles) => {
        const file = acceptedFiles[0];
        setIsUploading(true);
        
        try {
            const result = await uploadFile(file, (progress) => {
                setUploadProgress(progress);
            });
            onUploadComplete(result);
        } catch (error) {
            console.error('Upload failed:', error);
        } finally {
            setIsUploading(false);
            setUploadProgress(0);
        }
    }, [onUploadComplete]);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        maxFiles: 1
    });

    return (
        <div className="upload-container">
            <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''}`}>
                <input {...getInputProps()} />
                {isUploading ? (
                    <div className="progress-container">
                        <progress value={uploadProgress} max="100" />
                        <span>{uploadProgress}%</span>
                    </div>
                ) : (
                    <p>Drag & drop a file here, or click to select</p>
                )}
            </div>
        </div>
    );
};
