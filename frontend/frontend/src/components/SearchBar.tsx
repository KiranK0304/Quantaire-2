import React, { useState } from 'react';

interface SearchBarProps {
  onSearch: (ticker: string) => void;
  isLoading?: boolean;
}

export const SearchBar: React.FC<SearchBarProps> = ({ onSearch, isLoading = false }) => {
  const [ticker, setTicker] = useState('');
  const [market, setMarket] = useState('IN'); // Default to India

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (ticker.trim() && !isLoading) {
      const baseTicker = ticker.trim().toUpperCase();
      
      // Determine the suffix based on selected market
      const suffix = market === 'IN' ? '.NS' : '';
      
      // Only append if a suffix is needed and the user didn't manually type it
      const finalTicker = (suffix && !baseTicker.endsWith(suffix))
        ? `${baseTicker}${suffix}`
        : baseTicker;
      onSearch(finalTicker);
    }
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
        <button type="submit" className="btn" disabled={!ticker.trim() || isLoading}>
          {isLoading ? 'SCANNING...' : 'ANALYZE'}
        </button>
      </div>
    </form>
  );
};
