import { useState } from 'react';
import { Landing } from './pages/Landing';
import { Analysis } from './pages/Analysis';
import './index.css';

function App() {
  const [activeTicker, setActiveTicker] = useState<string | null>(null);

  const handleAnalyze = (ticker: string) => {
    setActiveTicker(ticker);
  };

  const handleBack = () => {
    setActiveTicker(null);
  };

  return (
    <div className="root">
      <div className="topbar">
        <div className="topbar-left">
          <span className="pa-badge">PA</span>
          <div>
            <div className="topbar-title">Price Action Analyzer</div>
            <div className="topbar-sub">YOLOv8 candlestick pattern detection &middot; by Kiran</div>
          </div>
        </div>
        <div className="sys">
          <div className="dot"></div>SYS: ONLINE
        </div>
      </div>

      {activeTicker ? (
        <Analysis initialTicker={activeTicker} onBack={handleBack} />
      ) : (
        <Landing onAnalyze={handleAnalyze} />
      )}
    </div>
  );
}

export default App;
