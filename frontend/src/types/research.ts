export interface Finding {
    source: string;
    url?: string;
    content: string;
    raw_content: string;
    question: string;
}

export interface ResearchPlan {
    topic: string;
    subtopics: string[];
    queries: string[];
}

export interface Customization {
    depth: 'basic' | 'deep' | 'comprehensive';
    tone: 'professional' | 'academic' | 'creative';
}

export interface ResearchState {
    topic: string;
    customization: Customization;
    research_plan: ResearchPlan | null;
    web_findings: Finding[];
    technical_findings: Finding[];
    business_findings: Finding[];
    synthesized_content: string | null;
    html_output: string | null;
    quality_report: { score: number; critique: string } | null;
    status: "started" | "in_progress" | "complete" | "error";
    progress_updates: string[];
    errors: string[];
    metadata: Record<string, unknown>;
}

export type MessageType = 'user' | 'assistant';

export interface ChatMessage {
    id: string;
    type: MessageType;
    content: string;
    timestamp: number;
    // Assistant specific
    isThinking?: boolean;
    researchId?: string;
    researchState?: ResearchState;
    sources?: Finding[];
}

export interface ResearchResponse {
    research_id: string;
    status: string;
    message: string;
}
