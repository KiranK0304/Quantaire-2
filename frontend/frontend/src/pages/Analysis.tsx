import React, { useEffect, useState } from 'react';
import { analyzeTicker, getChartUrl } from '../services/api';
import type { AnalysisResponse } from '../services/api';
import { SearchBar } from '../components/SearchBar';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { PatternCard } from '../components/PatternCard';

interface AnalysisProps {
  initialTicker: string;
  onBack: () => void;
}

export const Analysis: React.FC<AnalysisProps> = ({ initialTicker, onBack }) => {
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AnalysisResponse | null>(null);
  const [modalImage, setModalImage] = useState<string | null>(null);

  const performAnalysis = async (targetTicker: string) => {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await analyzeTicker(targetTicker);
      setResult(data);
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
        <div className="toolbar-actions">
          <SearchBar onSearch={performAnalysis} isLoading={isLoading} />
          <button className="btn-link" onClick={onBack}>New Search</button>
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
        <>
          <div className="results-layout">
            {/* Chart */}
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

            {/* Sidebar */}
            <div className="sidebar">
              {/* Summary */}
              <div className="summary-card">
                <div className="summary-header">
                  <h3>SCAN SUMMARY</h3>
                </div>
                <div className="summary-body">
                  <div className="summary-ticker">{result.ticker}</div>
                  <p className="summary-text">{result.summary}</p>
                  <div className="meta-grid">
                    <div className="meta-item">
                      <span className="meta-label">DETECTIONS</span>
                      <span className="meta-value">{result.metadata.detection_count}</span>
                    </div>
                    <div className="meta-item">
                      <span className="meta-label">AVG CONF</span>
                      <span className="meta-value">{avgConfDisplay}</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Detections */}
              {result.detections.length === 0 ? (
                <div className="status-panel" style={{ margin: 0 }}>
                  <h3>No Patterns Detected</h3>
                  <p>The model did not find recognizable patterns in the current timeframe.</p>
                </div>
              ) : (
                result.detections.map((pattern, idx) => (
                  <PatternCard key={idx} pattern={pattern} />
                ))
              )}
            </div>
          </div>

          {/* Disclaimer */}
          <div className="status-panel" style={{ margin: '0 32px 24px' }}>
            <h3>Experimental Output</h3>
            <p>
              Results may not be correct. This is an educational experiment,
              not a paid signal service or financial advice.
            </p>
          </div>
        </>
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
