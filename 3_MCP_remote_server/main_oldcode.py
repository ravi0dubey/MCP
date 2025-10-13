from fastmcp import FastMCP
import random
import json
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "expense_db.db")
EXPENSE_CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "expense_categories.json")

# Create the FastMCP server instance
mcp = FastMCP("ExpenseTracker_Server")

# ExpenseDB creation
def init_db():
    print("inside init_db")
    with sqlite3.connect(DB_PATH) as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS expense_db
                  (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  expense_date TEXT NOT NULL,
                  expense_amount REAL NOT NULL,
                  expense_category TEXT NOT NULL,
                  expense_subcategory TEXT DEFAULT ' ',
                  note TEXT DEFAULT ''
                  )
    """)

init_db()

# Tool : Add Expense in expense_db
@mcp.tool()
def add_expense(date, amount, category, subcategory="", note=""):
    """
    Add a new expense entry to the database.
        Args:
    start_date : Date from which you want expenses in the list
    end_date   : End Date till you want expenses to be summarized

    Returns:
    It returns the dictionary of expenses done, date wise
    """
    print("inside add_expense")
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            "INSERT INTO expense_db(expense_date,expense_amount,expense_category,expense_subcategory,note)" \
            "VALUES(?,?,?,?,?)",(date,amount,category,subcategory,note)
        )
        return {"status":"ok", "id": cur.lastrowid}
    

# Tool : to List expense
@mcp.tool()
def list_expense(start_date,end_date):
    """
    Report expense incurred during the giving dates

    Args:
    start_date : Date from which you want expenses in the list
    end_date   : End Date till you want expenses to be summarized

    Returns:
    It returns the dictionary of expenses done, date wise
    """
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            """
            select id , expense_date, expense_amount, expense_category, expense_subcategory , note
            from expense_db
            where expense_date  between ? and ?
            order by id ASC
            """,
            (start_date,end_date)  
        )
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]



#Tool : Summarize the expense
@mcp.tool()
def summarize_expense(start_date, end_date, category = None):
    """
    To summarize the expense between the given date. If category is provided then breakdown the 
    expense based on category.

    Args:

    start_date : Date from which you want expenses in the list
    end_date   : End Date till you want expenses to be summarized
    catgory    : Category 

    Returns:
    It returns the dictionary of expenses done, date wise  based on the category
    """

    with sqlite3.connect(DB_PATH) as c:
        query = (
            """
            SELECT expense_category, SUM(expense_amount) AS total_amount
            FROM expense_db
            WHERE expense_date BETWEEN ? AND ?
            """
        )
        params = [start_date, end_date]

        if category:
            query += " AND expense_category = ?"
            params.append(category)

        query += " GROUP BY expense_category ORDER BY expense_category ASC"

        cur = c.execute(query,params)
        print(cur)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]

    


# Resource : Server information
@mcp.resource("expense://categories", mime_type="application/json")
def categories():
    # Read fresh each time so you can edit the file without restarting
    print("inside resource")
    with open(EXPENSE_CATEGORIES_PATH, "r", encoding="utf-8") as f:
        return f.read()
    

# Start the server
if __name__ == "__main__":
    print("inside main")
    mcp.run(transport="http", host ="127.0.0.1", port = 8000)
