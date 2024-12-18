// frontend/src/components/FileList/index.js
import React from 'react';
import { formatBytes, formatDate } from '../../utils/formatters';
import './FileList.css';

const getFileIcon = (contentType) => {
    // Basic file type icons
    switch (contentType) {
        case 'image/jpeg':
        case 'image/png':
        case 'image/gif':
            return '📷';
        case 'application/pdf':
            return '📄';
        case 'video/mp4':
        case 'video/quicktime':
            return '🎥';
        case 'audio/mpeg':
        case 'audio/wav':
            return '🎵';
        default:
            return '📁';
    }
};

export const FileList = ({ files, onFileSelect }) => {
    return (
        <div className="file-list">
            <h2>Uploaded Files</h2>
            <div className="file-grid">
                {files.map((file) => (
                    <div 
                        key={file.fileId} 
                        className="file-item"
                        onClick={() => onFileSelect(file)}
                    >
                        <div className="file-icon">
                            {getFileIcon(file.contentType)}
                        </div>
                        <div className="file-info">
                            <span className="file-name">{file.originalName}</span>
                            <span className="file-size">{formatBytes(file.size)}</span>
                            <span className="file-date">
                                {formatDate(file.createdAt)}
                            </span>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};
