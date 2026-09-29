"""The three tools the agent can call."""
import ast
import operator
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from langchain_core.tools import tool

# --- Tool 1: calculator -----------------------------------------------------

_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _eval_node(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
        return _OPERATORS[type(node.op)](_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPERATORS:
        return _OPERATORS[type(node.op)](_eval_node(node.operand))
    raise ValueError("Only numbers and + - * / // % ** are allowed")


@tool
def calculator(expression: str) -> str:
    """Evaluate an arithmetic expression, e.g. '(12.5 * 4) / 3 + 2**8'."""
    try:
        result = _eval_node(ast.parse(expression, mode="eval").body)
    except (ValueError, SyntaxError, ZeroDivisionError) as exc:
        return f"Error: {exc}"
    return str(result)


# --- Tool 2: current date/time ----------------------------------------------


@tool
def get_current_datetime(timezone: str = "UTC") -> str:
    """Get the current date and time in an IANA timezone, e.g. 'Asia/Kolkata' or 'America/New_York'."""
    try:
        now = datetime.now(ZoneInfo(timezone))
    except ZoneInfoNotFoundError:
        return f"Error: unknown timezone '{timezone}'"
    return now.strftime("%A, %Y-%m-%d %H:%M:%S %Z")


# --- Tool 3: unit converter -------------------------------------------------

# Factors relative to a base unit per category (meters, kilograms).
_LENGTH = {"mm": 0.001, "cm": 0.01, "m": 1.0, "km": 1000.0, "in": 0.0254, "ft": 0.3048, "mi": 1609.344}
_WEIGHT = {"g": 0.001, "kg": 1.0, "lb": 0.45359237, "oz": 0.028349523125}


def _convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    to_celsius = {"c": lambda v: v, "f": lambda v: (v - 32) * 5 / 9, "k": lambda v: v - 273.15}
    from_celsius = {"c": lambda v: v, "f": lambda v: v * 9 / 5 + 32, "k": lambda v: v + 273.15}
    return from_celsius[to_unit](to_celsius[from_unit](value))


@tool
def convert_units(value: float, from_unit: str, to_unit: str) -> str:
    """Convert a value between units.

    Length: mm, cm, m, km, in, ft, mi. Weight: g, kg, lb, oz. Temperature: c, f, k.
    """
    src, dst = from_unit.lower(), to_unit.lower()
    for table in (_LENGTH, _WEIGHT):
        if src in table and dst in table:
            return f"{value * table[src] / table[dst]:.6g} {to_unit}"
    if src in {"c", "f", "k"} and dst in {"c", "f", "k"}:
        return f"{_convert_temperature(value, src, dst):.6g} {to_unit.upper()}"
    return f"Error: cannot convert '{from_unit}' to '{to_unit}'"


TOOLS = [calculator, get_current_datetime, convert_units]
