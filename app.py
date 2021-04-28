import streamlit as st
import pandas as pd
from modules.data_query import DataQuery
from modules.utils import run_concurrent_queries, estimate_gigabytes_scanned
from modules.sql_queries import (
    QUERY_TEMPERATURE,
    NAMES,
    YEARS,
)
from google.cloud import bigquery
from modules.plot import plot_temp
import urllib

# Define BigQuery client
CLIENT = bigquery.Client()


def main():
    # Render the readme as markdown using st.markdown.
    readme_text = st.markdown(get_file_content_as_string("instructions.md"))

    # Add a selector for the app mode on the sidebar.
    st.sidebar.title("Navigation")

    app_mode = st.sidebar.radio(
        "Choose the app mode", ["Show instructions", "Run the app"]
    )

    if app_mode == "Show instructions":
        st.sidebar.success('To continue select "Run the app".')
    elif app_mode == "Run the app":
        readme_text.empty()
        run_the_app()


# This is the main app which appears when the user selects "Run the app".
def run_the_app():
    # In the sidebar, the user select a state and a year and hit run
    n_name, year = frame_selector_ui()

    st.deck_gl_chart(
        viewport={"latitude": 46, "longitude": 2, "zoom": 5, "pitch": 40}
    )

    st.markdown("Made by [Ahmed](https://www.linkedin.com/in/ahmed-ben-debba/)")


@st.cache(allow_output_mutation=True)
def get_data(n_name, year):
    # Define queries
    queries_map = {
        "temperature": [QUERY_TEMPERATURE]

    }

    queries_fetchers = [
        DataQuery(n_name, queries_map["temperature"][0], year)
    ]

    results = run_concurrent_queries(queries_fetchers)

    return results


def compute_size_query(n_name, year):
    queries_map = {
        "temperature": [QUERY_TEMPERATURE]
    }

    queries_fetchers = [
        DataQuery(n_name, queries_map["temperature"][0], year)

    ]

    return sum(estimate_gigabytes_scanned(q.query, CLIENT) for q in queries_fetchers)


# This sidebar UI
def frame_selector_ui():
    st.sidebar.markdown("# Department")

    # The user can pick a state and a year
    n_name = st.sidebar.selectbox("Select a department", NAMES, 4)

    st.sidebar.markdown("# Year")

    year = st.sidebar.selectbox("Select the year of statistics", YEARS, 20)

    # Manul running
    # SQL queries are heavy, we will run only if the user hit Run
    if st.sidebar.button(" Run "):
        # Call function to run the queries and return data
        weights_warning = st.warning("Quering data from Big Query...")
        results = get_data(n_name, year)
        weights_warning.empty()
        # Plot2
        fig = plot_temp(results[n_name])
        st.plotly_chart(fig)



    else:
        # call function to Compute how much data will be processed
        weights_warning = st.warning("Computing query size...")
        size = compute_size_query(n_name, year)
        weights_warning.empty()
        st.success(
            "The query for the selected state and year will process %6.2f GB of data on BigQuery. \t Click run to get the results."
            % size
        )

    return n_name, year


@st.cache(show_spinner=False)
def get_file_content_as_string(path):
    with open(path, "r") as myfile:
        return myfile.read()


if __name__ == "__main__":
    main()
