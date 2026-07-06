import React, { useState } from 'react';
import type { StockInfo } from '../services/api';

interface StockMetricsProps {
  info: StockInfo;
}

/** Format large numbers into readable format (e.g., 4.53T, 159.9B) */
const formatNumber = (value: number | null, currency?: string | null): string => {
  if (value == null) return '—';
  const symbol = currency === 'INR' ? '₹' : currency === 'USD' ? '$' : '';
  if (value >= 1e12) return `${symbol}${(value / 1e12).toFixed(2)}T`;
  if (value >= 1e9) return `${symbol}${(value / 1e9).toFixed(2)}B`;
  if (value >= 1e6) return `${symbol}${(value / 1e6).toFixed(2)}M`;
  return `${symbol}${value.toLocaleString()}`;
};

/** Format percentage values */
const formatPct = (value: number | null): string => {
  if (value == null) return '—';
  return `${(value * 100).toFixed(2)}%`;
};

/** Format a simple number to 2 decimal places */
const fmt = (value: number | null): string => {
  if (value == null) return '—';
  return value.toFixed(2);
};

/** Format volume with commas */
const formatVol = (value: number | null): string => {
  if (value == null) return '—';
  return value.toLocaleString();
};

export const StockMetrics: React.FC<StockMetricsProps> = ({ info }) => {
  const [showSummaryModal, setShowSummaryModal] = useState(false);
  const isSummaryLong = info.summary && info.summary.length > 300;

  return (
    <div className="stock-metrics">
      {/* Company Header */}
      <div className="metrics-header">
        <div>
          <h3 className="metrics-company-name">{info.long_name || 'Unknown Company'}</h3>
          <div className="metrics-tags">
            {info.sector && <span className="metrics-tag">{info.sector}</span>}
            {info.industry && <span className="metrics-tag">{info.industry}</span>}
          </div>
        </div>
        {info.website && (
          <a href={info.website} target="_blank" rel="noopener noreferrer" className="metrics-website">
            {info.website.replace(/^https?:\/\//, '')} ↗
          </a>
        )}
      </div>

      {/* Business Summary */}
      {info.summary && (
        <div className="metrics-summary">
          <p>
            {isSummaryLong ? info.summary.slice(0, 300) + '…' : info.summary}
            {isSummaryLong && (
              <button 
                className="btn-link" 
                style={{ marginLeft: '8px', fontSize: '13px' }} 
                onClick={() => setShowSummaryModal(true)}
              >
                Read More
              </button>
            )}
          </p>
        </div>
      )}

      {/* Price Action Section */}
      <div className="metrics-section">
        <div className="metrics-section-title">PRICE ACTION</div>
        <div className="metrics-grid">
          <div className="metric-cell">
            <span className="metric-label">PREV CLOSE</span>
            <span className="metric-value">{fmt(info.previous_close)}</span>
          </div>
          <div className="metric-cell">
            <span className="metric-label">OPEN</span>
            <span className="metric-value">{fmt(info.open_price)}</span>
          </div>
          <div className="metric-cell">
            <span className="metric-label">DAY LOW</span>
            <span className="metric-value">{fmt(info.day_low)}</span>
          </div>
          <div className="metric-cell">
            <span className="metric-label">DAY HIGH</span>
            <span className="metric-value">{fmt(info.day_high)}</span>
          </div>
          <div className="metric-cell">
            <span className="metric-label">VOLUME</span>
            <span className="metric-value">{formatVol(info.volume)}</span>
          </div>
          <div className="metric-cell">
            <span className="metric-label">AVG VOLUME</span>
            <span className="metric-value">{formatVol(info.average_volume)}</span>
          </div>
        </div>
      </div>

      {/* Technical Section */}
      <div className="metrics-section">
        <div className="metrics-section-title">TECHNICALS</div>
        <div className="metrics-grid">
          <div className="metric-cell">
            <span className="metric-label">52W HIGH</span>
            <span className="metric-value">{fmt(info.fifty_two_week_high)}</span>
          </div>
          <div className="metric-cell">
            <span className="metric-label">52W LOW</span>
            <span className="metric-value">{fmt(info.fifty_two_week_low)}</span>
          </div>
          <div className="metric-cell">
            <span className="metric-label">50D AVG</span>
            <span className="metric-value">{fmt(info.fifty_day_average)}</span>
          </div>
          <div className="metric-cell">
            <span className="metric-label">200D AVG</span>
            <span className="metric-value">{fmt(info.two_hundred_day_average)}</span>
          </div>
        </div>
      </div>

      {/* Valuation Section */}
      <div className="metrics-section">
        <div className="metrics-section-title">VALUATION</div>
        <div className="metrics-grid">
          <div className="metric-cell">
            <span className="metric-label">MARKET CAP</span>
            <span className="metric-value accent">{formatNumber(info.market_cap, info.currency)}</span>
          </div>
          <div className="metric-cell">
            <span className="metric-label">ENTERPRISE VAL</span>
            <span className="metric-value">{formatNumber(info.enterprise_value, info.currency)}</span>
          </div>
          <div className="metric-cell">
            <span className="metric-label">TRAILING P/E</span>
            <span className="metric-value">{fmt(info.trailing_pe)}</span>
          </div>
          <div className="metric-cell">
            <span className="metric-label">FORWARD P/E</span>
            <span className="metric-value">{fmt(info.forward_pe)}</span>
          </div>
          <div className="metric-cell">
            <span className="metric-label">P/B RATIO</span>
            <span className="metric-value">{fmt(info.price_to_book)}</span>
          </div>
          <div className="metric-cell">
            <span className="metric-label">DIV YIELD</span>
            <span className="metric-value">{formatPct(info.dividend_yield)}</span>
          </div>
        </div>
      </div>

      {/* Financial Health Section */}
      <div className="metrics-section">
        <div className="metrics-section-title">FINANCIAL HEALTH</div>
        <div className="metrics-grid">
          <div className="metric-cell">
            <span className="metric-label">PROFIT MARGIN</span>
            <span className="metric-value">{formatPct(info.profit_margins)}</span>
          </div>
          <div className="metric-cell">
            <span className="metric-label">OP MARGIN</span>
            <span className="metric-value">{formatPct(info.operating_margins)}</span>
          </div>
          <div className="metric-cell">
            <span className="metric-label">ROE</span>
            <span className="metric-value">{formatPct(info.return_on_equity)}</span>
          </div>
          <div className="metric-cell">
            <span className="metric-label">REV GROWTH</span>
            <span className="metric-value">{formatPct(info.revenue_growth)}</span>
          </div>
          <div className="metric-cell">
            <span className="metric-label">EARN GROWTH</span>
            <span className="metric-value">{formatPct(info.earnings_growth)}</span>
          </div>
          <div className="metric-cell">
            <span className="metric-label">D/E RATIO</span>
            <span className="metric-value">{fmt(info.debt_to_equity)}</span>
          </div>
        </div>
      </div>

      {/* Summary Modal Popup */}
      {showSummaryModal && (
        <div className="modal-overlay" onClick={() => setShowSummaryModal(false)}>
          <div className="status-panel" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '600px', width: '90%', textAlign: 'left', position: 'relative' }}>
            <button 
              className="close-modal" 
              style={{ position: 'absolute', top: '12px', right: '16px', background: 'none', border: 'none', color: 'var(--text-muted)', fontSize: '24px', cursor: 'pointer' }}
              onClick={() => setShowSummaryModal(false)}
            >
              &times;
            </button>
            <h3 style={{ marginBottom: '16px', color: 'var(--accent)' }}>Business Summary</h3>
            <p style={{ color: 'var(--text-primary)', fontSize: '15px', lineHeight: '1.6', overflowY: 'auto', maxHeight: '60vh' }}>
              {info.summary}
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

