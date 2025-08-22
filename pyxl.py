import streamlit as st
import pandas as pd
st.title(":red[PYXL - Excel File Processing📁 and Visualization📊] ")
st.set_page_config(
    page_title="PYXL App",
    layout="wide",   # "centered" (default) or "wide"
    initial_sidebar_state="expanded"  # optional
)
st.markdown(
    """
    <style>
    .stApp, .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp span, .stApp label {
        color: white !important;  
    }
    <hr style="border:2px solid #000000; border-radius: 5px;">
    </style>
    """,
    unsafe_allow_html=True
)
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    selected_columns = st.multiselect(
        'Select columns to display:',
        df.columns.tolist(),
        default=df.columns.tolist(),
        key="column_selector"
    )

    if selected_columns:
        option = st.selectbox(
            "Choose an action",
            ["Sort", "Filter"],
            key="action_selector"
        )

        result_df = df[selected_columns]  # Default to selected columns

        if option == "Sort":
            sort_column = st.selectbox(
                "Select column to sort by",
                selected_columns,
                key="sort_column_selector"
            )
            ascending = st.checkbox("Sort ascending", value=True, key="sort_ascending_checkbox")
            result_df = result_df.sort_values(by=sort_column, ascending=ascending)
            st.dataframe(result_df, use_container_width=True)
        elif option == "Filter":
            filter_column = st.selectbox(
                "Select column to filter by",
                selected_columns,
                key="filter_column_selector"
            )
            filter_value = st.text_input("Enter value to filter", key="filter_value_input")
            if filter_value:
                result_df = result_df[result_df[filter_column].astype(str).str.contains(filter_value)]
            st.dataframe(result_df, use_container_width=True)

        # Download button for the current result_df
        csv = convert_df(result_df)
        st.download_button(
            label="Download filtered data as CSV",
            data=csv,
            file_name="filtered_data.csv",
            mime="text/csv",
            key="download-csv"
        )

        # Visualization section
        if st.checkbox("Do you want to create a visualization?"):
            chart_type = st.selectbox("Select chart type", ["Bar Chart", "Line Chart"], key="chart_type_selector")
            x_col = st.selectbox("Select X-axis column", result_df.columns, key="x_axis_selector")
            y_col = st.selectbox("Select Y-axis column", result_df.columns, key="y_axis_selector")

            if chart_type == "Bar Chart":
                st.bar_chart(result_df[[x_col, y_col]].set_index(x_col))
            elif chart_type == "Line Chart":
                st.line_chart(result_df[[x_col, y_col]].set_index(x_col))
    else:
        st.warning("Please select at least one column to display.")
else:
    st.info("Please upload an Excel file to get started.")

st.info("Please use the X mark in file uploader to clear the uploaded file and start over.")