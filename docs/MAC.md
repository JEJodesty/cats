## [Multi-Agent Collaboration of CAT Order Composition (Experiment): CATs adjacent experiment for agents that compose CAT Orders from natural language](../car_demo.py)
LangGraph demo with collaborating LLM agents (research + chart outline). This is adjacent experiment from the CAT mesh workflow in [DEMO.md](./DEMO.md) for future of agents that compose CAT Orders from natural language
  * no IPFS, Docker, or CAT node required.

#### Demonstrates the following
`car_demo.py` builds a small multi-agent collaboration graph using LangChain + LangGraph:

1. Two specialized agents sharing one conversation (MessagesState):
  * Researcher — has Tavily web search; gathers current information
  * Chart generator — no tools; turns research into a chart outline/description
2. Orchestration via a state graph:
  * researcher → may call Tavily (call_tool) → back to researcher
  * → hands off to chart_generator
  * → can loop back to researcher until someone emits FINAL ANSWER
  * Routers decide: run tools, switch agents, or stop
3. Operational wiring:
  * API keys from `.env` (OpenAI, LangChain/LangSmith, Tavily)
  * LangSmith tracing (LANGCHAIN_TRACING_V2, project "Multi-agent Collaboration")
  * Marimo UI with a Run button so the graph doesn’t fire on every cell rerun

#### Steps:
##### 1. [Create Virtual Environment](./ENV.md)
```bash
# CATs working directory
cd cats
python -m venv ./venv
```
##### 2. Activate Virtual Environment:
```bash
source ./venv/bin/activate
# (venv) $
pip install -e .
```
##### 3. Configure API keys *in the repo root* (`.env` is gitignored):
```bash
OPENAI_API_KEY=sk-...
LANGCHAIN_API_KEY=...
TAVILY_API_KEY=...
```
* **OpenAI** — LLM calls (`gpt-4o-mini` by default in the notebook)
* **LangChain / LangSmith** — optional tracing (`LANGCHAIN_TRACING_V2=true`)
* **Tavily** — web search tool for the research agent

##### 4. Run the Marimo notebook: [Demo](../car_demo.py)
```bash
# (venv) $
marimo edit car_demo.py
```
Work through the cells top to bottom, then click **Run multi-agent demo** to invoke the graph. Each run calls OpenAI and Tavily; ensure your OpenAI account has available quota.

* **Optional:** Shut down Marimo with `Ctrl+C` in the terminal running the editor.