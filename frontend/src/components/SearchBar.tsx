import React, { useState } from 'react';

interface SearchBarProps {
  onAction: (ticker: string, action: 'analyze' | 'details') => void;
  isLoading?: boolean;
}

export const SearchBar: React.FC<SearchBarProps> = ({ onAction, isLoading = false }) => {
  const [ticker, setTicker] = useState('');
  const [market, setMarket] = useState('IN'); // Default to India

  const handleAction = (action: 'analyze' | 'details') => {
    if (ticker.trim() && !isLoading) {
      const baseTicker = ticker.trim().toUpperCase();
      const suffix = market === 'IN' ? '.NS' : '';
      const finalTicker = (suffix && !baseTicker.endsWith(suffix))
        ? `${baseTicker}${suffix}`
        : baseTicker;
      onAction(finalTicker, action);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    handleAction('analyze');
  };

  return (
    <form onSubmit={handleSubmit} className="search-form">
      <div className="region-selector">
        <span className="region-label">COUNTRY:</span>
        <select
          value={market}
          onChange={(e) => setMarket(e.target.value)}
          className="region-select"
          disabled={isLoading}
        >
          <option value="IN">INDIA</option>
          <option value="US">UNITED STATES</option>
          <option value="OTHER">OTHER</option>
        </select>
      </div>
      <div className="input-wrap">
        <span className="ticker-icon">▸</span>
        <input
          type="text"
          value={ticker}
          onChange={(e) => setTicker(e.target.value)}
          placeholder="e.g. RELIANCE, TCS, AAPL"
          disabled={isLoading}
          autoComplete="off"
        />
        <button 
          type="button" 
          className="btn" 
          onClick={() => handleAction('analyze')}
          disabled={!ticker.trim() || isLoading}
        >
          {isLoading ? 'SCANNING...' : 'ANALYZE'}
        </button>
      </div>
      
      <div style={{ display: 'flex', justifyContent: 'center', marginTop: '8px' }}>
        <button 
          type="button" 
          className="btn" 
          onClick={() => handleAction('details')}
          disabled={!ticker.trim() || isLoading}
          style={{ 
            backgroundColor: 'transparent', 
            border: '1px solid var(--border-light)', 
            color: 'var(--text-secondary)',
            fontSize: '14px',
            padding: '8px 16px',
            borderRadius: 'var(--radius)',
            height: 'auto'
          }}
        >
          GET STOCK DETAILS
        </button>
      </div>
    </form>
  );
};
