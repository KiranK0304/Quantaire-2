import React, { useEffect, useState } from 'react';
import { analyzeTicker, getChartUrl, fetchStockInfo } from '../services/api';
import type { AnalysisResponse, StockInfo } from '../services/api';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { PatternCard } from '../components/PatternCard';
import { StockMetrics } from '../components/StockMetrics';

interface AnalysisProps {
  initialTicker: string;
  onBack: () => void;
}

export const Analysis: React.FC<AnalysisProps> = ({ initialTicker, onBack }) => {
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AnalysisResponse | null>(null);
  const [stockInfo, setStockInfo] = useState<StockInfo | null>(null);
  const [modalImage, setModalImage] = useState<string | null>(null);

  const performAnalysis = async (targetTicker: string) => {
    setIsLoading(true);
    setError(null);
    setResult(null);
    setStockInfo(null);

    try {
      // Fetch analysis and stock info in parallel
      const [analysisData, infoData] = await Promise.all([
        analyzeTicker(targetTicker),
        fetchStockInfo(targetTicker).catch(() => null), // Don't fail if info is unavailable
      ]);
      setResult(analysisData);
      setStockInfo(infoData);
    } catch (err: any) {
      setError(err.message || 'An unexpected error occurred.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    performAnalysis(initialTicker);
  }, []);

  const openModal = (src: string) => setModalImage(src);
  const closeModal = () => setModalImage(null);

  const avgConf = result?.metadata?.average_confidence;
  const avgConfDisplay = avgConf != null && !isNaN(avgConf)
    ? `${Math.round(avgConf * 100)}%`
    : '—';

  return (
    <>
      {/* Toolbar */}
      <div className="results-toolbar">
        <div>
          <p className="eyebrow">{isLoading ? 'SCANNING...' : 'SCAN COMPLETE'}</p>
          <h2>Analysis: {result?.ticker || initialTicker.toUpperCase()}</h2>
        </div>
      </div>

      {/* Loading State */}
      {isLoading && <LoadingSpinner />}

      {/* Error State */}
      {error && (
        <div className="status-panel error-panel" style={{ margin: '24px 32px' }}>
          <h3>Error Analyzing Ticker</h3>
          <p>{error}</p>
        </div>
      )}

      {/* Results */}
      {result && !isLoading && (
        <div className="results-single">

          {/* No Detections Message */}
          {result.detections.length === 0 && (
            <div className="status-panel" style={{ margin: '0 0 16px' }}>
              <h3 style={{ color: '#ff9800' }}>No Patterns Detected</h3>
              <p>The model did not find any recognizable price-action patterns for {result.ticker} in the current timeframe.</p>
            </div>
          )}

          {/* Chart — only shown when patterns were detected */}
          {result.detections.length > 0 && (
            <div className="chart-card">
              <div className="chart-header">
                <h3>{result.ticker} · CHART</h3>
                <span className="badge badge-detected">
                  {result.metadata.detection_count} DETECTED
                </span>
              </div>
              <div
                className="chart-image-container"
                onClick={() => openModal(getChartUrl(result.ticker))}
              >
                <img
                  src={getChartUrl(result.ticker)}
                  alt={`${result.ticker} annotated chart`}
                  onError={(e) => {
                    (e.target as HTMLImageElement).style.display = 'none';
                  }}
                />
                <div className="expand-hint">Click to enlarge</div>
              </div>
            </div>
          )}

          {/* Scan Summary */}
          <div className="summary-card">
            <div className="summary-header">
              <h3>SCAN SUMMARY</h3>
            </div>
            <div className="summary-body">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div className="summary-ticker">{result.ticker}</div>
                <span className={`badge ${result.metadata.detection_count > 0 ? 'badge-detected' : 'badge-neutral'}`}>
                  {result.metadata.detection_count > 0 ? 'SIGNALS FOUND' : 'NO SIGNALS'}
                </span>
              </div>

              <div className="meta-grid" style={{ marginTop: '16px' }}>
                <div className="meta-item">
                  <span className="meta-label">DETECTIONS</span>
                  <span className="meta-value" style={{ color: 'var(--accent)' }}>{result.metadata.detection_count}</span>
                </div>
                <div className="meta-item">
                  <span className="meta-label">AVG CONF</span>
                  <span className="meta-value">{avgConfDisplay}</span>
                </div>
              </div>

              <div className="sys-log">
                <div className="sys-log-title">SYSTEM OUTPUT</div>
                <p className="sys-log-text">{result.summary}</p>
              </div>
            </div>
          </div>

          {/* Detection Cards */}
          {result.detections.length > 0 && (
            <div className="detections-list">
              {result.detections.map((pattern, idx) => (
                <PatternCard key={idx} pattern={pattern} />
              ))}
            </div>
          )}

          {/* Stock Info */}
          {stockInfo && <StockMetrics info={stockInfo} />}

          {/* New Search CTA */}
          <div style={{ marginTop: '32px', display: 'flex', justifyContent: 'center' }}>
            <button 
              className="btn btn-rounded" 
              onClick={onBack}
              style={{ width: '100%', maxWidth: '400px', padding: '18px', fontSize: '18px', letterSpacing: '2px', background: 'var(--accent)', color: 'var(--bg-root)' }}
            >
              ← START NEW SEARCH
            </button>
          </div>

          {/* Disclaimer */}
          <div className="status-panel" style={{ marginTop: '16px' }}>
            <h3>Experimental Output</h3>
            <p>
              Results may not be correct. This is an educational experiment,
              not a paid signal service or financial advice.
            </p>
          </div>
        </div>
      )}

      {/* Image Modal */}
      {modalImage && (
        <div className="modal-overlay" onClick={closeModal}>
          <button className="close-modal" onClick={closeModal}>&times;</button>
          <img className="modal-content" src={modalImage} alt="Expanded chart" />
        </div>
      )}
    </>
  );
};
