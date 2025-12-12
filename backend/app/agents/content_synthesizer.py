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
        for f in all_findings:
            findings_text += f"\n--- Finding ({f.get('type')}) ---\n"
            findings_text += f"Question: {f.get('question')}\n"
            findings_text += f"Content: {f.get('content') or f.get('raw_content')}\n"
            findings_text += f"Source: {f.get('source')}\n"

        system_prompt = "You are a Lead Editor. Synthesize the following research findings into a Comprehensive Markdown Report."
        
        try:
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
