from app.agents.base import BaseAgent
from app.core.state import ResearchState
from app.core.config import logger
from langchain_core.messages import SystemMessage, HumanMessage

class HTMLDesignerAgent(BaseAgent):
    async def invoke(self, state: ResearchState) -> ResearchState:
        logger.info("HTML Designer: Converting synthesized content to HTML")
        
        synthesized_content = state.get("synthesized_content")
        if not synthesized_content:
            logger.warning("No synthesized content to design.")
            return state

        # Construct prompt
        system_prompt = """You are an Elite Frontend Architect and UI/UX Designer.
        Your goal is to transform the provided Markdown research report into a "Deep Research Dashboard" - a single-file, interactive HTML application.
        
        **CRITICAL REQUIREMENT:**
        You must include **Interactive Charts** (using Chart.js via CDN) and **Key Metrics Cards**. 
        Do not just output text. Visualise the data.
        
        **Design System:**
        - Theme: Modern, Clean, Professional (Use Bootstrap 5 or Tailwind CSS via CDN).
        - Layout: Single Page Application feel.
        - Colors: Corporate Blue/Grey palette with vibrant accent colors for charts.
        
        **Structure Requirements:**
        1. **Executive Summary Card**: High-level impact statement.
        2. **Key Metrics Grid**: 3-4 cards showing numbers (e.g., "Market Size", "Growth Rate", "Key Players"). If exact numbers aren't in the data, estimate reasonable placeholders or use ranges found in the text.
        3. **Interactive Charts**:
           - Include at least one Bar Chart (e.g., Market Share or Regional Splits).
           - Include at least one Line Chart (e.g., Trends over time).
           - Use `<canvas>` elements and initialize `new Chart()` in a `<script>` tag at the bottom.
        4. **Deep Dive Sections**: Technical, Business, and Market analysis in collapsible accordions or tabs.
        5. **Sources Section**: A clean list of citations.

        **Content to Visualize:**
        Topic: {state['topic']}
        
        Refine and synthesize these findings into the report:
        {state.get('synthesized_content', 'No content available')}
        
        **Technical Constraints:**
        - Use a CDN for Chart.js: `<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>`
        - Ensure the HTML is fully self-contained (Single File).
        - Make it responsive.
        
        Output ONLY the raw HTML code. Do not wrap in markdown code blocks.
        """
        
        human_prompt = f"""Here is the research content to transform:
        
        {synthesized_content}
        
        Create the Deep Research Dashboard HTML now.
        """
        
        try:
            response = await self.llm.ainvoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt)
            ])
            
            html_output = response.content
            
            # Clean up if LLM wraps in code blocks despite instructions
            if html_output.startswith("```html"):
                html_output = html_output.replace("```html", "").replace("```", "")
            elif html_output.startswith("```"):
                html_output = html_output.replace("```", "")
                
            state["html_output"] = html_output.strip()
            state["progress_updates"].append("HTML Report generated.")
            
        except Exception as e:
            logger.error(f"Error generating HTML: {e}")
            state["errors"].append(f"HTML Generation Error: {e}")
            
        return state
