from app.agents.base import BaseAgent
from app.core.state import ResearchState
from app.core.config import logger
from langchain_core.messages import SystemMessage, HumanMessage
from app.utils.text import clean_html_response

class HTMLDesignerAgent(BaseAgent):
    async def invoke(self, state: ResearchState) -> ResearchState:
        logger.info("HTML Designer: Converting synthesized content to HTML")
        
        synthesized_content = state.get("synthesized_content")
        if not synthesized_content:
            logger.warning("No synthesized content to design.")
            return state

        state["progress_updates"].append("HTML Designer: Designing Dashboard Layout...")

        # Construct prompt
        system_prompt = """You are an Elite Business Intelligence Architect and Academic Researcher.
        
        **OBJECTIVE:**
        Transform the provided research findings into a **World-Class Executive Strategy Dashboard**.
        The output must be a single-file HTML application that looks like a $50,000 KPMG/McKinsey report, but dynamic.
        
        **CORE REQUIREMENTS:**
        1. **Depth & Length:** The report must be EXTENSIVE. Do not summarize too much. Keep specific details, numbers, and technical specs. 
        2. **Visuals:** Use Chart.js to create AT LEAST 3 distinct interactive charts (Bar, Line, Radar, or Doughnut). Infer data points from the text if explicit numbers are missing (estimate with ranges based on context).
        3. **Sources:** You MUST cite sources. Create a dedicated "References & Citations" section at the bottom with links.
        
        **DESIGN SYSTEM (Modern & Professional):**
        - Use **Tailwind CSS** (via CDN) for styling.
        - Font: 'Inter' or 'Roboto'.
        - Layout: 
          - **Header**: Sticky, with "BVA507E - Business Analytics Project" branding.
          - **Hero Section**: Title, Subtitle, Date, prepared for "Strategic Management".
          - **Executive Summary**: A powerful high-level overview (300+ words).
          - **Key Metrics Row**: 4 cards with big numbers and trend indicators (green/red arrows).
          - **Analysis Tabs**: Use JavaScript to toggle between "Market Analysis", "Technical Architecture", and "Business Strategy".
          - **Strategic Recommendations**: A SWOT analysis or bulleted strategic advice.
        
        **CONTENT TO PROCESS:**
        Topic: {topic}
        Content: {content}
        
        **TECHNICAL DETAILS:**
        - Include `Chart.js` via CDN.
        - Include `Tailwind` via CDN.
        - Ensure responsive mobile/desktop design.
        - **Interactive Elements**: Hover effects, smooth scrolling, tab switching.
        
        Output ONLY the raw HTML code. Do not wrap in markdown code blocks.
        """
        
        human_prompt = f"""Generate the Academic Business Intelligence Dashboard for: "{state['topic']}".
        Ensure it is detailed, professional, and visually stunning.
        """
        
        try:
            # Format prompt with content safely
            formatted_system = system_prompt.format(
                topic=state['topic'],
                content=synthesized_content
            )
            
            response = await self.llm.ainvoke([
                SystemMessage(content=formatted_system),
                HumanMessage(content=human_prompt)
            ])
            
            html_output = clean_html_response(response.content)
                
            state["html_output"] = html_output
            state["progress_updates"].append("HTML Report generated.")
            
        except Exception as e:
            logger.error(f"Error generating HTML: {e}")
            state["errors"].append(f"HTML Generation Error: {e}")
            
        return state
