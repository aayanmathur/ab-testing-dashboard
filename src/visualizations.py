import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

def create_promotion_comparison(df):
    """Box plot comparing sales across promotions"""
    fig = px.box(
        df, 
        x='Promotion', 
        y='SalesInThousands',
        title='Sales Distribution by Promotion Type',
        color='Promotion',
        color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1']
    )
    
    fig.update_layout(
        xaxis_title='Promotion Type',
        yaxis_title='Sales (Thousands $)',
        showlegend=False,
        height=400
    )
    
    return fig

def create_bar_chart(summary_stats):
    """Bar chart of mean sales by promotion"""
    fig = go.Figure(data=[
        go.Bar(
            x=summary_stats.index,
            y=summary_stats['Mean_Sales'],
            text=summary_stats['Mean_Sales'],
            textposition='auto',
            marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1']
        )
    ])
    
    fig.update_layout(
        title='Average Sales by Promotion',
        xaxis_title='Promotion Type',
        yaxis_title='Average Sales (Thousands $)',
        height=400
    )
    
    return fig

def create_time_series(df):
    """Time series showing sales trends by week"""
    weekly_data = df.groupby(['week', 'Promotion'])['SalesInThousands'].mean().reset_index()
    
    fig = px.line(
        weekly_data,
        x='week',
        y='SalesInThousands',
        color='Promotion',
        title='Sales Trends Over 4 Weeks',
        markers=True,
        color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1']
    )
    
    fig.update_layout(
        xaxis_title='Week',
        yaxis_title='Average Sales (Thousands $)',
        height=400
    )
    
    return fig

def create_market_analysis(df):
    """Sales by market size and promotion"""
    market_summary = df.groupby(['MarketSize', 'Promotion'])['SalesInThousands'].mean().reset_index()
    
    fig = px.bar(
        market_summary,
        x='MarketSize',
        y='SalesInThousands',
        color='Promotion',
        title='Sales Performance by Market Size',
        barmode='group',
        color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1']
    )
    
    fig.update_layout(
        xaxis_title='Market Size',
        yaxis_title='Average Sales (Thousands $)',
        height=400
    )
    
    return fig

def create_statistical_summary(anova_results, tukey_results):
    """Create a summary table of statistical results"""
    
    # Extract Tukey results
    tukey_df = pd.DataFrame(data=tukey_results._results_table.data[1:], 
                           columns=tukey_results._results_table.data[0])
    
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=['Statistical Test', 'Value', 'Interpretation'],
            fill_color='lightblue',
            align='left'
        ),
        cells=dict(
            values=[
                ['ANOVA F-statistic', 'P-value', 'Effect', 'Tukey HSD'],
                [anova_results['f_statistic'], 
                 anova_results['p_value'], 
                 'Significant' if anova_results['significant'] else 'Not Significant',
                 'See detailed results below'],
                ['Measures overall difference between groups',
                 'Probability of observing this difference by chance',
                 'There IS a statistically significant difference',
                 'Shows which specific promotions differ']
            ],
            fill_color='white',
            align='left'
        )
    )])
    
    fig.update_layout(
        title='Statistical Test Results Summary',
        height=300
    )
    
    return fig