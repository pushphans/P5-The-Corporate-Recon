# P5-The-Corporate-Recon

A LangGraph-based corporate research and analysis agent that helps turn a business query into a structured, professional executive summary. The workflow breaks the request into multiple research topics, gathers information using web search, and combines the results into a final report.

## Overview

P5-The-Corporate-Recon is an AI-powered research agent designed for company analysis and business intelligence tasks. It demonstrates a multi-step workflow where:

- a manager agent splits the user request into focused research topics,
- worker nodes collect relevant information from the web,
- a reducer node synthesizes the findings into a polished summary.

This makes it useful for exploring company profiles, market positioning, recent developments, and strategic themes.

## Key Features

- Multi-step research workflow with LangGraph
- Topic planning and decomposition for complex queries
- Web search-based evidence gathering
- Structured aggregation of research results
- Executive-summary generation from collected data
- Modular agent design for extension and experimentation

## Tech Stack

- Python
- LangChain
- LangGraph
- OpenAI GPT-4o-mini
- DuckDuckGo Search
- Pydantic
- FastAPI (included in dependencies, though the core logic is workflow-focused)

## Project Structure

```text
.
├── app/
│   ├── agent/
│   │   └── graph.py
│   ├── core/
│   │   ├── config.py
│   │   └── tools.py
├── 1.md
├── analysis.md
├── requirements.txt
└── README.md
```

## Prerequisites

Before running the project, make sure you have:

- Python 3.10 or higher
- pip installed
- An OpenAI API key

## Installation

1. Clone the repository

```bash
git clone https://github.com/pushphans/P5-The-Corporate-Recon.git
cd P5-The-Corporate-Recon
```

2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Configure environment variables

Create a `.env` file or export your API key:

```bash
export OPENAI_API_KEY=your_openai_api_key
```

## How It Works

The workflow inside `app/agent/graph.py` follows this structure:

1. Manager node
   - Breaks the user request into three focused research topics.

2. Worker nodes
   - Search the web for each topic using DuckDuckGo.

3. Reducer node
   - Combines the gathered evidence and writes a final executive summary.

This approach is useful for research tasks that need multiple perspectives and evidence-based reporting.

## Example Usage

You can run the workflow by invoking the agent with a company analysis query such as:

```python
from app.agent.graph import run_agent

await run_agent("Analyze Infosys and provide an executive summary")
```

## Notes

The project is designed as a practical example of an AI research agent using LangGraph. It is ideal for learning how to:

- split a problem into subtasks,
- use tools in a graph-based workflow,
- generate structured outputs from retrieved information.

## Contributing

Contributions, improvements, and new research workflows are welcome. Feel free to open an issue or submit a pull request.
