from typing import List, Dict, Any
from app.agents.base import BaseAgent
from app.core.state import ResearchState
from app.core.config import logger
from langchain_core.messages import SystemMessage, HumanMessage

class ContentSynthesizerAgent(BaseAgent):
    async def invoke(self, state: ResearchState) -> ResearchState:
        logger.info("Content Synthesizer: Aggregating findings and generating report")
        
        # 1. Aggregate Findings
        web_findings = state.get("web_findings", [])
        technical_findings = state.get("technical_findings", [])
        business_findings = state.get("business_findings", [])
        
        all_findings = []
        for f in web_findings:
            all_findings.append(f"[Web] {f.get('question', '')}: {f.get('raw_content', '')}")
        for f in technical_findings:
            all_findings.append(f"[Technical] {f['question']}: {f.get('raw_content', '')}")
        for f in business_findings:
            all_findings.append(f"[Business] {f['question']}: {f.get('raw_content', '')}")
            
        if not all_findings:
            logger.warning("No findings available to synthesize.")
            state["synthesized_content"] = "No research findings were collected."
            return state

        combined_text = "\n\n".join(all_findings)
        
        # 2. Construct Prompt for Synthesis
        state["progress_updates"].append("Content Synthesizer: Aggregating all research data...")
        
        # Format findings for LLM
        findings_text = ""
        
        # Helper to format dict findings
        def format_finding(f, f_type):
            text = f"\n--- Finding ({f_type}) ---\n"
            text += f"Question: {f.get('question', 'N/A')}\n"
            # Handle both 'content' and 'raw_content' keys
            content = f.get('content') or f.get('raw_content') or "No content"
            text += f"Content: {content}\n"
            text += f"Source: {f.get('source', 'Unknown')}\n"
            return text

        for f in web_findings:
            findings_text += format_finding(f, "Web")
        for f in technical_findings:
            findings_text += format_finding(f, "Technical")
        for f in business_findings:
            findings_text += format_finding(f, "Business")

        # Safe truncation to avoid Context Limit Errors or timeouts
        MAX_CHARS = 50000 
        if len(findings_text) > MAX_CHARS:
            logger.warning(f"Truncating findings from {len(findings_text)} to {MAX_CHARS} chars.")
            findings_text = findings_text[:MAX_CHARS] + "\n...(truncated due to length)..."
            
        logger.info(f"Synthesizer Input Size: {len(findings_text)} chars")
        state["progress_updates"].append(f"Processing {len(findings_text)} characters of data...")

        system_prompt = "You are a Lead Editor. Synthesize the following research findings into a Comprehensive Markdown Report."
        
        try:
            # Add timeout to call to prevent infinite hang? 
            # Standard langchain call
            response = await self.llm.ainvoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Write the report based on:\n\n{findings_text}")
            ])
            
            state["synthesized_content"] = response.content
            state["progress_updates"].append("Content Synthesizer: Final Report Drafted.")
            
        except Exception as e:

            logger.error(f"Error during content synthesis: {e}")
            state["errors"].append(f"Content Synthesis Error: {e}")
            
        return state
