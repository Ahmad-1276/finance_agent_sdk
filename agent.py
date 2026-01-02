import os
import sys

# Try to import agents SDK
try:
    from agents import Agent, Runner, function_tool
except ImportError:
    print("❌ OpenAI Agents SDK not installed. Install with: pip install openai-agents")
    sys.exit(1)

from db import db

# Set your OpenAI API key (REPLACE WITH YOUR KEY)
os.environ["OPENAI_API_KEY"] = "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"

# Define tools
@function_tool
def record_expense(amount: float, category: str = "general", note: str = "") -> str:
    """Record a new expense"""
    return db.add_expense(amount, category, note)

@function_tool
def show_total_spending() -> str:
    """Show total amount spent"""
    total = db.get_total()
    return f"💰 Total spending: ${total:.2f}"

@function_tool
def show_average_spending() -> str:
    """Show average spending"""
    avg = db.get_average()
    return f"📊 Average spending: ${avg:.2f}"

@function_tool
def list_recent_expenses(limit: int = 10) -> str:
    """Show recent expenses"""
    expenses = db.get_recent_expenses(limit)
    
    if not expenses:
        return "No expenses recorded yet."
    
    result = "📝 Recent expenses:\n"
    for exp in expenses:
        result += f"  • ${exp[1]:.2f} - {exp[2]}"
        if exp[3]:
            result += f" ({exp[3]})"
        result += f" - {exp[4]}\n"
    return result

@function_tool
def analyze_spending_by_category() -> str:
    """Analyze spending by category"""
    categories = db.get_expenses_by_category()
    
    if not categories:
        return "No expenses recorded yet."
    
    result = "📊 Spending by category:\n"
    for category, data in categories.items():
        result += f"  • {category.title()}: ${data['total']:.2f} ({data['count']} items)\n"
    return result

# Create agent
finance_agent = Agent(
    name="Finance Assistant",
    instructions="""You are a personal finance assistant. Help users track and analyze expenses.

    Available tools:
    1. record_expense - Record a new expense (amount is required)
    2. show_total_spending - Show total spending
    3. show_average_spending - Show average expense
    4. list_recent_expenses - Show recent expenses
    5. analyze_spending_by_category - Analyze spending by category

    Rules:
    - When user mentions spending money, use record_expense
    - Extract amount, category, and note from their message
    - If category isn't specified, use "general"
    - For total queries, use show_total_spending
    - For average queries, use show_average_spending
    - For recent expenses, use list_recent_expenses
    - For category analysis, use analyze_spending_by_category
    - Be helpful and concise""",
    tools=[
        record_expense,
        show_total_spending,
        show_average_spending,
        list_recent_expenses,
        analyze_spending_by_category
    ],
    model="gpt-4.1-mini"
)

def chat_with_agent(user_input: str) -> str:
    """Chat with the finance agent"""
    try:
        result = Runner.run_sync(finance_agent, user_input)
        return result.final_output
    except Exception as e:
        return f"❌ Error: {str(e)}"