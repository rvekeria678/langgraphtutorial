from langchain_core.tools import tool

@tool
def add(a: int, b: int) -> int:
    """Adds a and b."""
    return a + b

@tool
def subtract(a: int, b: int) -> int:
    """Subtract b from a"""
    return a - b

@tool
def multiply(a: int, b: int) -> int:
    """Multiplies a and b."""
    return a * b

@tool
def divide(a: int, b: int) -> float:
    """Divides a by b."""
    return a / b