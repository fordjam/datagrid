"""
Reusable AG Grid components for Streamlit
"""
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode
import streamlit as st
import pandas as pd

def create_aggrid_table(
    df, 
    enable_selection=True,
    selection_mode="multiple",
    enable_sorting=True,
    enable_filtering=True,
    enable_grouping=False,
    groupable_columns=None,
    height=400,
    theme="alpine",
    show_aggregations=True,
    custom_css=None
):
    """
    Create a customizable AG Grid table
    
    Args:
        df: pandas DataFrame
        enable_selection: Enable row selection
        selection_mode: 'single' or 'multiple'
        enable_sorting: Enable column sorting
        enable_filtering: Enable column filtering
        enable_grouping: Enable row grouping
        groupable_columns: List of columns that can be grouped
        height: Table height in pixels
        theme: AG Grid theme ('alpine', 'balham', 'material')
        show_aggregations: Show aggregation row
        custom_css: Custom CSS styling
    
    Returns:
        AgGrid response object
    """
    
    # Build grid options
    gb = GridOptionsBuilder.from_dataframe(df)
    
    # Configure selection
    if enable_selection:
        gb.configure_selection(
            selection_mode, 
            use_checkbox=True,
            groupSelectsChildren=True,
            groupSelectsFiltered=True
        )
    
    # Configure default columns
    gb.configure_default_column(
        groupable=enable_grouping,
        value=True,
        enableRowGroup=enable_grouping,
        aggFunc="sum",
        editable=False,
        sortable=enable_sorting,
        filter=enable_filtering,
        resizable=True
    )
    
    # Configure specific columns
    if 'Date' in df.columns:
        gb.configure_column('Date', type=["dateColumnFilter", "customDateTimeFormat"], 
                          custom_format_string='yyyy-MM-dd', pivot=True)
    
    if 'Total Amount' in df.columns:
        gb.configure_column('Total Amount', type=["numericColumn", "numberColumnFilter", "customNumericFormat"], 
                          precision=2, aggFunc="sum")
    
    if 'Unit Price' in df.columns:
        gb.configure_column('Unit Price', type=["numericColumn", "numberColumnFilter", "customNumericFormat"], 
                          precision=2, aggFunc="avg")
    
    if 'Quantity' in df.columns:
        gb.configure_column('Quantity', type=["numericColumn", "numberColumnFilter"], 
                          aggFunc="sum")
    
    if 'Profit Margin' in df.columns:
        gb.configure_column('Profit Margin', type=["numericColumn", "numberColumnFilter"], 
                          precision=1, aggFunc="avg")
    
    # Configure grouping
    if enable_grouping and groupable_columns:
        for col in groupable_columns:
            if col in df.columns:
                gb.configure_column(col, rowGroup=True, hide=True)
    
    # Configure sidebar
    gb.configure_side_bar()
    
    # Configure grid options
    gridOptions = gb.build()
    
    # Add aggregation row
    if show_aggregations:
        gridOptions["groupIncludeFooter"] = True
        gridOptions["groupIncludeTotalFooter"] = True
        
    # Custom JS for cell styling
    cell_style_jscode = JsCode("""
    function(params) {
        if (params.column.colId === 'Profit Margin') {
            if (params.value > 40) {
                return {'background-color': '#d4edda', 'color': '#155724'};
            } else if (params.value < 20) {
                return {'background-color': '#f8d7da', 'color': '#721c24'};
            }
        }
        if (params.column.colId === 'Total Amount') {
            if (params.value > 1000) {
                return {'font-weight': 'bold', 'color': '#007bff'};
            }
        }
        return {};
    }
    """)
    
    # Apply cell styling to relevant columns
    if 'Profit Margin' in df.columns or 'Total Amount' in df.columns:
        for col in df.columns:
            if col in ['Profit Margin', 'Total Amount']:
                gb.configure_column(col, cellStyle=cell_style_jscode)
    
    gridOptions = gb.build()
    
    # Create and return the AgGrid
    response = AgGrid(
        df,
        gridOptions=gridOptions,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        fit_columns_on_grid_load=False,
        theme=theme,
        enable_enterprise_modules=True,
        height=height,
        width='100%',
        reload_data=False,
        custom_css=custom_css
    )
    
    return response

def create_pivot_table(df, rows=None, cols=None, values=None, aggfunc='sum'):
    """
    Create a pivot table using AG Grid
    
    Args:
        df: pandas DataFrame
        rows: List of columns to use as row groups
        cols: List of columns to use as column groups
        values: List of columns to aggregate
        aggfunc: Aggregation function
    
    Returns:
        AgGrid response object
    """
    
    gb = GridOptionsBuilder.from_dataframe(df)
    
    # Configure pivot mode
    gb.configure_grid_options(pivotMode=True)
    
    # Configure row groups
    if rows:
        for row in rows:
            gb.configure_column(row, rowGroup=True, hide=True)
    
    # Configure column groups (pivot columns)
    if cols:
        for col in cols:
            gb.configure_column(col, pivot=True, hide=True)
    
    # Configure value columns
    if values:
        for value in values:
            if aggfunc == 'sum':
                gb.configure_column(value, aggFunc='sum')
            elif aggfunc == 'avg':
                gb.configure_column(value, aggFunc='avg')
            elif aggfunc == 'count':
                gb.configure_column(value, aggFunc='count')
            elif aggfunc == 'min':
                gb.configure_column(value, aggFunc='min')
            elif aggfunc == 'max':
                gb.configure_column(value, aggFunc='max')
    
    # Configure sidebar for easier column management
    gb.configure_side_bar()
    
    gridOptions = gb.build()
    
    response = AgGrid(
        df,
        gridOptions=gridOptions,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        fit_columns_on_grid_load=True,
        theme="alpine",
        enable_enterprise_modules=True,
        height=400,
        width='100%'
    )
    
    return response

def create_summary_cards(df):
    """Create summary cards for key metrics"""
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_sales = df['Total Amount'].sum()
        st.metric(
            label="Total Sales",
            value=f"${total_sales:,.2f}",
            delta=None
        )
    
    with col2:
        avg_order = df['Total Amount'].mean()
        st.metric(
            label="Average Order",
            value=f"${avg_order:,.2f}",
            delta=None
        )
    
    with col3:
        total_orders = len(df)
        st.metric(
            label="Total Orders",
            value=f"{total_orders:,}",
            delta=None
        )
    
    with col4:
        avg_profit = df['Profit Margin'].mean()
        st.metric(
            label="Avg Profit Margin",
            value=f"{avg_profit:.1f}%",
            delta=None
        )
