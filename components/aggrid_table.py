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
    custom_css=None,
    enable_sidebar=True,
    enable_column_filter=True
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
        enable_sidebar: Show sidebar with column tools
        enable_column_filter: Enable column filter panel
    
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
        resizable=True,
        floatingFilter=enable_column_filter  # Add floating filters
    )
    
    # Configure specific columns with error handling
    try:
        if 'Date' in df.columns:
            gb.configure_column('Date', type=["dateColumnFilter", "customDateTimeFormat"], 
                              custom_format_string='yyyy-MM-dd', pivot=True, 
                              floatingFilter=enable_column_filter)
        
        if 'Total Amount' in df.columns:
            gb.configure_column('Total Amount', type=["numericColumn", "numberColumnFilter", "customNumericFormat"], 
                              precision=2, aggFunc="sum", floatingFilter=enable_column_filter)
        
        if 'Unit Price' in df.columns:
            gb.configure_column('Unit Price', type=["numericColumn", "numberColumnFilter", "customNumericFormat"], 
                              precision=2, aggFunc="avg", floatingFilter=enable_column_filter)
        
        if 'Quantity' in df.columns:
            gb.configure_column('Quantity', type=["numericColumn", "numberColumnFilter"], 
                              aggFunc="sum", floatingFilter=enable_column_filter)
        
        if 'Profit Margin' in df.columns:
            gb.configure_column('Profit Margin', type=["numericColumn", "numberColumnFilter"], 
                              precision=1, aggFunc="avg", floatingFilter=enable_column_filter)
                              
        # Configure text columns for better filtering
        for col in df.columns:
            if df[col].dtype == 'object' and col not in ['Date']:
                gb.configure_column(col, filter="agTextColumnFilter", 
                                  floatingFilter=enable_column_filter)
                                  
    except Exception as e:
        st.warning(f"Column configuration warning: {str(e)}")
    
    # Configure grouping
    if enable_grouping and groupable_columns:
        for col in groupable_columns:
            if col in df.columns:
                gb.configure_column(col, rowGroup=True, hide=True)
    
    # Configure sidebar with column tools
    if enable_sidebar:
        gb.configure_side_bar(
            filters_panel=True,
            columns_panel=True,
            defaultToolPanel="columns"
        )
    
    # Build grid options
    gridOptions = gb.build()
    
    # Add aggregation row
    if show_aggregations:
        gridOptions["groupIncludeFooter"] = True
        gridOptions["groupIncludeTotalFooter"] = True
        
    # Enable column filter panel at top
    if enable_column_filter:
        gridOptions["floatingFilter"] = True
    
    # Create and return the AgGrid
    try:
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
    
    except Exception as e:
        st.error(f"Error creating AG Grid table: {str(e)}")
        st.warning("Falling back to standard Streamlit dataframe...")
        st.dataframe(df, use_container_width=True, height=height)
        
        # Return a mock response object for compatibility
        class MockResponse:
            def __init__(self, df):
                self.selected_rows = []
                self.data = df
            
            def __getitem__(self, key):
                if key == "selected_rows":
                    return []
                elif key == "data":
                    return self.data
                else:
                    return []
        
        return MockResponse(df)

