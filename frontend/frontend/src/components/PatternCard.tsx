import React from 'react';
import type { PatternDetection } from '../services/api';

interface PatternCardProps {
  pattern: PatternDetection;
}

export const PatternCard: React.FC<PatternCardProps> = ({ pattern }) => {
  const isBullish = pattern.name.toLowerCase().includes('bottom');
  const isBearish = pattern.name.toLowerCase().includes('top') || pattern.name === 'M_Head';

  const confidencePercent = Math.round(pattern.confidence * 100);
  const badgeClass = isBullish ? 'badge badge-detected' : isBearish ? 'badge badge-bearish' : 'badge badge-neutral';

  return (
    <div className="detection-card">
      <div className="detection-header">
        <span className="detection-name">{pattern.name}</span>
        <span className={badgeClass}>{confidencePercent}%</span>
      </div>
      <div className="detection-body">
        <p className="detection-desc">{pattern.description || 'Detected technical formation.'}</p>
        {pattern.annotations?.class_id !== undefined && (
          <div className="detection-meta">Class ID: {pattern.annotations.class_id}</div>
        )}
      </div>
    </div>
  );
};
