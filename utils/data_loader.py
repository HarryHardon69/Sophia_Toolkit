import json
import pandas as pd
import streamlit as st # For displaying warnings/errors in the UI

def load_ethics_db(file_path):
    """
    Safely loads and parses the ethics_db.json file.

    Args:
        file_path (str): The path to the ethics_db.json file.

    Returns:
        dict: Parsed JSON data, or an empty dict if loading fails.
              Expected structure: {"ethical_events": [...], "trend_analysis": {...}}
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        if not isinstance(data, dict) or "ethical_events" not in data:
            st.warning(f"Warning: {file_path} does not contain the expected 'ethical_events' key or is not a dictionary.")
            return {"ethical_events": [], "trend_analysis": {}} # Return default structure
        return data
    except FileNotFoundError:
        st.error(f"Error: Ethics DB file not found at {file_path}. Please check the path.")
        return {"ethical_events": [], "trend_analysis": {}}
    except json.JSONDecodeError:
        st.error(f"Error: Could not decode JSON from {file_path}. The file might be corrupted or empty.")
        return {"ethical_events": [], "trend_analysis": {}}
    except Exception as e:
        st.error(f"An unexpected error occurred while loading {file_path}: {e}")
        return {"ethical_events": [], "trend_analysis": {}}

def load_knowledge_graph(file_path):
    """
    Safely loads and parses the knowledge_graph.json file.

    Args:
        file_path (str): The path to the knowledge_graph.json file.

    Returns:
        dict: Parsed JSON data, or an empty dict with 'nodes' and 'edges' keys if loading fails.
              Expected structure: {"nodes": [...], "edges": [...]}
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        if not isinstance(data, dict) or "nodes" not in data or "edges" not in data:
            st.warning(f"Warning: {file_path} does not contain 'nodes' and 'edges' keys or is not a dictionary.")
            return {"nodes": [], "edges": []} # Return default structure
        return data
    except FileNotFoundError:
        st.error(f"Error: Knowledge Graph file not found at {file_path}. Please check the path.")
        return {"nodes": [], "edges": []}
    except json.JSONDecodeError:
        st.error(f"Error: Could not decode JSON from {file_path}. The file might be corrupted or empty.")
        return {"nodes": [], "edges": []}
    except Exception as e:
        st.error(f"An unexpected error occurred while loading {file_path}: {e}")
        return {"nodes": [], "edges": []}

def load_system_event_log(file_path):
    """
    Safely loads and parses a line-delimited JSON system_events.log file.

    Args:
        file_path (str): The path to the system_events.log file.

    Returns:
        list: A list of parsed JSON objects (dicts), or an empty list if loading fails.
    """
    log_entries = []
    try:
        with open(file_path, 'r') as f:
            for line_number, line in enumerate(f, 1):
                try:
                    if line.strip(): # Ensure line is not empty
                        log_entries.append(json.loads(line))
                except json.JSONDecodeError:
                    st.warning(f"Warning: Could not decode JSON from line {line_number} in {file_path}. Skipping line.")
        return log_entries
    except FileNotFoundError:
        st.error(f"Error: System Event Log file not found at {file_path}. Please check the path.")
        return []
    except Exception as e:
        st.error(f"An unexpected error occurred while loading {file_path}: {e}")
        return []

if __name__ == '__main__':
    # Basic test cases (won't run in Streamlit context directly, but good for local testing)
    # Create dummy files for testing
    dummy_ethics_content = {
        "ethical_events": [
            {"timestamp": "2023-01-01T12:00:00Z", "final_score": 0.8, "description": "Event A"},
            {"timestamp": "2023-01-01T12:05:00Z", "final_score": 0.7, "description": "Event B"}
        ],
        "trend_analysis": {"current_trend_direction": "stable", "short_term_avg_score_t_weighted": 0.75}
    }
    with open("dummy_ethics.json", "w") as f:
        json.dump(dummy_ethics_content, f)

    dummy_kg_content = {
        "nodes": [{"id": "node1", "label": "Node 1"}, {"id": "node2", "label": "Node 2"}],
        "edges": [{"source": "node1", "target": "node2", "relation": "connects_to"}]
    }
    with open("dummy_kg.json", "w") as f:
        json.dump(dummy_kg_content, f)

    dummy_log_content = [
        '{"timestamp": "2023-01-01T10:00:00Z", "event_type": "INFO", "message": "System started"}',
        '{"timestamp": "2023-01-01T10:05:00Z", "event_type": "WARNING", "message": "Low disk space"}',
        'This is not a valid JSON line.',
        '{"timestamp": "2023-01-01T10:10:00Z", "event_type": "ERROR", "message": "Critical failure"}'
    ]
    with open("dummy_system_events.log", "w") as f:
        for entry in dummy_log_content:
            f.write(entry + "\n")
    
    print("--- Testing load_ethics_db ---")
    ethics_data = load_ethics_db("dummy_ethics.json")
    print(f"Loaded ethics data: {json.dumps(ethics_data, indent=2)}")
    ethics_data_missing = load_ethics_db("non_existent_ethics.json") # Test missing file
    
    print("\n--- Testing load_knowledge_graph ---")
    kg_data = load_knowledge_graph("dummy_kg.json")
    print(f"Loaded KG data: {json.dumps(kg_data, indent=2)}")
    kg_data_missing = load_knowledge_graph("non_existent_kg.json") # Test missing file

    print("\n--- Testing load_system_event_log ---")
    log_data = load_system_event_log("dummy_system_events.log")
    print(f"Loaded log data: {json.dumps(log_data, indent=2)}")
    log_data_missing = load_system_event_log("non_existent_log.log") # Test missing file

    # Clean up dummy files
    import os
    os.remove("dummy_ethics.json")
    os.remove("dummy_kg.json")
    os.remove("dummy_system_events.log")

    # Test with empty/malformed files (manual creation needed for these tests if desired)
    # with open("empty.json", "w") as f: json.dump({}, f) # or just an empty file
    # ethics_data_empty = load_ethics_db("empty.json")
    # with open("malformed.json", "w") as f: f.write("{'key': 'value'") # malformed
    # ethics_data_malformed = load_ethics_db("malformed.json")
