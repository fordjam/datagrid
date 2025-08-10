"""
Streamlit AgGrid Data Table Demo
A comprehensive demonstration of interactive data tables with aggregations
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our custom modules
from data.sample_data import generate_sample_data, get_aggregation_demo_data
from components.aggrid_table import create_aggrid_table, create_pivot_table, create_summary_cards

# Page configuration
st.set_page_config(
    page_title="AgGrid Demo - Interactive Data Tables",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #ecf0f1;
        padding-bottom: 0.5rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">📊 AgGrid Interactive Data Tables Demo</h1>', 
               unsafe_allow_html=True)
    
    st.markdown("""
    This demo showcases the power of **streamlit-aggrid** for creating interactive data tables 
    with advanced features like sorting, filtering, grouping, and aggregations.
    """)
    
    # Sidebar configuration
    st.sidebar.title("⚙️ Configuration")
    
    # Data options
    st.sidebar.subheader("Data Options")
    data_size = st.sidebar.selectbox(
        "Dataset Size",
        options=[100, 500, 1000, 2000],
        index=1,
        help="Choose the number of records to display"
    )
    
    # Table configuration
    st.sidebar.subheader("Table Configuration")
    table_theme = st.sidebar.selectbox(
        "Theme",
        options=["alpine", "balham", "material"],
        index=0
    )
    
    table_height = st.sidebar.slider(
        "Table Height",
        min_value=300,
        max_value=800,
        value=400,
        step=50
    )
    
    enable_grouping = st.sidebar.checkbox("Enable Row Grouping", value=False)
    enable_selection = st.sidebar.checkbox("Enable Row Selection", value=True)
    show_aggregations = st.sidebar.checkbox("Show Aggregations", value=True)
    
    # Demo mode selection
    st.sidebar.subheader("Demo Mode")
    demo_mode = st.sidebar.radio(
        "Choose Demo",
        options=[
            "📊 Basic Table",
            "🔢 Aggregations",
            "📈 Pivot Table",
            "🎯 Advanced Features"
        ]
    )
    
    # Generate data
    with st.spinner("Loading data..."):
        if data_size <= 500:
            df = get_aggregation_demo_data()[:data_size]
        else:
            df = generate_sample_data(data_size)
    
    # Display summary metrics
    st.markdown('<h2 class="section-header">📋 Data Overview</h2>', 
               unsafe_allow_html=True)
    
    create_summary_cards(df)
    
    # Show data info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"**Records:** {len(df):,}")
    with col2:
        st.info(f"**Columns:** {len(df.columns)}")
    with col3:
        st.info(f"**Date Range:** {df['Date'].min()} to {df['Date'].max()}")
    
    # Demo sections based on selection
    if demo_mode == "📊 Basic Table":
        show_basic_table_demo(df, table_theme, table_height, enable_selection)
    
    elif demo_mode == "🔢 Aggregations":
        show_aggregations_demo(df, table_theme, table_height)
    
    elif demo_mode == "📈 Pivot Table":
        show_pivot_table_demo(df)
    
    elif demo_mode == "🎯 Advanced Features":
        show_advanced_features_demo(df, table_theme, table_height)
    
    # Show data visualizations
    show_data_visualizations(df)

def show_basic_table_demo(df, theme, height, enable_selection):
    """Display basic table functionality"""
    
    st.markdown('<h2 class="section-header">📊 Basic Interactive Table</h2>', 
               unsafe_allow_html=True)
    
    st.markdown("""
    **Features demonstrated:**
    - ✅ Column sorting (click headers)
    - ✅ Column filtering (use floating filters at top)
    - ✅ Row selection with checkboxes
    - ✅ Responsive column resizing
    - ✅ Column selector in sidebar
    - ✅ Data export capabilities
    """)
    
    # Additional controls
    col1, col2, col3 = st.columns(3)
    with col1:
        enable_column_filter = st.checkbox("Enable Column Filters", value=True)
    with col2:
        enable_sidebar = st.checkbox("Show Column Selector", value=True)
    with col3:
        fit_columns = st.checkbox("Auto-fit Columns", value=False)
    
    # Create the enhanced table
    response = create_aggrid_table(
        df,
        enable_selection=enable_selection,
        theme=theme,
        height=height,
        show_aggregations=False,
        enable_sidebar=enable_sidebar,
        enable_column_filter=enable_column_filter
    )
    
    # Show selected data
    if enable_selection and len(response["selected_rows"]) > 0:
        st.subheader("Selected Rows")
        selected_df = pd.DataFrame(response["selected_rows"])
        st.dataframe(selected_df, use_container_width=True)
        
        # Download button for selected data
        csv = selected_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Selected Data as CSV",
            data=csv,
            file_name="selected_data.csv",
            mime="text/csv"
        )

def show_aggregations_demo(df, theme, height):
    """Display aggregation functionality"""
    
    st.markdown('<h2 class="section-header">🔢 Aggregations & Grouping</h2>', 
               unsafe_allow_html=True)
    
    st.markdown("""
    **Features demonstrated:**
    - ✅ Automatic aggregations (sum, average, count)
    - ✅ Row grouping by categories
    - ✅ Expandable/collapsible groups
    - ✅ Group-level aggregations
    - ✅ Column selector sidebar
    - ✅ Floating filter headers
    """)
    
    # Grouping options
    col1, col2, col3 = st.columns(3)
    with col1:
        group_by = st.multiselect(
            "Group by columns:",
            options=["Category", "Region", "Sales Rep"],
            default=["Category"],
            help="Select columns to group the data by"
        )
    
    with col2:
        show_totals = st.checkbox("Show Group Totals", value=True)
        enable_filters = st.checkbox("Enable Column Filters", value=True)
    
    with col3:
        enable_sidebar = st.checkbox("Show Column Tools", value=True)
    
    # Create grouped table
    response = create_aggrid_table(
        df,
        enable_grouping=True,
        groupable_columns=group_by,
        theme=theme,
        height=height,
        show_aggregations=show_totals,
        enable_sidebar=enable_sidebar,
        enable_column_filter=enable_filters
    )
    
    # Show aggregation summary
    if len(df) > 0:
        st.subheader("📊 Summary Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if group_by:
                for group_col in group_by:
                    unique_count = df[group_col].nunique()
                    st.metric(f"Unique {group_col}s", unique_count)
        
        with col2:
            total_quantity = df['Quantity'].sum()
            avg_quantity = df['Quantity'].mean()
            st.metric("Total Quantity", f"{total_quantity:,}")
            st.metric("Average Quantity", f"{avg_quantity:.1f}")
        
        with col3:
            total_revenue = df['Total Amount'].sum()
            avg_profit = df['Profit Margin'].mean()
            st.metric("Total Revenue", f"${total_revenue:,.2f}")
            st.metric("Average Profit Margin", f"{avg_profit:.1f}%")

def show_pivot_table_demo(df):
    """Display pivot table functionality"""
    
    st.markdown('<h2 class="section-header">📈 Pivot Table Analysis</h2>', 
               unsafe_allow_html=True)
    
    st.markdown("""
    **Features demonstrated:**
    - ✅ Dynamic pivot table creation
    - ✅ Drag-and-drop column organization in sidebar
    - ✅ Multiple aggregation functions
    - ✅ Cross-tabulation analysis
    - ✅ Interactive column selector
    - ✅ Real-time pivot updates
    """)
    
    st.info("💡 **Tip**: Use the Column Tool Panel on the right to drag columns into Row Groups, Pivot, and Values sections!")
    
    # Enhanced pivot configuration
    st.subheader("🎯 Pivot Configuration")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        pivot_rows = st.multiselect(
            "📊 Row Groups:",
            options=["Category", "Region", "Sales Rep", "Product"],
            default=["Category"],
            help="Columns to group rows by"
        )
    
    with col2:
        pivot_cols = st.multiselect(
            "🔄 Pivot Columns:",
            options=["Region", "Category", "Sales Rep", "Product"],
            default=["Region"],
            help="Columns to pivot (create columns from values)"
        )
    
    with col3:
        pivot_values = st.multiselect(
            "📈 Value Columns:",
            options=["Total Amount", "Quantity", "Unit Price", "Profit Margin"],
            default=["Total Amount"],
            help="Columns to aggregate"
        )
    
    with col4:
        agg_function = st.selectbox(
            "🔢 Aggregation:",
            options=["sum", "avg", "count", "min", "max"],
            index=0,
            help="How to aggregate the values"
        )
    
    # Additional options
    col1, col2, col3 = st.columns(3)
    with col1:
        show_pandas_comparison = st.checkbox("Show Pandas Pivot Comparison", value=False)
    with col2:
        auto_size_columns = st.checkbox("Auto-size Columns", value=True)
    with col3:
        show_totals = st.checkbox("Show Row Totals", value=True)
    
    # Instructions for drag-and-drop
    with st.expander("📚 How to use the Pivot Table", expanded=False):
        st.markdown("""
        **Method 1: Use the controls above** 
        - Select Row Groups, Pivot Columns, and Values using the dropdowns above
        - Click the refresh button to update the table
        
        **Method 2: Use drag-and-drop (Advanced)**
        1. Open the **Column Tool Panel** on the right side of the table
        2. Drag columns into the appropriate sections:
           - **Row Groups**: Groups data by these columns
           - **Pivot**: Creates columns from unique values
           - **Values**: The data to aggregate
        3. The table updates automatically as you drag columns
        
        **Tips:**
        - You can have multiple row groups and pivot columns
        - Right-click on column headers for more options
        - Use the filters to focus on specific data
        """)
    
    # Create the pivot table
    st.subheader("📊 Interactive Pivot Table")
    
    if pivot_rows or pivot_cols or pivot_values:
        # Create pivot table
        try:
            response = create_pivot_table(
                df,
                rows=pivot_rows,
                cols=pivot_cols,
                values=pivot_values,
                aggfunc=agg_function
            )
            
            # Show pivot stats
            if pivot_values:
                st.subheader("📈 Pivot Statistics")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if pivot_rows:
                        total_row_groups = len(df.groupby(pivot_rows[0])) if len(pivot_rows) > 0 else 0
                        st.metric("Row Groups", total_row_groups)
                
                with col2:
                    if pivot_cols:
                        total_pivot_cols = len(df[pivot_cols[0]].unique()) if len(pivot_cols) > 0 else 0
                        st.metric("Pivot Columns", total_pivot_cols)
                
                with col3:
                    total_cells = len(df)
                    st.metric("Total Data Points", total_cells)
                    
        except Exception as e:
            st.error(f"Error creating pivot table: {str(e)}")
            st.warning("Please check your column selections and try again.")
    else:
        st.warning("Please select at least one Row Group, Pivot Column, or Value to create a pivot table.")
        # Show a basic table as fallback
        create_aggrid_table(df, height=300, enable_sidebar=True, enable_column_filter=True)
    
    # Show traditional pandas pivot for comparison
    if show_pandas_comparison and pivot_rows and pivot_values:
        st.subheader("📊 Pandas Pivot Comparison")
        try:
            pandas_pivot = df.pivot_table(
                index=pivot_rows,
                columns=pivot_cols[0] if pivot_cols else None,
                values=pivot_values[0],
                aggfunc=agg_function,
                fill_value=0,
                margins=show_totals
            )
            st.dataframe(pandas_pivot, use_container_width=True)
            
            # Download button for pandas pivot
            csv = pandas_pivot.to_csv()
            st.download_button(
                label="📥 Download Pandas Pivot as CSV",
                data=csv,
                file_name="pandas_pivot_table.csv",
                mime="text/csv"
            )
            
        except Exception as e:
            st.error(f"Error creating pandas pivot: {str(e)}")

def show_advanced_features_demo(df, theme, height):
    """Display advanced features"""
    
    st.markdown('<h2 class="section-header">🎯 Advanced Features</h2>', 
               unsafe_allow_html=True)
    
    st.markdown("""
    **Features demonstrated:**
    - ✅ Advanced filtering with floating filters
    - ✅ Column selector and management tools
    - ✅ Export functionality
    - ✅ Real-time data updates
    - ✅ Responsive column sizing
    - ✅ Enhanced user interface
    """)
    
    # Advanced options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_category = st.selectbox(
            "Filter by Category:",
            options=["All"] + list(df['Category'].unique()),
            index=0
        )
        
        min_amount = st.number_input(
            "Minimum Total Amount:",
            min_value=0.0,
            max_value=float(df['Total Amount'].max()),
            value=0.0,
            step=100.0
        )
    
    with col2:
        enable_floating_filters = st.checkbox("Enable Floating Filters", value=True)
        enable_sidebar = st.checkbox("Show Column Tools", value=True)
        auto_size_columns = st.checkbox("Auto-size Columns", value=False)
    
    with col3:
        enable_selection = st.checkbox("Enable Row Selection", value=True)
        show_aggregations = st.checkbox("Show Aggregations", value=True)
        fit_columns = st.checkbox("Fit Columns to Screen", value=False)
    
    # Apply filters
    filtered_df = df.copy()
    if filter_category != "All":
        filtered_df = filtered_df[filtered_df['Category'] == filter_category]
    if min_amount > 0:
        filtered_df = filtered_df[filtered_df['Total Amount'] >= min_amount]
    
    st.info(f"📊 Showing {len(filtered_df):,} records (filtered from {len(df):,})")
    
    # Create advanced table
    response = create_aggrid_table(
        filtered_df,
        theme=theme,
        height=height,
        show_aggregations=show_aggregations,
        enable_selection=enable_selection,
        enable_sidebar=enable_sidebar,
        enable_column_filter=enable_floating_filters
    )
    
    # Advanced features demo
    if len(filtered_df) > 0:
        st.subheader("� Advanced Controls")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📊 Export Current View"):
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Current View",
                    data=csv,
                    file_name="advanced_view_export.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("📋 Export Selected"):
                if enable_selection and len(response["selected_rows"]) > 0:
                    selected_csv = pd.DataFrame(response["selected_rows"]).to_csv(index=False)
                    st.download_button(
                        label="📥 Download Selected",
                        data=selected_csv,
                        file_name="selected_rows.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("No rows selected or selection is disabled")
        
        with col3:
            if st.button("📈 Generate Report"):
                st.info("Report generation feature - would create detailed analytics report")
        
        with col4:
            if st.button("🔄 Reset Filters"):
                st.experimental_rerun()
        
        # Show selection details
        if enable_selection and len(response["selected_rows"]) > 0:
            st.subheader("📋 Selected Data Details")
            selected_df = pd.DataFrame(response["selected_rows"])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Selected Rows", len(selected_df))
            with col2:
                if 'Total Amount' in selected_df.columns:
                    total_selected = selected_df['Total Amount'].sum()
                    st.metric("Total Selected Amount", f"${total_selected:,.2f}")
            with col3:
                if 'Profit Margin' in selected_df.columns:
                    avg_margin = selected_df['Profit Margin'].mean()
                    st.metric("Avg Profit Margin", f"{avg_margin:.1f}%")
            
            # Show selected data
            st.dataframe(selected_df, use_container_width=True, height=200)

def show_data_visualizations(df):
    """Display data visualizations"""
    
    st.markdown('<h2 class="section-header">📈 Data Visualizations</h2>', 
               unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Sales by category
        fig1 = px.bar(
            df.groupby('Category')['Total Amount'].sum().reset_index(),
            x='Category',
            y='Total Amount',
            title='Sales by Category',
            color='Total Amount',
            color_continuous_scale='Blues'
        )
        fig1.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Profit margin distribution
        fig2 = px.histogram(
            df,
            x='Profit Margin',
            title='Profit Margin Distribution',
            nbins=20,
            color_discrete_sequence=['#1f77b4']
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Sales trend over time
    df['Date'] = pd.to_datetime(df['Date'])
    daily_sales = df.groupby('Date')['Total Amount'].sum().reset_index()
    
    fig3 = px.line(
        daily_sales,
        x='Date',
        y='Total Amount',
        title='Sales Trend Over Time',
        color_discrete_sequence=['#1f77b4']
    )
    st.plotly_chart(fig3, use_container_width=True)

if __name__ == "__main__":
    main()
