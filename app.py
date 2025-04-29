import streamlit as st
import pandas as pd
import json

# --- Set page settings ---
st.set_page_config(page_title="Strategy Rule Matcher", page_icon="🎯")

st.title("🎯 Strategy Rule Matcher")
st.markdown("Match your query context against rules, with dropdown and slider-based inputs.")

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

# --- Dropdowns for each entity ---
query_context = {}
for entity, options in entity_options.items():
    selection = st.selectbox(f"{entity}:", options, index=0)
    query_context[entity] = selection

# --- Entity Weightings with Sliders ---
st.header("⚖️ Entity Weightings")

st.markdown("Adjust the importance (weight) for each entity. Higher numbers mean more influence.")

entity_weights = {}
for entity in entity_options.keys():
    default_weight = {
        "Brand": 1,
        "Sport": 1,
        "Competition": 1,
        "Grade": 3,
        "Market": 4,
        "TimeBased": 5,
        "Cohort": 6
    }.get(entity, 1)

    weight = st.slider(
        f"Weight for {entity}",
        min_value=0,
        max_value=10,
        value=default_weight
    )
    entity_weights[entity] = weight

# --- Rules Input using st.data_editor ---
st.subheader("📋 Define Your Rules")
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

rules_data = st.data_editor(
    default_rules,
    use_container_width=True,
    num_rows="dynamic",
    height=400
)

# --- Run Button ---
if st.button("▶️ Run Matching"):
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
