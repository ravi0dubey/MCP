from __future__ import annotations
import os
import sqlite3
from fastmcp import FastMCP

mcp = FastMCP("maths_cal")
DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")
CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")

def _as_number(x):
    # Accept ints/floats or numeric strings ; raise clean errors otherwise
    if isinstance(x,(int,float)):
        return float(x)
    if isinstance(x,str):
        return float(x.strip())
    raise TypeError("Expected a number (int/float or numeric string)")


@mcp.tool()
async def add(a:float, b:float)-> float:
    """ return a + b."""
    return _as_number(a) + _as_number(b)

@mcp.tool()
async def subtract(a:float , b:float) -> float:
    """ return a - b """
    return _as_number(a) - _as_number(b)

@mcp.tool()
async def multiply(a:float , b:float) -> float:
    """ return a * b """
    return _as_number(a) * _as_number(b)

@mcp.tool()
async def divide(a:float , b:float) -> float:
    """ return a / b """
    try:
        if b == 0 :
            return 0
        else:
            return _as_number(a) / _as_number(b)
    except:
        return 0
    