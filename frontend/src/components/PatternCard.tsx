import React from 'react';
import type { PatternDetection } from '../services/api';

interface PatternCardProps {
  pattern: PatternDetection;
}

export const PatternCard: React.FC<PatternCardProps> = ({ pattern }) => {
  return (
    <div className="detection-card">
      <div className="detection-header">
        <span className="detection-name">{pattern.name.replace('_', ' ').toUpperCase()}</span>
        <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
          <span className="meta-label" style={{ fontSize: '13px' }}>CONF</span>
          <span className="badge badge-detected">{Math.round(pattern.confidence * 100)}%</span>
        </div>
      </div>
      <div className="detection-body">
        <p className="detection-desc">{pattern.description}</p>
        
        <div className="pattern-data-grid">
           <div className="data-cell">
             <span className="data-label">TYPE</span>
             <span className="data-value">{pattern.name}</span>
           </div>
           <div className="data-cell">
             <span className="data-label">CLASS ID</span>
             <span className="data-value">{pattern.annotations?.class_id ?? 'N/A'}</span>
           </div>
           <div className="data-cell">
             <span className="data-label">STATUS</span>
             <span className="data-value" style={{ color: 'var(--accent)' }}>VERIFIED</span>
           </div>
        </div>
      </div>
    </div>
  );
};
