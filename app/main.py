"""CLI chat application for the LangGraph agent.

Run:  python -m app.main
"""
import uuid

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from app.graph import build_graph


def _text_of(message: AIMessage) -> str:
    """Return only the text parts of a (possibly multi-part) message."""
    if isinstance(message.content, str):
        return message.content
    return "".join(b.get("text", "") for b in message.content if b.get("type") == "text")


def main() -> None:
    app = build_graph()
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}

    print("Assistant ready (tools: calculator, get_current_datetime, convert_units).")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if user_input.lower() in {"exit", "quit"}:
            break
        if not user_input:
            continue

        # stream_mode="updates" yields each node's output as it finishes.
        for update in app.stream({"messages": [HumanMessage(user_input)]}, config, stream_mode="updates"):
            for node, output in update.items():
                for msg in output["messages"]:
                    if isinstance(msg, AIMessage):
                        for call in msg.tool_calls:
                            print(f"  [tool call] {call['name']}({call['args']})")
                        if text := _text_of(msg):
                            print(f"Assistant: {text}\n")
                    elif isinstance(msg, ToolMessage):
                        print(f"  [tool result] {msg.content}")


if __name__ == "__main__":
    main()
