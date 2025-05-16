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
    "Grade": ["A", "C", "AA", "AMF_NFL"],
    "Market": ["Market 3", "First GS", "WDW", "Win-Draw-Win", "Anytime TDS"],
    "TimeBased": ["Live", "Pre Live", "30", "150", "360", "480", "600", "1440", "2880", "4320", "8640"],
    "Cohort": ["Cohort A", "Cohort B"]
}

# --- Default selections ---
default_query_context = {
    "Brand": "Brand 1",
    "Sport": "Football",
    "Competition": "EPL",
    "Grade": "AA",
    "Market": "WDW",
    "TimeBased": "150",
    "Cohort": "Cohort A"
}

# --- Query Context Dropdowns ---
query_context = {}
for entity, options in entity_options.items():
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
    "Competition": 5,
    "Grade": 3,
    "Market": 7,
    "TimeBased": 15,
    "Cohort": 30
}

entity_weights = {}
for entity in entity_options.keys():
    weight = st.slider(
        f"Weight for {entity}",
        min_value=0,
        max_value=10,
        value=default_weights.get(entity, 1)
    )
    entity_weights[entity] = weight

# --- Rules (latest from user) ---
default_rules = pd.DataFrame({
    "Permutation": [
        "Brand:Brand 1, Sport:Football, Grade:AA, Market:WDW, TimeBased:1440",
        "Brand:Brand 1, Sport:Football, Grade:AA, Market:WDW, TimeBased:360",
        "Brand:Brand 1, Sport:Football, Grade:AA, Market:WDW, TimeBased:120",
        "Brand:Brand 1, Sport:Football, Grade:AA, Market:WDW, TimeBased:30",
        "Brand:Brand 1, Sport:Football, Grade:AA, Market:WDW, TimeBased:Live",
        "Brand:Brand 1, Sport:Football, Grade:AA, Market:First GS",
        "Brand:Brand 1, Sport:Football, Grade:AA, Market:First GS, TimeBased:Live",
        "Brand:Brand 1, Sport:Football, Grade:AA, TimeBased:120",
        "Brand:Brand 1, Sport:Football, Grade:AA, TimeBased:30",
        "Brand:Brand 1, Sport:Football, Grade:AA, TimeBased:Live",
        "Brand:Brand 1, Sport:Football, Grade:AA",
        "Brand:Brand 1, Sport:Football, Competition:La Liga, TimeBased:120",
        "Brand:Brand 1, Sport:Football, Competition:La Liga, TimeBased:30",
        "Brand:Brand 1, Sport:Football, Competition:La Liga, TimeBased:Live",
        "Brand:Brand 1, Sport:Football, Competition:EPL, Market:WDW, TimeBased:1440",
        "Brand:Brand 1, Sport:Football, Competition:EPL, Market:WDW",
        "Brand:Brand 1, Sport:Football, Competition:EPL, Market:WDW, TimeBased:Live",
        "Brand:Brand 1, Sport:Football, Market:WDW",
        "Brand:Brand 1, Sport:Football, Market:WDW, TimeBased:30",
        "Brand:Brand 1, Sport:Football, Market:WDW, TimeBased:Live",
        "Brand:Brand 1, Sport:Football, Market:First GS",
        "Brand:Brand 1, Sport:Football, Market:First GS, TimeBased:Live",
        "Brand:Brand 1, Sport:Football",
        "Brand:Brand 1, Sport:Football, Competition:EPL, TimeBased:1440",
        "Brand:Brand 1, Sport:American Football, Market:Anytime TDS, TimeBased:Pre Live",
        "Brand:Brand 1, Sport:American Football, Market:Anytime TDS, TimeBased:Live",
        "Brand:Brand 1, Sport:American Football, Competition:NFL, Market:Anytime TDS, TimeBased:Pre Live",
        "Brand:Brand 1, Sport:American Football, Competition:NFL, Market:Anytime TDS, TimeBased:Live",
        "Brand:Brand 1, Sport:American Football, Grade:AMF_NFL, Market:Anytime TDS, TimeBased:Pre Live",
        "Brand:Brand 1, Sport:American Football, Grade:AMF_NFL, Market:Anytime TDS, TimeBased:600",
        "Brand:Brand 1, Sport:American Football, Grade:AMF_NFL, Market:Anytime TDS, TimeBased:150",
        "Brand:Brand 1, Sport:American Football, Grade:AMF_NFL, Market:Anytime TDS, TimeBased:Live",
        "Brand:Brand 1, Sport:American Football, TimeBased:600, Grade:AMF_NFL",
        "Brand:Brand 1, Sport:American Football, Grade:AMF_NFL, Market:Anytime TDS, TimeBased:150",
        "Brand:Brand 1, Sport:American Football, Cohort:Cohort B, Market:Anytime TDS, TimeBased:150",
        "Brand:Brand 1, Sport:American Football, Cohort:Cohort A",
        "Brand:Brand 1, Sport:American Football, TimeBased:150",
        "Brand:Brand 1, Sport:American Football, Market:Anytime TDS, Grade:AMF_NFL",
        "Brand:Brand 1, Sport:American Football, TimeBased:Pre Live, Cohort:Cohort B",
        "Brand:Brand 1, Sport:American Football, Market:Anytime TDS, Cohort:Cohort A, TimeBased:1440",
        "Brand:Brand 1, Sport:American Football, Cohort:Cohort B, TimeBased:1440, Market:Anytime TDS",
        "Brand:Brand 1, Sport:American Football, Market:Anytime TDS",
        "Brand:Brand 1, Sport:American Football, Cohort:Cohort A, Competition:NFL, Market:Anytime TDS, TimeBased:600",
        "Brand:Brand 1, Sport:American Football, TimeBased:Pre Live, Competition:NFL",
        "Brand:Brand 1, Sport:American Football, Market:Anytime TDS, Grade:AMF_NFL, TimeBased:Live",
        "Brand:Brand 1, Sport:American Football, Competition:NFL, TimeBased:Pre Live, Cohort:Cohort A",
        "Brand:Brand 1, Sport:American Football, Cohort:Cohort B, Market:Anytime TDS, TimeBased:Live",
        "Brand:Brand 1, Sport:American Football, Cohort:Cohort B, Competition:NFL, Grade:AMF_NFL, TimeBased:Live",
        "Brand:Brand 1, Sport:American Football, TimeBased:1440, Market:Anytime TDS, Competition:NFL",
        "Brand:Brand 1, Sport:American Football, TimeBased:150, Market:Anytime TDS, Competition:NFL, Cohort:Cohort B",
        "Brand:Brand 1, Sport:American Football, Grade:AMF_NFL, TimeBased:150, Competition:NFL, Market:Anytime TDS, Cohort:Cohort B",
        "Brand:Brand 1, Sport:American Football, Cohort:Cohort A, Grade:AMF_NFL, Market:Anytime TDS",
        "Brand:Brand 1, Sport:American Football, Market:Anytime TDS, Competition:NFL",
        "Brand:Brand 1, Sport:American Football, TimeBased:Pre Live, Market:Anytime TDS",
        "Brand:Brand 1, Sport:American Football, Market:Anytime TDS, Grade:AMF_NFL, TimeBased:600, Competition:NFL, Cohort:Cohort B",
        "Brand:Brand 1, Sport:American Football, Competition:NFL, TimeBased:150, Grade:AMF_NFL, Cohort:Cohort A, Market:Anytime TDS",
        "Brand:Brand 1, Sport:American Football, TimeBased:Live, Market:Anytime TDS, Grade:AMF_NFL, Cohort:Cohort B",
        "Brand:Brand 1, Sport:American Football, Cohort:Cohort B, Competition:NFL",
        "Brand:Brand 1, Sport:American Football, Grade:AMF_NFL",
        "Brand:Brand 1, Sport:American Football, Market:Anytime TDS, TimeBased:600",
        "Brand:Brand 1, Sport:American Football",
        "Brand:Brand 1, Sport:American Football, Market:Anytime TDS, Competition:NFL, TimeBased:Live",
        "Brand:Brand 1, Sport:American Football, Competition:NFL, Cohort:Cohort A, Market:Anytime TDS, TimeBased:Live",
        "Brand:Brand 1, Sport:American Football, TimeBased:Pre Live",
        "Brand:Brand 1, Sport:American Football, Competition:NFL, Grade:AMF_NFL, TimeBased:Live, Cohort:Cohort B, Market:Anytime TDS",
        "Brand:Brand 1, Sport:American Football, Market:Anytime TDS, TimeBased:1440, Grade:AMF_NFL",
        "Brand:Brand 1, Sport:American Football, Grade:AMF_NFL, TimeBased:Live",
        "Brand:Brand 1, Sport:American Football, Cohort:Cohort A, Competition:NFL, Market:Anytime TDS",
        "Brand:Brand 1, Sport:American Football, Grade:AMF_NFL, Cohort:Cohort B, TimeBased:150, Market:Anytime TDS",
        "Brand:Brand 1, Sport:American Football, TimeBased:Pre Live, Market:Anytime TDS, Cohort:Cohort B, Grade:AMF_NFL",
        "Brand:Brand 1, Sport:American Football, TimeBased:150, Cohort:Cohort A",
        "Brand:Brand 1, Sport:American Football, Competition:NFL, TimeBased:600, Market:Anytime TDS",
    ],
    "Strategy": [
        "strategy_001",
        "strategy_002",
        "strategy_003",
        "strategy_004",
        "strategy_005",
        "strategy_006",
        "strategy_007",
        "strategy_008",
        "strategy_009",
        "strategy_010",
        "strategy_011",
        "strategy_012",
        "strategy_013",
        "strategy_014",
        "strategy_015",
        "strategy_016",
        "strategy_017",
        "strategy_018",
        "strategy_019",
        "strategy_020",
        "strategy_021",
        "strategy_022",
        "strategy_023",
        "strategy_024",
        "strategy_025a",
        "strategy_025b",
        "strategy_026a",
        "strategy_026b",
        "strategy_026c",
        "strategy_027",
        "strategy_028",
        "strategy_026d",
        "strategy_AF_001",
        "strategy_AF_002",
        "strategy_AF_003",
        "strategy_AF_004",
        "strategy_AF_005",
        "strategy_AF_006",
        "strategy_AF_007",
        "strategy_AF_008",
        "strategy_AF_009",
        "strategy_AF_010",
        "strategy_AF_011",
        "strategy_AF_012",
        "strategy_AF_013",
        "strategy_AF_014",
        "strategy_AF_015",
        "strategy_AF_016",
        "strategy_AF_017",
        "strategy_AF_018",
        "strategy_AF_019",
        "strategy_AF_020",
        "strategy_AF_021",
        "strategy_AF_022",
        "strategy_AF_023",
        "strategy_AF_024",
        "strategy_AF_025",
        "strategy_AF_026",
        "strategy_AF_027",
        "strategy_AF_028",
        "strategy_AF_029",
        "strategy_AF_030",
        "strategy_AF_031",
        "strategy_AF_032",
        "strategy_AF_033",
        "strategy_AF_034",
        "strategy_AF_035",
        "strategy_AF_036",
        "strategy_AF_037",
        "strategy_AF_038",
        "strategy_AF_039",
        "strategy_AF_040",
    ]
})

# --- Rule Editor ---
st.subheader("📋 Define Your Rules")
rules_data = st.data_editor(
    default_rules,
    use_container_width=True,
    num_rows="dynamic",
    height=450
)

# --- Run Matching ---
if st.button("▶️ Run Matching"):
    try:
        def extract_entity_value(entry):
            entity, value = entry.split(":", 1)
            return entity.strip(), value.strip()

        def compute_score(permutation):
            return sum(entity_weights.get(entity, 0) for entity, _ in map(extract_entity_value, permutation))

        # Match only if each entity:value in the rule matches the query context exactly
        def matches_query(permutation):
            for entity, value in map(extract_entity_value, permutation):
                if query_context.get(entity) != value:
                    return False
            return True

        def includes_brand_and_sport(permutation):
            entities = [e for e, _ in map(extract_entity_value, permutation)]
            return "Brand" in entities and "Sport" in entities

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

        matched_rules = []
        for rule in rules:
            perm = rule["permutation"]
            strategy = rule["strategy"]
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
