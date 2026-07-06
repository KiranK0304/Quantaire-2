import React from 'react';

export const LoadingSpinner: React.FC = () => {
  return (
    <div className="loading-container">
      <div className="loading-spinner"></div>
      <p className="loading-text">Initializing scan parameters...</p>
      <p className="loading-sub">This may take ~10-15 seconds.</p>
    </div>
  );
};
