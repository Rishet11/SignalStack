import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { tickerApi } from '../../services/api';
import type { TickerInfo } from '../../types';
import { Search, Loader2 } from 'lucide-react';

const TickerSearch: React.FC = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<TickerInfo[]>([]);
  const [loading, setLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const navigate = useNavigate();
  const wrapperRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  useEffect(() => {
    if (query.length < 2) {
      setResults([]);
      return;
    }

    const delayDebounceFn = setTimeout(async () => {
      setLoading(true);
      try {
        const data = await tickerApi.search(query);
        setResults(data);
        setIsOpen(true);
      } catch (err) {
        console.error("Search failed:", err);
      } finally {
        setLoading(false);
      }
    }, 300);

    return () => clearTimeout(delayDebounceFn);
  }, [query]);

  const handleSelect = (symbol: string) => {
    setIsOpen(false);
    setQuery('');
    navigate(`/ticker/${symbol}`);
  };

  return (
    <div className="search-wrapper" ref={wrapperRef}>
      <div className="search-input-container">
        <Search className="search-icon" size={18} />
        <input
          type="text"
          placeholder="Search tickers (e.g. RELIANCE, TCS)..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onFocus={() => query.length >= 2 && setIsOpen(true)}
        />
        {loading && <Loader2 className="spinner" size={18} />}
      </div>

      {isOpen && results.length > 0 && (
        <div className="search-results glass-card">
          {results.map((result) => (
            <div
              key={result.symbol}
              className="search-result-item"
              onClick={() => handleSelect(result.symbol)}
            >
              <div className="result-symbol">{result.symbol}</div>
              <div className="result-info">
                <span className="result-name">{result.name}</span>
                <span className="result-sector">{result.sector}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default TickerSearch;
