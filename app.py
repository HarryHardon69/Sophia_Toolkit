import streamlit as st
import pandas as pd
from utils.data_loader import load_ethics_db, load_knowledge_graph, load_system_event_log

# Placeholder paths for Sophia_Alpha2 data files
# In a real scenario, these might be configurable or detected.
# For now, adjust these relative paths if your Sophia_Alpha2 data
# is located elsewhere relative to where you run the Sophia_Toolkit.
SOPHIA_ETHICS_DB_PATH = "../Sophia_Alpha2/data/ethics_db.json"
SOPHIA_KG_PATH = "../Sophia_Alpha2/data/knowledge_graph.json"
SOPHIA_SYSTEM_LOG_PATH = "../Sophia_Alpha2/data/logs/system_events.log"

# Number of log entries to display by default
NUM_LOG_ENTRIES_DISPLAY = 20

# --- Page Implementations ---

def ethical_trends_page():
    st.title("Ethical Trends Analysis")

    # Load ethics data
    ethics_data = load_ethics_db(SOPHIA_ETHICS_DB_PATH)

    if not ethics_data or not ethics_data.get("ethical_events"):
        st.warning("No ethical events data loaded or data is empty. Cannot display trends.")
        # Optionally, display the error messages captured by load_ethics_db if they are stored
        # or use a more specific check if load_ethics_db returns more info on error
        return

    # Display trend analysis summary
    trend_summary = ethics_data.get("trend_analysis", {})
    if trend_summary:
        st.subheader("Trend Analysis Summary")
        col1, col2 = st.columns(2)
        col1.metric("Current Trend Direction", trend_summary.get("current_trend_direction", "N/A"))
        col2.metric("Short-term Avg Score (Time-Weighted)",
                    f"{trend_summary.get('short_term_avg_score_t_weighted', 0):.2f}")
        # Add more summary metrics if available and relevant
    else:
        st.info("No trend analysis summary available in the data.")

    # Prepare data for charting
    events = ethics_data["ethical_events"]
    if not events:
        st.info("No ethical events recorded to display.")
        return

    # Convert to DataFrame for easier manipulation and charting
    # Ensure timestamps are converted to datetime objects for proper sorting and charting
    try:
        df_ethics = pd.DataFrame(events)
        if 'timestamp' not in df_ethics.columns:
            st.error("Error: 'timestamp' column missing in ethical events data.")
            return
        if 'final_score' not in df_ethics.columns:
            st.error("Error: 'final_score' column missing in ethical events data.")
            return

        df_ethics['timestamp'] = pd.to_datetime(df_ethics['timestamp'])
        df_ethics = df_ethics.sort_values(by='timestamp') # Sort by time for the line chart

        st.subheader("Ethical Score Over Time")
        # Use st.line_chart, ensuring 'timestamp' is the index or x-axis
        # and 'final_score' is the y-axis.
        # st.line_chart expects the DataFrame index to be the x-axis if only one column is passed for y.
        # Or specify x and y.
        
        # Create a chart with 'timestamp' as x and 'final_score' as y
        # Create a new DataFrame with 'timestamp' as index for st.line_chart
        chart_df = df_ethics.set_index('timestamp')[['final_score']]
        st.line_chart(chart_df)

    except Exception as e:
        st.error(f"An error occurred while preparing data for the chart: {e}")
        # Consider logging the full traceback here for debugging if needed
        # import traceback
        # st.text(traceback.format_exc())

def knowledge_graph_explorer_page():
    st.title("Knowledge Graph Explorer")

    # Load KG data
    kg_data = load_knowledge_graph(SOPHIA_KG_PATH)

    if not kg_data or ("nodes" not in kg_data and "edges" not in kg_data) :
        # load_knowledge_graph returns {"nodes": [], "edges": []} on error,
        # so check if both are potentially empty or if the dict itself is empty.
        st.warning("Knowledge graph data could not be loaded or is empty.")
        return

    num_nodes = len(kg_data.get("nodes", []))
    num_edges = len(kg_data.get("edges", []))

    st.subheader("Graph Overview")
    col1, col2 = st.columns(2)
    col1.metric("Total Nodes", num_nodes)
    col2.metric("Total Edges", num_edges)

    if num_nodes == 0 and num_edges == 0 and not load_knowledge_graph(SOPHIA_KG_PATH): # Check if it was an actual error
        st.info("Consider checking file paths or content if you expected data.")


    st.subheader("Visualization")
    st.text_area("Graph Visualization Placeholder", 
                 "Interactive graph visualization and browsing capabilities will be implemented here in a future update. "
                 "Libraries like Streamlit Agraph, Pyvis, or Plotly could be used.",
                 height=100)
    
    # Optionally, display some raw data if useful (e.g., first few nodes/edges)
    # if st.checkbox("Show raw KG data sample"):
    #     st.write("Sample Nodes:", kg_data.get("nodes", [])[:5])
    #     st.write("Sample Edges:", kg_data.get("edges", [])[:5])

def system_event_log_viewer_page():
    st.title("System Event Log Viewer")

    # Load system event log data
    log_entries = load_system_event_log(SOPHIA_SYSTEM_LOG_PATH)

    if not log_entries:
        st.warning("No system event log data loaded or the log is empty.")
        # Optionally, display messages if load_system_event_log recorded specific file errors
        return

    st.subheader(f"Last {NUM_LOG_ENTRIES_DISPLAY} Log Entries")
    
    # Display the last N entries. Assuming log_entries is a list of dicts.
    # Using a DataFrame for a nice tabular display.
    if isinstance(log_entries, list) and len(log_entries) > 0:
        df_logs = pd.DataFrame(log_entries)
        # Ensure chronological order if timestamps are reliable and consistent
        # For now, just taking the last N as they are loaded (which might be reversed if appended to)
        # If logs are appended, the last N entries in the file are the most recent.
        st.dataframe(df_logs.tail(NUM_LOG_ENTRIES_DISPLAY), height=300) # Use st.dataframe for scrollability
    else:
        st.info("Log data is not in the expected list format or is empty.")

    st.subheader("Future Enhancements")
    st.text_area("Filtering and Searching Placeholder",
                 "Future versions of this tool will include capabilities to filter logs by severity (INFO, WARNING, ERROR), "
                 "search by keywords, and select date ranges.",
                 height=100)

# --- Main Application Setup ---

def main():
    st.set_page_config(page_title="Sophia Toolkit", layout="wide")

    st.sidebar.title("Sophia Toolkit Navigation")
    page_options = {
        "Ethical Trends": ethical_trends_page,
        "Knowledge Graph Explorer": knowledge_graph_explorer_page,
        "System Event Log Viewer": system_event_log_viewer_page,
    }

    selected_page = st.sidebar.radio("Go to", list(page_options.keys()))

    # Display the selected page
    page_options[selected_page]()

if __name__ == "__main__":
    main()
