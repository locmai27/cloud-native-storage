// frontend/src/components/StorageStats/index.js
import React from 'react';
import { formatBytes } from '../../utils/formatters';
import './StorageStats.css';

const StorageStats = ({ stats }) => {
    const usagePercentage = (stats.usedStorage / stats.totalStorage) * 100 || 0;

    return (
        <div className="storage-stats">
            <h3>Storage Statistics</h3>
            <div className="stats-container">
                <div className="stat-item">
                    <label>Used Storage</label>
                    <span>{formatBytes(stats.usedStorage || 0)}</span>
                </div>
                <div className="stat-item">
                    <label>Total Storage</label>
                    <span>{formatBytes(stats.totalStorage || 0)}</span>
                </div>
                <div className="usage-bar">
                    <div 
                        className="usage-fill" 
                        style={{ width: `${usagePercentage}%` }}
                    />
                </div>
            </div>
        </div>
    );
};

export default StorageStats;  // Changed to default export
