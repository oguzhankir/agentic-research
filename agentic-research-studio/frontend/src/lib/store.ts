import { create } from 'zustand';
import { Customization, ChatMessage } from '../types/research';
import { startResearch, getResearchState } from './api';
import { v4 as uuidv4 } from 'uuid';

interface ChatStore {
    messages: ChatMessage[];
    isLoading: boolean;

    // Actions
    addMessage: (msg: ChatMessage) => void;
    updateMessage: (id: string, updates: Partial<ChatMessage>) => void;
    startResearchSession: (topic: string, customization?: Customization) => Promise<void>;
    pollActiveRequest: (researchId: string, messageId: string) => Promise<void>;
}

export const useChatStore = create<ChatStore>((set, get) => ({
    messages: [],
    isLoading: false,

    addMessage: (msg) => set((state) => ({ messages: [...state.messages, msg] })),

    updateMessage: (id, updates) => set((state) => ({
        messages: state.messages.map((m) => m.id === id ? { ...m, ...updates } : m)
    })),

    startResearchSession: async (topic, customization) => {
        const { addMessage, pollActiveRequest, updateMessage } = get();

        // 1. Add User Message
        addMessage({
            id: uuidv4(),
            type: 'user',
            content: topic,
            timestamp: Date.now()
        });

        // 2. Add Assistant Placeholder (Thinking)
        const assistantMsgId = uuidv4();
        addMessage({
            id: assistantMsgId,
            type: 'assistant',
            content: '',
            isThinking: true,
            timestamp: Date.now(),
            researchState: undefined
        });

        set({ isLoading: true });

        try {
            const response = await startResearch(topic, customization);

            // Update with research ID
            updateMessage(assistantMsgId, { researchId: response.research_id });

            // Start polling
            pollActiveRequest(response.research_id, assistantMsgId);

        } catch (err: unknown) {
            const errorMessage = err instanceof Error ? err.message : String(err);
            updateMessage(assistantMsgId, {
                content: `Error starting research: ${errorMessage}`,
                isThinking: false
            });
            set({ isLoading: false });
        }
    },

    pollActiveRequest: async (researchId, messageId) => {
        const pollInterval = setInterval(async () => {
            const { updateMessage } = get();
            try {
                const data = await getResearchState(researchId);

                updateMessage(messageId, {
                    researchState: data,
                    // Update sources if available
                    sources: [
                        ...data.web_findings,
                        ...data.technical_findings,
                        ...data.business_findings
                    ]
                });

                if (data.status === 'complete' || data.status === 'error' || !!data.html_output) {
                    clearInterval(pollInterval);
                    set({ isLoading: false });
                    updateMessage(messageId, {
                        isThinking: false,
                        content: data.synthesized_content || "Research complete."
                    });
                }
            } catch (err) {
                console.error("Polling error", err);
            }
        }, 2000);
    }
}));
