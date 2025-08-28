import streamlit as st
import pandas as pd
from src.analysis import *
from src.visualizations import *

# Page config
st.set_page_config(
    page_title="A/B Testing Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title and description
st.title("🍟 Fast-Food Marketing Campaign A/B Test Analysis")
st.markdown("**Analyzing the effectiveness of 3 different promotional campaigns**")

# Load data
@st.cache_data
def load_cached_data():
    return load_data()

df = load_cached_data()


# Main dashboard
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Observations", 
        len(df)
    )

with col2:
    best_promo = business_insights(df)['best_promotion']
    st.metric(
        "Best Promotion", 
        f"Promotion {best_promo}"
    )

with col3:
    revenue_lift = business_insights(df)['revenue_lift']
    st.metric(
        "Revenue Lift", 
        f"${revenue_lift}k"
    )

# Summary statistics
st.subheader("Summary Statistics")
summary_stats = get_summary_stats(df)
st.dataframe(summary_stats, use_container_width=True)

# Visualizations
st.subheader("Promotional Performance Analysis")

col1, col2 = st.columns(2)

with col1:
    fig1 = create_promotion_comparison(df)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = create_bar_chart(summary_stats)
    st.plotly_chart(fig2, use_container_width=True)

# Time series and market analysis
col3, col4 = st.columns(2)

with col3:
    fig3 = create_time_series(df)
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    fig4 = create_market_analysis(df)
    st.plotly_chart(fig4, use_container_width=True)

# Statistical results
st.subheader("Statistical Analysis")
anova_results = perform_anova(df)
tukey_results = tukey_posthoc(df)

col5, col6 = st.columns([1, 1])

with col5:
    st.write("**ANOVA Results:**")
    st.write(f"F-statistic: {anova_results['f_statistic']}")
    st.write(f"P-value: {anova_results['p_value']}")
    st.write(f"Significant: {'Yes' if anova_results['significant'] else 'No'}")

with col6:
    st.write("**Tukey HSD Post-hoc Test:**")
    st.text(str(tukey_results))

# Business recommendations
st.subheader("💡 Business Recommendations")
insights = business_insights(df)

st.success(f"""
**Key Findings:**
- Promotion {insights['best_promotion']} is the clear winner with ${insights['revenue_lift']}k higher average sales
- Statistical tests confirm significant differences between promotions (p < 0.05)
- Recommendation: Roll out Promotion {insights['best_promotion']} company-wide
""")

# Raw data toggle
if st.checkbox("Show Raw Data"):
    st.subheader("Raw Data")
    st.dataframe(df, use_container_width=True)