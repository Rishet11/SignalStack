import axios from 'axios';
import type { OpportunityCard, TickerInfo, AuditTrail } from '../types';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
});

export const signalsApi = {
  getOpportunities: async (): Promise<OpportunityCard[]> => {
    const response = await api.get('/signals/opportunities');
    return response.data;
  },
  analyzeTicker: async (ticker: string): Promise<OpportunityCard> => {
    const response = await api.post(`/signals/analyze/${ticker}`);
    return response.data;
  },
};

export const tickerApi = {
  search: async (query: string): Promise<TickerInfo[]> => {
    const response = await api.get('/ticker/search', { params: { q: query } });
    return response.data;
  },
  getInfo: async (symbol: string): Promise<TickerInfo> => {
    const response = await api.get(`/ticker/${symbol}`);
    return response.data;
  },
  getChartData: async (symbol: string): Promise<any[]> => {
    const response = await api.get(`/ticker/${symbol}/chart`);
    return response.data;
  },
};

export const auditApi = {
  getTrail: async (requestId: string): Promise<AuditTrail> => {
    const response = await api.get(`/audit/${requestId}`);
    return response.data;
  },
};

export default api;
