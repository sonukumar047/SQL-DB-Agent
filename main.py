import streamlit as st
import pandas as pd
from groq_helpers import nl_to_sql
from sql_helpers import get_db_schema, run_sql_query, validate_sql
from ui_components import (
    inject_css, show_header, schema_expander, save_history, 
    show_enhanced_history, display_query_results
)
from config import DATABASES

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI DB Assistant", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_css()
show_header()

# ── Session State ──────────────────────────────────────────────────────────────
if "schema" not in st.session_state: 
    st.session_state.schema = {}
if "history" not in st.session_state: 
    st.session_state.history = []
if "curr_db" not in st.session_state: 
    st.session_state.curr_db = None
if "show_schema" not in st.session_state: 
    st.session_state.show_schema = False
if "show_hist" not in st.session_state: 
    st.session_state.show_hist = False

# ── Enhanced Sidebar ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎛️ Control Panel")
    
    # Database selection
    db = st.selectbox(
        "🗄️ Select Database", 
        DATABASES, 
        key="db_select",
        help="Choose the database you want to query"
    )
    
    # Schema loading with better UX
    if db != st.session_state.curr_db:
        with st.spinner(f"🔄 Loading schema for {db}..."):
            try:
                st.session_state.schema = get_db_schema(db)
                st.session_state.curr_db = db
                st.success(f"✅ Schema loaded for {db}!")
            except Exception as e:
                st.session_state.schema = {}
                st.error(f"❌ Error loading schema: {e}")
    
    st.markdown("---")
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 View Schema", use_container_width=True):
            st.session_state.show_schema = True
    
    with col2:
        if st.button("📜 View History", use_container_width=True):
            st.session_state.show_hist = True
    
    # Quick stats in sidebar
    if st.session_state.schema:
        st.markdown("### 📊 Quick Stats")
        st.metric("Tables", len(st.session_state.schema))
        total_cols = sum(len(info['columns']) for info in st.session_state.schema.values())
        st.metric("Total Columns", total_cols)
    
    st.markdown("---")
    st.markdown("### 💡 Tips")
    with st.expander("Query Examples"):
        st.markdown("""
        - "Show all users"
        - "Find products with price > 100"
        - "Count orders by status"
        - "Join users and their orders"
        - "Show revenue by month"
        """)

# ── Main Content Area ──────────────────────────────────────────────────────────
# Query input section
st.markdown("### 💬 Ask Your Question")
st.markdown('<div class="query-box">', unsafe_allow_html=True)

col1, col2 = st.columns([4, 1])
with col1:
    nl_query = st.text_area(
        "Type your question in plain English:",
        height=100,
        placeholder="e.g., 'Show me all customers who placed orders in the last month'"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)  # Spacing
    run_button = st.button("🚀 Run Query", use_container_width=True, type="primary")

st.markdown('</div>', unsafe_allow_html=True)

# Query execution
if run_button and nl_query:
    if not st.session_state.schema:
        st.error("❌ Please load a database schema first by selecting a database.")
    else:
        try:
            # Generate SQL
            with st.spinner("🧠 Generating SQL..."):
                sql = nl_to_sql(nl_query, db, st.session_state.schema)
            
            # Validate SQL
            ok, msg = validate_sql(sql)
            if not ok:
                st.error(f"❌ SQL Validation Failed: {msg}")
            else:
                # Display generated SQL
                st.markdown("### 🔧 Generated SQL")
                st.code(sql, language="sql")
                
                # Execute query
                with st.spinner("⚡ Executing query..."):
                    df, execution_time = run_sql_query(sql, db)
                
                # Save to history
                save_history(nl_query, sql, db, execution_time, len(df))
                
                # Display results
                st.success(f"✅ Query executed successfully!")
                display_query_results(df, execution_time)
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# ── Schema and History Display ─────────────────────────────────────────────────
if st.session_state.get("show_schema"):
    st.markdown("---")
    schema_expander(st.session_state.schema)
    st.session_state.show_schema = False

if st.session_state.get("show_hist"):
    st.markdown("---")
    show_enhanced_history(st.session_state.history)
    st.session_state.show_hist = False

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>🤖 Powered by AI • Built with Streamlit • Enhanced Database Query Experience</p>
</div>
""", unsafe_allow_html=True)
