import React, { useState } from 'react';

interface SearchBarProps {
  onSearch: (ticker: string) => void;
  isLoading?: boolean;
}

export const SearchBar: React.FC<SearchBarProps> = ({ onSearch, isLoading = false }) => {
  const [ticker, setTicker] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (ticker.trim() && !isLoading) {
      onSearch(ticker.trim().toUpperCase());
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ width: '100%', display: 'flex', justifyContent: 'center' }}>
      <div className="input-wrap">
        <span className="ticker-icon">▸</span>
        <input
          type="text"
          value={ticker}
          onChange={(e) => setTicker(e.target.value)}
          placeholder="e.g. RELIANCE, TCS.NS, AAPL"
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
