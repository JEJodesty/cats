# [Multi-Agent Collaboration (MAC) for CATs Templated Demo](../car_demo.py)

**Description:** LangGraph demo with collaborating LLM agents (research + chart outline). Separate from the CAT mesh in [DEMO.md](./DEMO.md)—no IPFS, Docker, or CAT node required.
**Purpose:** *CAT Order Composition*

#### Background

#### **Multi-Agent Collaboration (MAC) for CATs using Content-Addressable Router (CAR) facilitated by the Architectural purpose of CATs as a Function**

- **Design Description**
  - CATs and LangGraphs integration can enable a row wise business function as a Chart Tool of Multi-Agent Collaboration (MAC) if CAT Orders act as a Transfer (Network) Function implemented as an OOP Command Pattern for which CATs Ingress and Egress sub-processes can be executed by CATs’ Content-Addressable Router (CAR).
  - *[Design context: June, Week 24](../articles.md#june)*
  - **Architectural Considerations:** CATs can inform business decisions given the following:
    - **Governance Plane: z(t)** - enables Stewardship of a Data Product Supply Network of CATs represented as a Directed Acyclic Graph of Data Product Supply
      - A GreyBox Model for as a feature parameterized Tensor Field with process variable (PV) as label
      - The business function is a CATs Control & Action Matrix - a 2 dimensional representation of 3 dimensional space
      - **Control Plane: y(t)** [aka Content-Addressable Router (CAR)] - enables Networking of what is Produced as a result of Science & Engineering CATs
        - CAR integrated with LangGraphs Router.
        - cadCAD (Network) Policies aka “Algorithmic Suggestions” can be deployed on LangGraphs Agent Nodes with specified Domain-Name references as Rule Asset RIDs
        - **Action Plane: x(t)** - enables the Science & Engineering of Data Transformation as Computational Processing, a.k.a. CATs
          - CAT Functions can be defined as LangGraph Call Tools executed by LangGraphs Tool Node
          - CAT Factory produces CAT Executors integrated with LangGraphs Tool Executor.
- **Status:** This experiment implements **Action/Control-plane orchestration patterns only** (multi-agent graph, routers, `ToolNode`). **CAR**, **CAT Order** composition, BOM governance, and cadCAD policy nodes are **not yet integrated**. `[cats_demo.py](../cats_demo.py)` remains the demo of the mesh as built today; `[car_demo.py](../car_demo.py)` is an early LangGraph shell toward the June 2024 MAC/CAR vision.

#### Demonstrates the following

`car_demo.py` builds a small multi-agent collaboration graph using LangChain + LangGraph:

1. Two specialized agents sharing one conversation (MessagesState):
  - Researcher — has Tavily web search; gathers current information
  - Chart generator — no tools; turns research into a chart outline/description
2. Orchestration via a state graph:
  - researcher → may call Tavily (call_tool) → back to researcher
  - → hands off to chart_generator
  - → can loop back to researcher until someone emits FINAL ANSWER
  - Routers decide: run tools, switch agents, or stop
3. Operational wiring:
  - API keys from `.env` (OpenAI, LangChain/LangSmith, Tavily)
  - LangSmith tracing (LANGCHAIN_TRACING_V2, project "Multi-agent Collaboration")
  - Marimo UI with a Run button so the graph doesn’t fire on every cell rerun

#### Steps:

##### 1. [Create Virtual Environment](./ENV.md)

```bash
# CATs working directory
cd cats
python -m venv ./venv
```

##### 2. Activate Virtual Environment and install dependencies:

```bash
source ./venv/bin/activate
# (venv) $
pip install -e ".[ops]"
pip install -r requirements-mac.txt
```

The base install includes `python-dotenv`; `[ops]` adds Marimo; `requirements-mac.txt`
adds LangChain/LangGraph packages used only by this experiment.

##### 3. Configure API keys *in the repo root* (`.env` is gitignored):

```bash
OPENAI_API_KEY=sk-...
LANGCHAIN_API_KEY=...
TAVILY_API_KEY=...
```

- **OpenAI** — LLM calls (`gpt-4o-mini` by default in the notebook)
- **LangChain / LangSmith** — optional tracing (`LANGCHAIN_TRACING_V2=true`)
- **Tavily** — web search tool for the research agent

##### 4. Run the Marimo notebook: [Demo](../car_demo.py)

```bash
# (venv) $
marimo edit car_demo.py
```

Work through the cells top to bottom, then click **Run multi-agent demo** to invoke the graph. Each run calls OpenAI and Tavily; ensure your OpenAI account has available quota.

- **Optional:** Shut down Marimo with `Ctrl+C` in the terminal running the editor.