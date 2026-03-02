# Career Discovery Coach

An AI-powered career discovery platform that helps young people find their "spark" in the entertainment industry. Built for Usher's New Look Foundation hackathon.

---

## Features

### 1. Conversational Career Discovery (`/chatbot`)

- AI-driven discovery through strategic questioning
- Rotates through interests, skills, and work style
- Provides top 3 career matches with fit scores
- Generates personalized action plans with resources

### 2. Visual Roadmap Generator (`/roadmap`)

- Instant career roadmap generation for any goal
- Beautiful Mermaid.js flowchart visualization
- Phase-by-phase breakdown with timelines
- Specific, actionable steps for each phase

---

## Architecture

### 10-Node Hybrid LangGraph System

```
Phase 1: DISCOVERY
├── Node 1: Greeting - Welcomes user and sets context
├── Node 2: Router - Decides what to ask next (interests/skills/workstyle)
├── Node 3: Discovery - LLM generates contextual questions
└── Node 4: Validation - Checks if enough info gathered

Phase 2: ANALYSIS
├── Node 5: Synthesis - Extracts structured insights from conversation
└── Node 6: Enrichment - Adds metadata and completeness scores

Phase 3: RECOMMENDATION
├── Node 7: Matching - Matches profile to 50+ entertainment careers
├── Node 8: Ranking - Sorts careers by fit score
└── Node 9: Explanation - Generates detailed reasoning for top 3

Phase 4: ACTION
└── Node 10: Action Plan - Creates personalized next steps with UNL programs
```

---

## Getting Started

### Installation

#### 1. Backend Setup (LangGraph)

```bash
# Navigate to backend directory
cd career-agent

# Install dependencies
pip install -r requirements.txt
# OR
pip install langgraph langchain-openai python-dotenv

# Create .env file
cat > .env << EOF
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini/other-api-keys
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=career-coach-hackathon
LANGSMITH_API_KEY=your_langsmith_key_here
EOF

# Start LangGraph server
langgraph dev
```

Server will run on: `http://127.0.0.1:2024`

#### 2. Roadmap API Setup (FastAPI)

```bash
# In career-agent directory
pip install fastapi uvicorn groq

# Start FastAPI server (in new terminal)
python api_server.py
```

Server will run on: `http://127.0.0.1:8000`

#### 3. Frontend Setup (React)

