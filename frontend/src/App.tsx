import { useState } from 'react';
import { Landing } from './pages/Landing';
import { Analysis } from './pages/Analysis';
import { StockDetails } from './pages/StockDetails';
import './index.css';

function App() {
  const [activeTicker, setActiveTicker] = useState<string | null>(null);
  const [appMode, setAppMode] = useState<'analyze' | 'details' | null>(null);

  const handleAction = (ticker: string, action: 'analyze' | 'details') => {
    setActiveTicker(ticker);
    setAppMode(action);
  };

  const handleBack = () => {
    setActiveTicker(null);
    setAppMode(null);
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

      {appMode === 'analyze' && activeTicker ? (
        <Analysis initialTicker={activeTicker} onBack={handleBack} />
      ) : appMode === 'details' && activeTicker ? (
        <StockDetails initialTicker={activeTicker} onBack={handleBack} />
      ) : (
        <Landing onAction={handleAction} />
      )}
    </div>
  );
}

export default App;
