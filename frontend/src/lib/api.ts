import axios from 'axios';
import { ResearchState, ResearchResponse, Customization } from '../types/research';

// Use Next.js proxy to avoid CORS
const API_URL = '/api';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const startResearch = async (topic: string, customization?: Customization): Promise<ResearchResponse> => {
    const response = await api.post<ResearchResponse>('/research', {
        topic,
        customization
    });
    return response.data;
};

export const getResearchState = async (researchId: string): Promise<ResearchState> => {
    const response = await api.get<ResearchState>(`/research/${researchId}`);
    return response.data;
};

export default api;
