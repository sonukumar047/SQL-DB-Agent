import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import math

# ── Enhanced CSS with Interactive Colors ────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    .hdr {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        color: #fff;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
        to { box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4); }
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: #fff;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #5a67d8, #6b46c1);
    }
    
    .stButton>button:active {
        transform: translateY(0px);
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .schema-table {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
        transition: border-color 0.3s ease;
    }
    
    .schema-table:hover {
        border-left-color: #f093fb;
    }
    
    .query-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border: 2px solid transparent;
        transition: border-color 0.3s ease;
    }
    
    .query-box:hover {
        border-color: #667eea;
    }
    
    .sidebar .stSelectbox {
        margin-bottom: 1rem;
    }
    
    .provider-card {
        background: linear-gradient(135deg, #fff 0%, #f8f9fa 100%);
        border-radius: 12px;
        padding: 1rem;
        border: 2px solid #e9ecef;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .provider-card:hover {
        border-color: #667eea;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
    }
    
    .provider-card.selected {
        border-color: #667eea;
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 50%);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    .model-badge {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: bold;
        display: inline-block;
        margin: 0.2rem 0.3rem 0.2rem 0;
        transition: transform 0.2s ease;
    }
    
    .model-badge:hover {
        transform: scale(1.05);
    }
    
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }
    
    .status-groq { background-color: #22c55e; }
    .status-ollama { background-color: #3b82f6; }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .main-content {
        padding: 1rem;
    }
    </style>""", unsafe_allow_html=True)

# ── Enhanced Header ───────────────────────────────────────────────────────────
def show_header():
    st.markdown("""
    <div class='hdr'>
        <h1>🤖 AI Database Query Assistant</h1>
        <p style='font-size: 1.2em; margin: 1rem 0;'>Transform natural language into powerful SQL queries</p>
        <p style='opacity: 0.9;'>✨ Ask questions in plain English → Get SQL + results instantly</p>
    </div>""", unsafe_allow_html=True)

# ── Provider Selection Component ──────────────────────────────────────────────
def show_provider_selection():
    """Show interactive provider and model selection"""
    st.markdown("### 🔧 AI Configuration")
    
    # Provider selection
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Choose AI Provider")
        provider = st.radio(
            "Select your preferred AI provider:",
            ["Groq", "Ollama"],
            key="ai_provider",
            help="Groq: Cloud-based, fast inference\nOllama: Local models, privacy-focused"
        )
    
    with col2:
        st.markdown("#### Model Selection")
        if provider == "Groq":
            from config import GROQ_MODELS
            model = st.selectbox(
                "Choose Groq model:",
                GROQ_MODELS,
                key="groq_model",
                help="Different models have varying capabilities and speeds"
            )
            st.markdown('<span class="status-indicator status-groq"></span>Groq Cloud API', unsafe_allow_html=True)
        else:
            from config import OLLAMA_MODELS
            model = st.selectbox(
                "Choose Ollama model:",
                OLLAMA_MODELS,
                key="ollama_model",
                help="Make sure the selected model is downloaded in Ollama"
            )
            st.markdown('<span class="status-indicator status-ollama"></span>Local Ollama', unsafe_allow_html=True)
    
    # Model info display
    with st.expander("ℹ️ Model Information"):
        if provider == "Groq":
            model_info = {
                "llama-3.3-70b-versatile": "Latest Llama model, excellent for complex queries",
                "llama-3.1-70b-versatile": "Powerful model with good reasoning capabilities",
                "llama-3.1-8b-instant": "Faster, lighter model for quick responses",
                "mixtral-8x7b-32768": "Mixture of Experts model, great for diverse tasks",
                "gemma2-9b-it": "Google's Gemma model, optimized for instruction following"
            }
        else:
            model_info = {
                "llama3.2": "Latest Llama model optimized for local deployment",
                "llama3.1": "Previous version of Llama, very capable",
                "codellama": "Specialized for code generation and understanding",
                "mistral": "Efficient model with good performance",
                "gemma2": "Google's open model, good balance of size and capability"
            }
        
        st.write(f"**{model}:** {model_info.get(model, 'Advanced language model')}")
    
    return provider, model

# ── Schema Statistics ─────────────────────────────────────────────────────────
def show_schema_stats(schema):
    if not schema:
        return
    
    total_tables = len(schema)
    total_columns = sum(len(info['columns']) for info in schema.values())
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='metric-card'>
            <h3 style='color: #667eea; margin: 0;'>📊 Tables</h3>
            <h2 style='margin: 0.5rem 0;'>{}</h2>
        </div>""".format(total_tables), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='metric-card'>
            <h3 style='color: #764ba2; margin: 0;'>🗂️ Columns</h3>
            <h2 style='margin: 0.5rem 0;'>{}</h2>
        </div>""".format(total_columns), unsafe_allow_html=True)
    
    with col3:
        avg_cols = round(total_columns / total_tables, 1) if total_tables > 0 else 0
        st.markdown("""
        <div class='metric-card'>
            <h3 style='color: #f093fb; margin: 0;'>📈 Avg Cols/Table</h3>
            <h2 style='margin: 0.5rem 0;'>{}</h2>
        </div>""".format(avg_cols), unsafe_allow_html=True)

# ── Graphical Schema Viewer ──────────────────────────────────────────────────
def create_schema_network_graph(schema):
    """Create an interactive network graph using Plotly"""
    if not schema:
        st.info("No schema available to display.")
        return
    
    try:
        # Create nodes and edges
        nodes = []
        edges = []
        node_positions = {}
        
        # Add nodes (tables)
        table_names = list(schema.keys())
        for i, (table, info) in enumerate(schema.items()):
            nodes.append({
                'id': table,
                'label': table,
                'columns': len(info['columns']),
                'title': f"Table: {table}<br>Columns: {len(info['columns'])}"
            })
        
        # Infer relationships based on foreign key naming conventions
        for table, info in schema.items():
            for column in info['columns']:
                if column.lower().endswith('_id') and column.lower() != 'id':
                    potential_ref = column[:-3]
                    if potential_ref in table_names:
                        edges.append({
                            'from': table,
                            'to': potential_ref,
                            'title': f"{table}.{column} → {potential_ref}.id"
                        })
        
        # Create Plotly network graph
        fig = go.Figure()
        
        # Simple circular layout for nodes
        n_nodes = len(nodes)
        for i, node in enumerate(nodes):
            if n_nodes == 1:
                x, y = 0, 0
            else:
                angle = 2 * math.pi * i / n_nodes
                x = math.cos(angle)
                y = math.sin(angle)
            node_positions[node['id']] = (x, y)
        
        # Add edges if any exist
        if edges:
            edge_x = []
            edge_y = []
            
            for edge in edges:
                x0, y0 = node_positions[edge['from']]
                x1, y1 = node_positions[edge['to']]
                edge_x.extend([x0, x1, None])
                edge_y.extend([y0, y1, None])
            
            fig.add_trace(go.Scatter(
                x=edge_x, y=edge_y,
                line=dict(width=2, color='rgba(125,125,125,0.5)'),
                hoverinfo='none',
                mode='lines',
                name='Relationships'
            ))
        
        # Add nodes
        node_x = [node_positions[node['id']][0] for node in nodes]
        node_y = [node_positions[node['id']][1] for node in nodes]
        node_text = [node['label'] for node in nodes]
        node_sizes = [max(30, min(80, node['columns'] * 10)) for node in nodes]
        
        fig.add_trace(go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            text=node_text,
            textposition="middle center",
            textfont=dict(size=12, color='white'),
            hovertemplate='<b>%{text}</b><br>Columns: %{customdata}<extra></extra>',
            customdata=[node['columns'] for node in nodes],
            marker=dict(
                size=node_sizes,
                color='#667eea',
                line=dict(width=2, color='white'),
                opacity=0.8
            ),
            name='Tables'
        ))
        
        fig.update_layout(
            title={
                'text': f'🔗 Database Schema Relationship Graph ({len(nodes)} tables)',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18}
            },
            showlegend=False,
            hovermode='closest',
            margin=dict(b=40,l=40,r=40,t=80),
            annotations=[ 
                dict(
                    text=f"Found {len(edges)} relationships • Node size = column count",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.5, y=-0.1,
                    xanchor='center', yanchor='top',
                    font=dict(color='gray', size=12)
                )
            ],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor='white',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        if edges:
            st.subheader("🔗 Detected Relationships")
            rel_df = pd.DataFrame([
                {"From Table": edge['from'], "To Table": edge['to'], "Relationship": edge['title']}
                for edge in edges
            ])
            st.dataframe(rel_df, use_container_width=True)
        else:
            st.info("💡 No relationships detected. Relationships are inferred from columns ending with '_id'")
            
    except Exception as e:
        st.error(f"Error creating network graph: {str(e)}")
        st.info("Displaying table list instead:")
        st.write("**Tables in schema:**")
        for table in schema.keys():
            st.write(f"• {table}")

# ── Column Types Analysis ────────────────────────────────────────────────────
def show_column_types_analysis(schema):
    """Analyze column types across all tables"""
    try:
        type_counts = {}
        type_details = []
        
        for table, info in schema.items():
            for column, col_type in info['types'].items():
                simple_type = col_type.split('(')[0].lower().strip()
                type_counts[simple_type] = type_counts.get(simple_type, 0) + 1
                type_details.append({
                    'Table': table,
                    'Column': column,
                    'Full_Type': col_type,
                    'Simple_Type': simple_type
                })
        
        if not type_counts:
            st.warning("No column type data available.")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_pie = px.pie(
                values=list(type_counts.values()),
                names=list(type_counts.keys()),
                title="Distribution of Column Types",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie.update_layout(height=400)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            fig_bar = px.bar(
                x=list(type_counts.keys()),
                y=list(type_counts.values()),
                title="Column Type Counts",
                color=list(type_counts.values()),
                color_continuous_scale='viridis'
            )
            fig_bar.update_layout(
                xaxis_title="Data Type",
                yaxis_title="Count",
                height=400
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        st.subheader("📊 Detailed Breakdown")
        
        summary_df = pd.DataFrame([
            {
                "Data Type": k, 
                "Count": v, 
                "Percentage": f"{v/sum(type_counts.values())*100:.1f}%"
            }
            for k, v in sorted(type_counts.items(), key=lambda x: x[1], reverse=True)
        ])
        st.dataframe(summary_df, use_container_width=True)
        
        with st.expander("🔍 View All Columns by Type"):
            detail_df = pd.DataFrame(type_details)
            
            selected_type = st.selectbox(
                "Filter by type:",
                ['All'] + list(sorted(type_counts.keys()))
            )
            
            if selected_type != 'All':
                filtered_df = detail_df[detail_df['Simple_Type'] == selected_type]
            else:
                filtered_df = detail_df
            
            st.dataframe(
                filtered_df[['Table', 'Column', 'Full_Type']], 
                use_container_width=True
            )
            
    except Exception as e:
        st.error(f"Error analyzing column types: {str(e)}")
        st.info("Raw schema data:")
        st.json(schema)

# ── Enhanced Schema Viewer ──────────────────────────────────────────────────
def schema_expander(schema: dict):
    if not schema:
        st.info("🔍 No schema loaded. Please select a database first.")
        return
    
    st.subheader("🗂️ Database Schema Details")
    
    show_schema_stats(schema)
    
    view_option = st.radio(
        "Choose view:",
        ["📋 Table Details", "🔗 Relationship Graph", "📊 Column Types Analysis"],
        horizontal=True
    )
    
    if view_option == "📋 Table Details":
        for table, info in schema.items():
            with st.expander(f"📅 {table} ({len(info['columns'])} columns)", expanded=False):
                df = pd.DataFrame([
                    {"Column": c, "Type": info['types'][c]} 
                    for c in info['columns']
                ])
                
                def highlight_types(val):
                    if 'int' in val.lower():
                        return 'background-color: #e3f2fd'
                    elif 'varchar' in val.lower() or 'text' in val.lower():
                        return 'background-color: #f3e5f5'
                    elif 'date' in val.lower() or 'time' in val.lower():
                        return 'background-color: #e8f5e8'
                    else:
                        return 'background-color: #fff3e0'
                
                styled_df = df.style.map(highlight_types, subset=['Type'])
                st.dataframe(styled_df, use_container_width=True)
    
    elif view_option == "🔗 Relationship Graph":
        create_schema_network_graph(schema)
    
    elif view_option == "📊 Column Types Analysis":
        show_column_types_analysis(schema)

# ── Enhanced History Display ─────────────────────────────────────────────────
def show_enhanced_history(history):
    if not history:
        st.info("📜 No query history yet. Run some queries to see them here!")
        return
    
    st.subheader("📜 Query History")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Queries", len(history))
    with col2:
        avg_time = sum(float(h['time'].replace('s', '')) for h in history) / len(history)
        st.metric("Avg Execution Time", f"{avg_time:.3f}s")
    
    for i, item in enumerate(reversed(history)):
        with st.expander(f"Query {len(history)-i}: {item['nl'][:50]}...", expanded=False):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**Database:** {item['db']}")
                st.write(f"**Provider:** {item.get('provider', 'N/A')} - {item.get('model', 'N/A')}")
                st.write(f"**Question:** {item['nl']}")
                st.code(item['sql'], language='sql')
            
            with col2:
                st.metric("Execution Time", item['time'])

# ── Save History ─────────────────────────────────────────────────────────────
def save_history(nl, sql, db, t, provider, model, result_count=0):
    st.session_state.history.append({
        "nl": nl, 
        "sql": sql, 
        "db": db, 
        "provider": provider,
        "model": model,
        "time": f"{t:.3f}s",
        "result_count": result_count,
        "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    st.session_state.history = st.session_state.history[-20:]

# ── Query Result Display ─────────────────────────────────────────────────────
def display_query_results(df, execution_time):
    """Enhanced display for query results"""
    if df.empty:
        st.info("📭 No rows returned by the query.")
        return
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Rows Returned", len(df))
    with col2:
        st.metric("Columns", len(df.columns))
    with col3:
        st.metric("Execution Time", f"{execution_time:.3f}s")
    
    st.subheader("📊 Query Results")
    
    view_option = st.radio(
        "View options:",
        ["📋 Table View", "📈 Quick Charts (if applicable)"],
        horizontal=True
    )
    
    if view_option == "📋 Table View":
        st.dataframe(df, use_container_width=True)
        
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"query_results_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    elif view_option == "📈 Quick Charts (if applicable)":
        numeric_cols = df.select_dtypes(include=['number']).columns
        
        if len(numeric_cols) > 0:
            chart_col = st.selectbox("Select column for chart:", numeric_cols)
            chart_type = st.selectbox("Chart type:", ["Histogram", "Box Plot"])
            
            if chart_type == "Histogram":
                fig = px.histogram(df, x=chart_col, title=f"Distribution of {chart_col}")
                st.plotly_chart(fig, use_container_width=True)
            else:
                fig = px.box(df, y=chart_col, title=f"Box Plot of {chart_col}")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No numeric columns available for charting.")
        
        st.dataframe(df, use_container_width=True)
