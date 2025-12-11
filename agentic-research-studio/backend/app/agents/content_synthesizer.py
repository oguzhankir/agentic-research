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
        topic = state.get("topic", "Unknown Topic")
        customization = state.get("customization", {})
        tone = customization.get("tone", "professional")
        depth = customization.get("depth", "comprehensive")
        
        system_prompt = f"""You are an Expert Research Synthesizer. 
        Your goal is to create a {depth} research report on the topic: "{topic}".
        Tone: {tone}.
        
        Use the provided research findings to answer the original research questions. 
        Format the output in strict Markdown.
        Include Executive Summary, Detailed Analysis, and Key Takeaways.
        """
        
        human_prompt = f"""Here are the collected research findings:
        
        {combined_text}
        
        Please synthesize this into a structured report.
        """
        
        # 3. Call LLM
        try:
            response = await self.llm.ainvoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt)
            ])
            
            report = response.content
            state["synthesized_content"] = report
            state["progress_updates"].append("Research content synthesized.")
            
        except Exception as e:
            logger.error(f"Error during content synthesis: {e}")
            state["errors"].append(f"Content Synthesis Error: {e}")
            
        return state
