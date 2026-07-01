import marimo

__generated_with = "0.23.12"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import os

    from dotenv import load_dotenv

    load_dotenv()

    for var in ("OPENAI_API_KEY", "LANGCHAIN_API_KEY", "TAVILY_API_KEY"):
        if not os.environ.get(var):
            raise EnvironmentError(
                f"{var} is not set; add it to .env in the repo root"
            )

    os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")
    os.environ.setdefault("LANGCHAIN_PROJECT", "Multi-agent Collaboration")

    return


@app.cell
def _():
    from typing import Literal

    from langchain_tavily import TavilySearch
    from langchain_core.messages import AIMessage, HumanMessage
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_openai import ChatOpenAI
    from langgraph.graph import END, START, MessagesState, StateGraph
    from langgraph.prebuilt import ToolNode

    def create_agent(llm, tools, system_message: str):
        """Create an agent."""
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful AI assistant, collaborating with other assistants."
                    " Use the provided tools to progress towards answering the question."
                    " If you are unable to fully answer, that's OK, another assistant with different tools "
                    " will help where you left off. Execute what you can to make progress."
                    " If you or any of the other assistants have the final answer or deliverable,"
                    " prefix your response with FINAL ANSWER so the team knows to stop."
                    " You have access to the following tools: {tool_names}.\n{system_message}",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        prompt = prompt.partial(system_message=system_message)
        prompt = prompt.partial(tool_names=", ".join([tool.name for tool in tools]))
        return prompt | llm.bind_tools(tools)

    return (
        AIMessage,
        ChatOpenAI,
        END,
        HumanMessage,
        Literal,
        MessagesState,
        START,
        StateGraph,
        TavilySearch,
        ToolNode,
        create_agent,
    )


@app.cell
def _(ChatOpenAI, TavilySearch, create_agent):
    model = ChatOpenAI(model="gpt-4o-mini")

    tavily_tool = TavilySearch(max_results=3)
    research_tools = [tavily_tool]

    research_agent = create_agent(
        model,
        research_tools,
        "You are a research assistant. Search the web for current information.",
    )
    chart_agent = create_agent(
        model,
        [],
        "You are a chart assistant. Describe or outline charts from the research provided.",
    )

    return chart_agent, model, research_agent, research_tools, tavily_tool


@app.cell
def _(
    AIMessage,
    END,
    Literal,
    MessagesState,
    START,
    StateGraph,
    ToolNode,
    chart_agent,
    research_agent,
    research_tools,
):
    def research_node(state: MessagesState):
        response = research_agent.invoke(state)
        return {"messages": [response]}

    def chart_node(state: MessagesState):
        response = chart_agent.invoke(state)
        return {"messages": [response]}

    def research_router(
        state: MessagesState,
    ) -> Literal["tools", "chart_generator", "end"]:
        last_message = state["messages"][-1]
        if isinstance(last_message, AIMessage) and last_message.tool_calls:
            return "tools"
        if "FINAL ANSWER" in last_message.content:
            return "end"
        return "chart_generator"

    def chart_router(state: MessagesState) -> Literal["researcher", "end"]:
        last_message = state["messages"][-1]
        if "FINAL ANSWER" in last_message.content:
            return "end"
        return "researcher"

    tool_node = ToolNode(research_tools)

    graph_builder = StateGraph(MessagesState)
    graph_builder.add_node("researcher", research_node)
    graph_builder.add_node("chart_generator", chart_node)
    graph_builder.add_node("call_tool", tool_node)

    graph_builder.add_conditional_edges(
        "researcher",
        research_router,
        {
            "tools": "call_tool",
            "chart_generator": "chart_generator",
            "end": END,
        },
    )
    graph_builder.add_conditional_edges(
        "chart_generator",
        chart_router,
        {"researcher": "researcher", "end": END},
    )
    graph_builder.add_edge("call_tool", "researcher")
    graph_builder.add_edge(START, "researcher")

    graph = graph_builder.compile()

    return (graph,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Run the demo

    The graph calls **OpenAI** and **Tavily** on each run. Click **Run** when ready.

    If you see `insufficient_quota` / 429, your OpenAI account has no remaining
    credits — check [billing](https://platform.openai.com/account/billing).
    """)
    return


@app.cell
def _(mo):
    run_btn = mo.ui.run_button(label="Run multi-agent demo")
    query = mo.ui.text_area(
        label="Query",
        value="Research recent AI agent frameworks and outline a comparison chart.",
        full_width=True,
    )
    return query, run_btn


@app.cell
def _(HumanMessage, graph, mo, query, run_btn):
    mo.stop(not run_btn.value)

    try:
        result = graph.invoke({"messages": [HumanMessage(content=query.value)]})
        output = result["messages"][-1].content
    except Exception as exc:
        error_text = str(exc)
        if "insufficient_quota" in error_text or "429" in error_text:
            mo.output(
                mo.callout(
                    "OpenAI quota exceeded. Add billing credits or use a key with "
                    "available balance, then click Run again.",
                    kind="danger",
                )
            )
        else:
            mo.output(mo.callout(f"Demo failed: {error_text}", kind="danger"))
        return None, None

    output

    return output, result


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
