import streamlit as st
import pandas as pd
import json

# Set page configuration
st.set_page_config(page_title="Strategy Rule Matcher", page_icon="🎯")

st.title("🎯 Strategy Rule Matcher")
st.markdown("Match your query context against rules with scoring and filtering.")

# --- Query Context Input ---
st.header("🔧 Settings")
query_context_input = st.text_area(
    "Query Context (comma-separated values)",
    value="Brand 1, Basketball, NBA, A, 24 hours, Cohort B"
)

# --- Weightings Input ---
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

# --- Rules Input as Editable Table ---
st.subheader("📋 Define Your Rules")
rules_df = pd.DataFrame({
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
})

edited_rules = st.data_editor(
    rules_df,
    use_container_width=True,
    num_rows="dynamic",
    hide_index=True
)

# --- Run Matching Button ---
if st.button("▶️ Run Matching"):
    try:
        # Parse Inputs
        query_context = [s.strip() for s in query_context_input.split(",") if s.strip()]
        weightings = json.loads(weightings_input)

        # Helper Functions
        def extract_entity_value(entry):
            entity, value = entry.split(":", 1)
            return entity.strip(), value.strip()

        def compute_score(permutation):
            return sum(weightings.get(entity, 0) for entity, _ in map(extract_entity_value, permutation))

        def matches_query(permutation):
            values = [v for _, v in map(extract_entity_value, permutation)]
            return any(q in values for q in query_context)

        def includes_brand_and_sport(permutation):
            entities = [e for e, _ in map(extract_entity_value, permutation)]
            return "Brand" in entities and "Sport" in entities

        # Process Rules
        matched_rules = []
        for _, row in edited_rules.iterrows():
            permutation = [item.strip() for item in row["Permutation"].split(",") if item.strip()]
            strategy = row["Strategy"]
            if strategy is None:
                continue
            if not matches_query(permutation):
                continue
            if not includes_brand_and_sport(permutation):
                continue
            score = compute_score(permutation)
            matched_rules.append({
                "Strategy": strategy,
                "Score": score,
                "Permutation": ", ".join(permutation)
            })

        # Display Results
        if matched_rules:
            matched_rules_df = pd.DataFrame(matched_rules)
            matched_rules_df = matched_rules_df.sort_values(by="Score", ascending=False)
            st.success(f"Found {len(matched_rules_df)} matching rule(s).")
            st.dataframe(matched_rules_df, use_container_width=True)
        else:
            st.warning("No matching rules found.")

    except Exception as e:
        st.error(f"An error occurred: {e}")
