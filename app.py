import streamlit as st
import json
import pandas as pd

st.set_page_config(page_title="Strategy Rule Matcher", page_icon="🎯")

st.title("🎯 Strategy Rule Matcher")
st.markdown("Match your query context against rules with scoring and filtering.")

st.header("🔧 Settings")

# --- Query Context Input
query_context_input = st.text_area(
    "Query Context (comma-separated values)", 
    value="Brand 1, Basketball, NBA, A, 24 hours, Cohort B"
)

# --- Weightings Input
weightings_input = st.text_area(
    "Entity Weightings (JSON format)", 
    value=json.dumps({
        "Brand": 1,
        "Sport": 1,
        "Competition": 1,
        "Grade": 3,
        "Market": 4,
        "TimeBased": 5,
        "Cohort": 6
    }, indent=2)
)

# --- Rules Input as Editable Table
st.subheader("📋 Define Your Rules")
rules_data = st.experimental_data_editor(
    pd.DataFrame({
        "Permutation": [
            "Brand:Brand 1, Sport:Basketball",
            "Grade:A, Market:Market 3",
            "TimeBased:24 hours, Sport:Football, Competition:NFL",
            "Brand:Brand 2, Grade:C, Cohort:Cohort A",
            "Brand:Brand 1, Sport:Basketball, Competition:NBA",
            "Brand:Brand 1, Competition:NBA"
        ],
        "Strategy": [
            "strategy_01", 
            "strategy_02", 
            None, 
            "strategy_03", 
            "strategy_04", 
            "strategy_05"
        ]
    }),
    use_container_width=True,
    num_rows="dynamic"
