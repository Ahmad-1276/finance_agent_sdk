import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import time

# Try to import our modules
try:
    from agent import chat_with_agent
    from db import db
except ImportError as e:
    st.error(f"Import error: {e}")
    st.info("Make sure you have db.py and agent.py in the same directory")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="AI Finance Agent",
    page_icon="💰",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
    }
    .chat-user {
        background-color: #e3f2fd;
        padding: 10px;
        border-radius: 10px;
        margin: 5px;
        border-left: 4px solid #1E88E5;
    }
    .chat-agent {
        background-color: #f5f5f5;
        padding: 10px;
        border-radius: 10px;
        margin: 5px;
        border-left: 4px solid #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Header
st.markdown('<h1 class="main-header">💰 AI Finance Agent</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📊 Quick Stats")
    
    # Display metrics
    total = db.get_total()
    avg = db.get_average()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Spending", f"${total:.2f}")
    with col2:
        st.metric("Average", f"${avg:.2f}")
    
    st.divider()
    
    st.header("➕ Add Expense")
    
    # Manual expense form
    with st.form("expense_form"):
        amount = st.number_input("Amount", min_value=0.01, step=0.01, format="%.2f")
        category = st.selectbox(
            "Category",
            ["food", "transport", "shopping", "entertainment", "bills", "general"]
        )
        note = st.text_input("Note (optional)")
        
        submitted = st.form_submit_button("Add Expense")
        if submitted:
            result = db.add_expense(amount, category, note)
            st.success(result)
            time.sleep(1)
            st.rerun()
    
    st.divider()
    
    # Quick actions
    st.header("⚡ Quick Actions")
    
    if st.button("View All Expenses"):
        expenses = db.get_all_expenses()
        if expenses:
            df = pd.DataFrame(expenses, columns=['ID', 'Amount', 'Category', 'Note', 'Date'])
            st.dataframe(df)
        else:
            st.info("No expenses yet")
    
    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

# Main tabs
tab1, tab2 = st.tabs(["💬 Chat", "📈 Analytics"])

# Tab 1: Chat Interface
with tab1:
    st.subheader("Chat with AI Finance Agent")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for role, message in st.session_state.chat_history:
            if role == "user":
                st.markdown(f'<div class="chat-user"><b>You:</b> {message}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-agent"><b>Agent:</b> {message}</div>', unsafe_allow_html=True)
    
    # Quick commands
    st.subheader("Quick Commands")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("💰 Total"):
            response = chat_with_agent("total spending")
            st.session_state.chat_history.append(("user", "total spending"))
            st.session_state.chat_history.append(("agent", response))
            st.rerun()
    
    with col2:
        if st.button("📊 Average"):
            response = chat_with_agent("average spending")
            st.session_state.chat_history.append(("user", "average spending"))
            st.session_state.chat_history.append(("agent", response))
            st.rerun()
    
    with col3:
        if st.button("📝 Recent"):
            response = chat_with_agent("show recent expenses")
            st.session_state.chat_history.append(("user", "show recent expenses"))
            st.session_state.chat_history.append(("agent", response))
            st.rerun()
    
    with col4:
        if st.button("📁 Categories"):
            response = chat_with_agent("analyze spending by category")
            st.session_state.chat_history.append(("user", "analyze spending by category"))
            st.session_state.chat_history.append(("agent", response))
            st.rerun()
    
    # Chat input
    st.subheader("Send Message")
    user_input = st.text_input(
        "Type your message here...",
        placeholder="e.g., 'I spent 50 on lunch'",
        label_visibility="collapsed"
    )
    
    col1, col2 = st.columns([4, 1])
    with col1:
        if st.button("Send", type="primary", use_container_width=True) and user_input:
            with st.spinner("Thinking..."):
                response = chat_with_agent(user_input)
                st.session_state.chat_history.append(("user", user_input))
                st.session_state.chat_history.append(("agent", response))
                st.rerun()

# Tab 2: Analytics
with tab2:
    st.subheader("📈 Spending Analytics")
    
    # Get expenses
    expenses = db.get_all_expenses()
    
    if expenses:
        # Create DataFrame
        df = pd.DataFrame(expenses, columns=['id', 'amount', 'category', 'note', 'date'])
        df['date'] = pd.to_datetime(df['date'])
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart
            category_totals = df.groupby('category')['amount'].sum().reset_index()
            fig1 = px.pie(category_totals, values='amount', names='category', 
                         title="Spending by Category")
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Bar chart
            fig2 = px.bar(category_totals.sort_values('amount', ascending=False), 
                         x='category', y='amount',
                         title="Total by Category")
            st.plotly_chart(fig2, use_container_width=True)
        
        # Recent expenses table
        st.subheader("Recent Expenses")
        recent_df = df.head(20)[['date', 'amount', 'category', 'note']].copy()
        recent_df['date'] = recent_df['date'].dt.strftime('%Y-%m-%d %H:%M')
        st.dataframe(recent_df, use_container_width=True, hide_index=True)
        
    else:
        st.info("No expenses recorded yet. Start by adding some expenses!")