def create_pivot_table(df, rows=None, cols=None, values=None, aggfunc='sum'):
    """
    Create a working pivot table using AG Grid
    
    Args:
        df: pandas DataFrame
        rows: List of columns to use as row groups
        cols: List of columns to use as column groups
        values: List of columns to aggregate
        aggfunc: Aggregation function
    
    Returns:
        AgGrid response object
    """
    
    if not rows and not cols and not values:
        st.warning("Please select at least one row, column, or value for the pivot table.")
        return create_aggrid_table(df, height=300)
    
    try:
        # Build grid options from dataframe
        gb = GridOptionsBuilder.from_dataframe(df)
        
        # Enable pivot mode
        gb.configure_grid_options(
            pivotMode=True,
            suppressAggFuncInHeader=False,
            suppressColumnVirtualisation=False
        )
        
        # Configure all columns as groupable and pivotable by default
        gb.configure_default_column(
            enableRowGroup=True,
            enablePivot=True,
            enableValue=True,
            sortable=True,
            resizable=True,
            filter=True,
            floatingFilter=True
        )
        
        # Configure row groups
        if rows:
            for row_col in rows:
                if row_col in df.columns:
                    gb.configure_column(
                        row_col, 
                        rowGroup=True, 
                        hide=False,  # Don't hide so users can see the grouping
                        enableRowGroup=True
                    )
        
        # Configure pivot columns
        if cols:
            for col_col in cols:
                if col_col in df.columns:
                    gb.configure_column(
                        col_col, 
                        pivot=True, 
                        enablePivot=True
                    )
        
        # Configure value columns with appropriate aggregation
        if values:
            for value_col in values:
                if value_col in df.columns:
                    # Set the aggregation function based on data type and user selection
                    if aggfunc == 'sum':
                        agg_func = 'sum'
                    elif aggfunc == 'avg':
                        agg_func = 'avg'
                    elif aggfunc == 'count':
                        agg_func = 'count'
                    elif aggfunc == 'min':
                        agg_func = 'min'
                    elif aggfunc == 'max':
                        agg_func = 'max'
                    else:
                        agg_func = 'sum'
                    
                    gb.configure_column(
                        value_col, 
                        aggFunc=agg_func,
                        enableValue=True,
                        valueFormatter="value = Math.round(value * 100) / 100" if value_col in ['Unit Price', 'Total Amount', 'Profit Margin'] else None
                    )
        
        # Configure sidebar for drag and drop functionality
        gb.configure_side_bar(
            filters_panel=True,
            columns_panel=True,
            defaultToolPanel="columns"
        )
        
        # Build the grid options
        gridOptions = gb.build()
        
        # Enable additional pivot features
        gridOptions.update({
            "pivotMode": True,
            "rowGroupPanelShow": "always",
            "pivotPanelShow": "always",
            "valuePanelShow": "always",
            "sideBar": {
                "toolPanels": [
                    {
                        "id": "columns",
                        "labelDefault": "Columns",
                        "labelKey": "columns",
                        "iconKey": "columns",
                        "toolPanel": "agColumnsToolPanel",
                        "toolPanelParams": {
                            "suppressRowGroups": False,
                            "suppressValues": False,
                            "suppressPivots": False,
                            "suppressPivotMode": False,
                            "suppressColumnFilter": False,
                            "suppressColumnSelectAll": False,
                            "suppressColumnExpandAll": False
                        }
                    },
                    {
                        "id": "filters",
                        "labelDefault": "Filters",
                        "labelKey": "filters",
                        "iconKey": "filter",
                        "toolPanel": "agFiltersToolPanel"
                    }
                ],
                "defaultToolPanel": "columns"
            }
        })
        
        # Create the AG Grid
        response = AgGrid(
            df,
            gridOptions=gridOptions,
            data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
            update_mode=GridUpdateMode.MODEL_CHANGED,
            fit_columns_on_grid_load=True,
            theme="alpine",
            enable_enterprise_modules=True,
            height=500,
            width='100%',
            allow_unsafe_jscode=True
        )
        
        return response
        
    except Exception as e:
        st.error(f"Error creating pivot table: {str(e)}")
        st.warning("Falling back to pandas pivot table...")
        
        # Fallback to pandas pivot
        try:
            if rows and values:
                pivot_df = df.pivot_table(
                    index=rows,
                    columns=cols[0] if cols else None,
                    values=values[0] if values else df.select_dtypes(include=[float, int]).columns[0],
                    aggfunc=aggfunc,
                    fill_value=0
                )
                st.dataframe(pivot_df, use_container_width=True)
        except Exception as e2:
            st.error(f"Pandas pivot also failed: {str(e2)}")
            return create_aggrid_table(df, height=400)

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
