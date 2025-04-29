# Save this file as app.py
# Run it locally: streamlit run app.py

import streamlit as st
import json

st.title("Strategy Rule Matcher")

st.markdown("""
Fill in the fields below and click **Run Matching** to process the rules.
""")

# --- Web Form for Inputs ---

with st.form("strategy_form"):

    query_context_input = st.text_area(
        "Query Context (comma-separated values)",
        value="Brand 1, Basketball, NBA, A, 24 hours, Cohort B"
    )

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

    rules_input = st.text_area(
        "Rules (JSON format)",
        value=json.dumps([
            { "permutation": ["Brand:Brand 1", "Sport:Basketball"], "strategy": "strategy_01" },
            { "permutation": ["Grade:A", "Market:Market 3"], "strategy": "strategy_02" },
            { "permutation": ["TimeBased:24 hours", "Sport:Football", "Competition:NFL"], "strategy": None },
            { "permutation": ["Brand:Brand 2", "Grade:C", "Cohort:Cohort A"], "strategy": "strategy_03" },
            { "permutation": ["Brand:Brand 1", "Sport:Basketball", "Competition:NBA"], "strategy": "strategy_04" },
            { "permutation": ["Brand:Brand 1", "Competition:NBA"], "strategy": "strategy_05" }
        ], indent=2)
    )

    submitted = st.form_submit_button("Run Matching")

# --- Logic to process after submitting the form ---
if submitted:
    try:
        query_context = [s.strip() for s in query_context_input.split(",") if s.strip()]
        weightings = json.loads(weightings_input)
        rules = json.loads(rules_input)

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

        # Apply all the filters
        matched_rules = []
        for rule in rules:
            perm = rule.get("permutation", [])
            strategy = rule.get("strategy")
            if strategy is None:
                continue
            if not matches_query(perm):
                continue
            if not includes_brand_and_sport(perm):
                continue
            score = compute_score(perm)
            matched_rules.append({
                "permutation": perm,
                "strategy": strategy,
                "score": score
            })

        matched_rules.sort(key=lambda x: x["score"], reverse=True)

        st.subheader("Matched & Scored Rules")
        st.json(matched_rules)

    except Exception as e:
        st.error(f"An error occurred: {e}")
