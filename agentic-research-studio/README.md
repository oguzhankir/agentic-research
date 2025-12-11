# Agentic Research Studio
## BVA507E - Business Analytics for Managers Projects

### Project Overview
Agentic Research Studio is a next-generation autonomous research web application designed to demonstrate the power of **Multi-Agent Systems (MAS)** in automating complex business and technical analysis.

This project was developed for the **BVA507E (Business Analytics for Managers)** course at **Istanbul Technical University (ITU)**. The goal is to showcase how AI agents can collaborate to solve unstructured problems, mimicking a human consulting team.

### Architecture: The Agent Swarm
The system is built on a **LangGraph** architecture, orchestrating a team of specialized AI agents:

1.  **Research Planner (The Manager)**: Decomposes a high-level user topic (e.g., "Future of Fusion Energy") into granular research questions. It assigns tasks to the most suitable sub-agents.
2.  **Web Researcher (The Explorer)**: Scours the internet for broad context and sources.
3.  **Technical Analyst (The Engineer)**: Deep dives into technical specifications, GitHub repositories, and architectural details.
4.  **Business Analyst (The Strategist)**: Evaluates market size, diverse competitors, and revenue models.
5.  **Content Synthesizer (The Writer)**: Aggregates all diverse findings into a coherent, flowing narrative.
6.  **HTML Designer (The Visualizer)**: Automatically codes an interactive HTML dashboard with charts and metrics to present the final report.

### Key Features
*   **"Super App" Interface**: Built with **Next.js 14**, featuring a premium "Aurora" dark mode UI, glassmorphism, and Framer Motion animations.
*   **Interactive Chat**: Conversational interface for initiating research and refining queries.
*   **Real-time Thinking**: Visualizes the internal state and logs of the agent swarm as they work.
*   **Dynamic Reporting**: Generates downloadable, single-file HTML dashboards with interactive charts (Chart.js).

### Technology Stack
*   **Frontend**: Next.js 14, TypeScript, Tailwind CSS v4, Shadcn/UI, Framer Motion.
*   **Backend**: Python, FastAPI, LangGraph, LangChain.
*   **AI Models**: OpenAI GPT-4o / GPT-4-turbo.
*   **Deployment**: Docker & Docker Compose.

### How to Run
Prerequisites: Docker key and OpenAI API Key.

1.  Clone the repository.
2.  Set your API key in `backend/.env`.
3.  Run the stack:
    ```bash
    docker-compose up --build
    ```
4.  Access the application at `http://localhost:3000`.

---
**Course**: BVA507E - Business Analytics for Managers
**Term**: Fall 2025
**Institution**: Istanbul Technical University
