const API_BASE_URL = 'http://127.0.0.1:8080';

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
      let errorMessage = `Failed to analyze ticker. Status: ${response.status}`;
      try {
        const errorData = await response.json();
        if (errorData.detail) {
          errorMessage = errorData.detail;
        }
      } catch (e) {
        // Ignored if JSON parsing fails
      }
      throw new Error(errorMessage);
    }

    return response.json();
  } catch (error: any) {
    // If it's already an error we threw, rethrow it. Otherwise, it's a network error.
    if (error.message && error.message.includes('Status:')) {
      throw error;
    }
    if (error.message && error.message !== 'Failed to fetch') {
      throw error;
    }
    throw new Error('Unable to connect to the analysis server. Please ensure the backend is running.');
  }
};

/**
 * Returns the full URL to fetch the generated chart image for a specific ticker.
 * @param ticker The stock ticker symbol
 */
export const getChartUrl = (ticker: string): string => {
  return `${API_BASE_URL}/chart/${ticker}?t=${new Date().getTime()}`;
};
