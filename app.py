import streamlit as st
import pandas as pd
import json

# --- Set page settings ---
st.set_page_config(page_title="Strategy Rule Matcher", page_icon="🎯")

st.title("🎯 Strategy Rule Matcher")
st.markdown("Match your query context against rules, with dropdown and slider-based inputs.")

# --- Session state setup (important for Reset functionality) ---
if "reset" not in st.session_state:
    st.session_state.reset = False

st.header("🔧 Query Context")

# --- Predefined options for each entity ---
entity_options = {
    "Brand": ["Brand 1", "Brand 2"],
    "Sport": ["Basketball", "Football", "American Football"],
    "Competition": ["NBA", "NFL", "La Liga", "EPL"],
    "Grade": ["A", "C", "AA"],
    "Market": ["Market 3", "First GS", "WDW"],
    "TimeBased": ["30", "120", "360", "1440", "Live"],
    "Cohort": ["Cohort A", "Cohort B"]
}

# --- Default selections ---
default_query_context = {
    "Brand": "Brand 1",
    "Sport": "Basketball",
    "Competition": "NBA",
    "Grade": "A",
    "Market": "Market 3",
    "TimeBased": "30",
    "Cohort": "Cohort A"
}

# --- Query Context Dropdowns ---
query_context = {}
for entity, options in entity_options.items():
    if st.session_state.reset:
        selection = options[0]
    else:
        selection = st.selectbox(
            f"{entity}:",
            options,
            index=options.index(default_query_context.get(entity, options[0]))
        )
    query_context[entity] = selection

# --- Entity Weightings with Sliders ---
st.header("⚖️ Entity Weightings")

default_weights = {
    "Brand": 1,
    "Sport": 1,
    "Competition": 1,
    "Grade": 3,
    "Market": 4,
    "TimeBased": 5,
    "Cohort": 6
}

entity_weights = {}
for entity in entity_options.keys():
    if st.session_state.reset:
        weight = default_weights.get(entity, 1)
    else:
        weight = st.slider(
            f"Weight for {entity}",
            min_value=0,
            max_value=10,
            value=default_weights.get(entity, 1)
        )
    entity_weights[entity] = weight

# --- Default Rules ---
default_rules = pd.DataFrame({
    "Permutation": [
        "Brand:Brand 1, Sport:Basketball",
        "Grade:AA, Market:First GS",
        "TimeBased:360, Sport:American Football, Competition:NFL",
        "Brand:Brand 2, Grade:C, Cohort:Cohort A",
        "Brand:Brand 1, Sport:Basketball, Competition:La Liga",
        "Brand:Brand 1, Competition:EPL, Market:WDW"
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

st.subheader("📋 Define Your Rules")
if st.session_state.reset:
    rules_data = default_rules.copy()
else:
    rules_data = st.data_editor(
        default_rules,
        use_container_width=True,
        num_rows="dynamic",
        height=400
    )

# --- Buttons Section ---
col1, col2 = st.columns(2)

with col1:
    run_matching = st.button("▶️ Run Matching")

with col2:
    reset_inputs = st.button("🔄 Reset Inputs")

# --- Reset Inputs Logic ---
if reset_inputs:
    st.session_state.reset = True
    st.experimental_rerun()

# --- Matching Logic ---
if run_matching:
    try:
        # Flatten query context into a list of just values
        query_values = list(query_context.values())

        # Helper functions
        def extract_entity_value(entry):
            entity, value = entry.split(":", 1)
            return entity.strip(), value.strip()

        def compute_score(permutation):
            return sum(entity_weights.get(entity, 0) for entity, _ in map(extract_entity_value, permutation))

        def matches_query(permutation):
            values = [v for _, v in map(extract_entity_value, permutation)]
            return any(q in values for q in query_values)

        def includes_brand_and_sport(permutation):
            entities = [e for e, _ in map(extract_entity_value, permutation)]
            return "Brand" in entities and "Sport" in entities

        # Format rules from editor
        rules = []
        for _, row in rules_data.iterrows():
            if pd.isna(row["Permutation"]):
                continue
            permutation = [item.strip() for item in row["Permutation"].split(",") if item.strip()]
            strategy = row["Strategy"] if not pd.isna(row["Strategy"]) else None
            rules.append({
                "permutation": permutation,
                "strategy": strategy
            })

        # Apply filtering
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
                "Strategy": strategy,
                "Score": score,
                "Permutation": ", ".join(perm)
            })

        matched_rules = sorted(matched_rules, key=lambda x: x["Score"], reverse=True)

        st.success(f"✅ Found {len(matched_rules)} matching rule(s).")
        st.dataframe(matched_rules, use_container_width=True)

    except Exception as e:
        st.error(f"⚠️ An error occurred: {e}")
