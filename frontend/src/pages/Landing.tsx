import React from 'react';
import { SearchBar } from '../components/SearchBar';

interface LandingProps {
  onAction: (ticker: string, action: 'analyze' | 'details') => void;
}

export const Landing: React.FC<LandingProps> = ({ onAction }) => {
  return (
    <>
      <div className="hero">
        <div className="eyebrow">MARKET PATTERN SCAN</div>

        <h2 className="headline">
          Detect market structures<br />using <em>AI-powered</em><br />chart analysis.
        </h2>

        <p className="subline">
          Enter a ticker symbol below to capture charts and run pattern detection, or view stock details.
        </p>

        <SearchBar onAction={onAction} />

        <div className="pills">
          <span className="pill">Loading may take some time.</span>
          <span className="pill">Educational and experimental output only.</span>
          <span className="pill">Not financial advice.</span>
        </div>
      </div>

      <hr className="sep" />

      <div className="footer-note">
        <span className="fn-badge">SYSTEM NOTE</span>
        <div>
          <div className="fn-title">Prototype by Kiran</div>
          <div className="fn-body">
            This scanner is an educational and experimental interface. Model output may be
            incomplete or incorrect, and it should not be treated as paid, certified, or
            financial advice.
          </div>
        </div>
      </div>
    </>
  );
};
