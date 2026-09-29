"""Offline tests: tool logic plus the graph loop with a scripted fake LLM."""
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from app.graph import build_graph
from app.tools import calculator, convert_units, get_current_datetime


def test_calculator():
    assert calculator.invoke({"expression": "2 + 3 * 4"}) == "14"
    assert calculator.invoke({"expression": "1/0"}).startswith("Error")
    assert calculator.invoke({"expression": "__import__('os')"}).startswith("Error")


def test_convert_units():
    assert convert_units.invoke({"value": 1, "from_unit": "km", "to_unit": "m"}) == "1000 m"
    assert convert_units.invoke({"value": 100, "from_unit": "c", "to_unit": "f"}) == "212 F"
    assert convert_units.invoke({"value": 1, "from_unit": "kg", "to_unit": "m"}).startswith("Error")


def test_get_current_datetime():
    assert "UTC" in get_current_datetime.invoke({"timezone": "UTC"})
    assert get_current_datetime.invoke({"timezone": "Mars/Base"}).startswith("Error")


class FakeToolModel(GenericFakeChatModel):
    def bind_tools(self, tools, **kwargs):
        return self


def test_graph_runs_tool_then_answers():
    llm = FakeToolModel(messages=iter([
        AIMessage(content="", tool_calls=[{"name": "calculator", "args": {"expression": "6*7"}, "id": "call_1"}]),
        AIMessage(content="The answer is 42."),
    ]))
    app = build_graph(llm)
    result = app.invoke(
        {"messages": [HumanMessage("What is 6*7?")]},
        {"configurable": {"thread_id": "test"}},
    )
    tool_msgs = [m for m in result["messages"] if isinstance(m, ToolMessage)]
    assert tool_msgs[0].content == "42"
    assert result["messages"][-1].content == "The answer is 42."
