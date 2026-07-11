const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8080';

export interface PatternDetection {
  name: string;
  confidence: number;
  description: string;
  annotations: Record<string, any>;
}

export interface AnalysisMetadata {
  detection_count: number;
  pattern_names: string[];
  has_confidence: boolean;
  average_confidence: number | null;
}

export interface AnalysisResponse {
  ticker: string;
  summary: string;
  detections: PatternDetection[];
  metadata: AnalysisMetadata;
}

/**
 * Submits a ticker to the FastAPI backend for price action analysis.
 * @param ticker The stock ticker symbol (e.g., 'TCS.NS')
 */
export const analyzeTicker = async (ticker: string): Promise<AnalysisResponse> => {
  try {
    const response = await fetch(`${API_BASE_URL}/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ ticker }),
    });

    if (!response.ok) {
      if (response.status === 404) {
        throw new Error(`We couldn't find any market data for '${ticker}'. Please check the symbol and try again.`);
      }
      if (response.status === 422) {
        throw new Error('The market data for this ticker could not be processed.');
      }
      throw new Error('The analysis service encountered an unexpected issue. Please try again later.');
    }

    return response.json();
  } catch (error: any) {
    // Pass through our custom user-friendly errors
    if (error.message && !error.message.includes('Failed to fetch') && !error.message.includes('NetworkError')) {
      throw error;
    }
    // Generic fallback for actual connection failures (backend down, DNS error, etc.)
    throw new Error('The analysis service is currently unavailable. Please check your connection or try again later.');
  }
};

/**
 * Returns the full URL to fetch the generated chart image for a specific ticker.
 * @param ticker The stock ticker symbol
 */
export const getChartUrl = (ticker: string): string => {
  return `${API_BASE_URL}/chart/${ticker}?t=${new Date().getTime()}`;
};

export interface StockInfo {
  long_name: string | null;
  sector: string | null;
  industry: string | null;
  summary: string | null;
  website: string | null;
  currency: string | null;
  previous_close: number | null;
  open_price: number | null;
  day_low: number | null;
  day_high: number | null;
  volume: number | null;
  average_volume: number | null;
  fifty_two_week_high: number | null;
  fifty_two_week_low: number | null;
  fifty_day_average: number | null;
  two_hundred_day_average: number | null;
  market_cap: number | null;
  enterprise_value: number | null;
  trailing_pe: number | null;
  forward_pe: number | null;
  price_to_book: number | null;
  dividend_yield: number | null;
  profit_margins: number | null;
  operating_margins: number | null;
  return_on_equity: number | null;
  revenue_growth: number | null;
  earnings_growth: number | null;
  debt_to_equity: number | null;
}

/**
 * Fetches detailed stock information for a given ticker.
 * @param ticker The stock ticker symbol
 */
export const fetchStockInfo = async (ticker: string): Promise<StockInfo> => {
  try {
    const response = await fetch(`${API_BASE_URL}/info`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ ticker }),
    });
    if (!response.ok) {
      throw new Error('Stock info unavailable.');
    }
    return response.json();
  } catch (error: any) {
    if (error.message && !error.message.includes('Failed to fetch')) {
      throw error;
    }
    throw new Error('Could not load stock information.');
  }
};
