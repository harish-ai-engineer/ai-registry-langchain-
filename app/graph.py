"""LangGraph agent: an LLM node and a tool node wired in a loop.

    START -> agent --(tool calls?)--> tools -> agent -> ... -> END
"""
from langchain_core.messages import SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from app.config import ANTHROPIC_MODEL, LLM_PROVIDER, MAX_TOKENS, OPENAI_MODEL, SYSTEM_PROMPT
from app.tools import TOOLS


def make_llm():
    """Create the chat model for the provider set in LLM_PROVIDER."""
    if LLM_PROVIDER == "openai":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(model=OPENAI_MODEL)
    if LLM_PROVIDER == "anthropic":
        from langchain_anthropic import ChatAnthropic

        return ChatAnthropic(model=ANTHROPIC_MODEL, max_tokens=MAX_TOKENS)
    raise ValueError(f"Unknown LLM_PROVIDER '{LLM_PROVIDER}' (use 'openai' or 'anthropic')")


def build_graph(llm=None):
    """Compile the agent graph. Pass `llm` to inject a fake model in tests."""
    if llm is None:
        llm = make_llm()
    llm_with_tools = llm.bind_tools(TOOLS)

    def agent(state: MessagesState):
        messages = [SystemMessage(SYSTEM_PROMPT), *state["messages"]]
        return {"messages": [llm_with_tools.invoke(messages)]}

    graph = StateGraph(MessagesState)
    graph.add_node("agent", agent)
    graph.add_node("tools", ToolNode(TOOLS))

    graph.add_edge(START, "agent")
    # Routes to "tools" if the last AI message has tool calls, else to END.
    graph.add_conditional_edges("agent", tools_condition, {"tools": "tools", END: END})
    graph.add_edge("tools", "agent")

    # MemorySaver keeps conversation history per thread_id.
    return graph.compile(checkpointer=MemorySaver())
