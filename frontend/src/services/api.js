// frontend/src/services/api.js
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

export const uploadFile = async (file, onProgress) => {
    // First, get the pre-signed URL
    const response = await axios.post(`${API_BASE_URL}/upload`, {
        fileName: file.name,
        fileSize: file.size,
        contentType: file.type
    });

    // Upload to S3 using pre-signed URL
    await axios.put(response.data.uploadUrl, file, {
        headers: { 'Content-Type': file.type },
        // this is a built-in provided by axios to track the upload progress
        onUploadProgress: (progressEvent) => {
            const percentage = (progressEvent.loaded * 100) / progressEvent.total;
            onProgress(Math.round(percentage));
        }
    });

    return response.data;
};

export const getFiles = async () => {
    const response = await axios.get(`${API_BASE_URL}/files`);
    return response.data;
};

export const getFileUrl = async (fileId) => {
    const response = await axios.get(`${API_BASE_URL}/files/${fileId}/url`);
    return response.data.url;
};