The frontend lives in a separate repository: [my-website](https://github.com/Vyanaktesh/my-website)

```bash
# Clone the frontend repository
git clone https://github.com/Vyanaktesh/my-website.git
cd my-website

# Install dependencies
npm install

# Start dev server
npm run dev
```

App will run on: `http://localhost:5173`

---

## Project Structure

```
career-agent/              # LangGraph Backend
   ├── app/
   │   ├── nodes.py          # 10 node implementations
   │   ├── graph.py          # Graph orchestration
   │   ├── prompts.py        # LLM prompts
   │   ├── career_data.py    # 50+ entertainment careers
   │   └── roadmap.py        # Roadmap generation logic
   ├── studio_entry.py       # LangGraph Studio entry point
   ├── api_server.py         # FastAPI server for roadmap
   ├── langgraph.json        # LangGraph configuration
   ├── requirements.txt      # Python dependencies
   └── .env                  # Environment variables
```

---

## Usage

### Career Discovery Chat

1. Navigate to `/chatbot`
2. The bot will greet you and ask about your interests
3. Answer 6 strategic questions:
   - **Q1-2:** Interests (what excites you?)
   - **Q3-4:** Skills (what are you good at?)
   - **Q5-6:** Work Style (how do you like to work?)
4. Receive top 3 career matches with:
   - Fit scores (%)
   - Detailed reasoning
   - Personalized action plan
   - Usher's New Look program connections

### Roadmap Generator

1. Navigate to `/roadmap`
2. Enter a career goal (e.g., "ML Engineer at Google", "Music Producer")
3. Click "Generate"
4. View:
   - Visual Mermaid flowchart
   - Phase-by-phase breakdown
   - Timelines and actionable steps

---

## Configuration

### LangGraph Settings (`career-agent/.env`)

```properties
# OpenAI Configuration
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini/other-llm-keys

# LangSmith Tracing (Optional)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=career-coach-hackathon
LANGSMITH_API_KEY=lsv2_...

# Use Groq instead of OpenAI (Optional, FREE)
USE_GROQ=false
GROQ_API_KEY=gsk_...
```

### Using Groq (Free Alternative)

```bash
# Install Groq
pip install groq

# Update .env
USE_GROQ=true
GROQ_API_KEY=your_groq_key_here

# Get free API key: https://console.groq.com
```

### CORS Configuration

If your frontend runs on a different port, update `api_server.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:YOUR_PORT",  # Add your port
    ],
    # ...
)
```

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend Framework | LangGraph (Multi-Agent Orchestration) |
| LLM | OpenAI GPT-4o-mini / Groq Llama 3.1 |
| API Framework | FastAPI (for roadmap endpoint) |
| Frontend | React 18 + Vite |
| UI Library | Ant Design |
| Visualization | Mermaid.js |
| State Management | LangGraph Checkpointing |
| Tracing | LangSmith (optional) |

---

## Why This Agentic Flow Over a Standard Chatbot

| Feature | ChatGPT/RAG | Career Discovery Coach |
|---------|-------------|------------------------|
| Architecture | Single agent | 10-node multi-agent system |
| Question Strategy | User-driven | AI-driven discovery router |
| Career Database | Generic | 50+ entertainment careers |
| Recommendations | Unstructured | Ranked with fit scores |
| Action Plans | Generic | Personalized with UNL programs |
| State Management | Simple | LangGraph with phases |
| Quality Assurance | None | Validation nodes |
| Output Format | Text | Structured JSON + visual roadmaps |

---

## Troubleshooting

### LangGraph won't start

```bash
# Check if port 2024 is in use
lsof -ti:2024

# Kill the process
kill -9 $(lsof -ti:2024)

# Restart
langgraph dev
```

### CORS errors

1. Check `api_server.py` has your frontend port in `allow_origins`
2. Restart the FastAPI server: `python api_server.py`
3. Hard refresh browser (Cmd+Shift+R / Ctrl+Shift+R)

### Questions not incrementing

1. Check LangGraph logs for `[ROUTER] Questions asked: X`
2. Verify thread_id is consistent across messages
3. Ensure LangGraph server has built-in persistence (no custom checkpointer needed)

### Roadmap generation fails

1. Verify FastAPI server is running on port 8000
2. Check CORS settings include your frontend port
3. Verify OpenAI/Groq API key is set in `.env`

---

## Demo Flow

Example conversation:

```
Bot: What about entertainment catches your interest?
User: I love concerts and live music

Bot: What specific moments at concerts excite you?
User: The energy of the crowd and guitar solos

Bot: What skills do you have related to music?
User: I play guitar and used to be in a band

Bot: What type of music inspires you?
User: Rock and metal

Bot: Do you prefer solo or collaborative work?
User: I love working with a band

Bot: How do you like to structure your creative process?
User: Spontaneous jam sessions work best for me

Bot: [Generates Recommendations]
1. Music Producer (Fit: 90%)
2. Tour Manager (Fit: 85%)
3. DJ/Club DJ (Fit: 80%)

[Provides detailed action plan with weekly tasks]
```

---

## Educational Value

This project demonstrates:

- Multi-agent orchestration with LangGraph
- Conditional graph routing based on state
- Structured output generation with LLMs
- Streaming API responses
- State persistence across conversation
- Integration of multiple AI models
- Production-ready error handling
- React + FastAPI + LangGraph architecture

---

## About Usher's New Look

[Usher's New Look Foundation](https://www.ushersnewlook.org) empowers young people (ages 13-18) through:

- **Talent Development:** Performing arts and creative expression
- **Career Pathways:** Professional development in entertainment
- **Leadership:** Community service and civic engagement
- **Service Learning:** Real-world experience

This platform connects users with UNL programs and resources.

---

## License

MIT License - See LICENSE file for details

---

## Contributors

Built for Usher's New Look Foundation Hackathon 2025.
Feel free to contribute. You can add new nodes, tune prompts, or add new features.

---

## Acknowledgments

- Usher's New Look Foundation for inspiration
- LangChain/LangGraph for multi-agent framework
- OpenAI for GPT models
- Ant Design for UI components
- Mermaid.js for visualization

---

## Support

For issues or questions:

1. Check the Troubleshooting section above
2. Review LangGraph logs: `langgraph dev` output
3. Check browser console for frontend errors
4. Verify all services are running on correct ports
