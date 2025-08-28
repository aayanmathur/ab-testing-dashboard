import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import warnings
warnings.filterwarnings('ignore')

def load_data():
    """Load and prepare the dataset"""
    df = pd.read_csv('data/AB_data.csv')
    return df

def inspect_data(df):
    """Inspect the dataset structure and quality"""
    inspection = {
        'shape': df.shape,
        'columns': df.columns.tolist(),
        'dtypes': df.dtypes.to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'promotion_counts': df['Promotion'].value_counts().to_dict(),
        'sample_data': df.head().to_dict()
    }
    return inspection

def get_summary_stats(df):
    """Get basic summary statistics"""
    summary = df.groupby('Promotion').agg({
        'SalesInThousands': ['count', 'mean', 'std', 'sum']
    }).round(2)
    summary.columns = ['Sample_Size', 'Mean_Sales', 'Std_Sales', 'Total_Sales']
    return summary

def perform_anova(df):
    """Perform ANOVA test to compare promotions"""
    promo1 = df[df['Promotion'] == 1]['SalesInThousands']
    promo2 = df[df['Promotion'] == 2]['SalesInThousands']
    promo3 = df[df['Promotion'] == 3]['SalesInThousands']
    
    f_stat, p_value = stats.f_oneway(promo1, promo2, promo3)
    
    return {
        'f_statistic': round(f_stat, 4),
        'p_value': round(p_value, 4),
        'significant': p_value < 0.05
    }

def tukey_posthoc(df):
    """Perform Tukey's HSD post-hoc test"""
    tukey = pairwise_tukeyhsd(
        endog=df['SalesInThousands'],
        groups=df['Promotion'],
        alpha=0.05
    )
    return tukey

def business_insights(df):
    """Generate business recommendations"""
    summary = get_summary_stats(df)
    best_promo = summary['Mean_Sales'].idxmax()
    worst_promo = summary['Mean_Sales'].idxmin()
    
    revenue_lift = (summary.loc[best_promo, 'Mean_Sales'] - 
                   summary.loc[worst_promo, 'Mean_Sales'])
    
    return {
        'best_promotion': best_promo,
        'worst_promotion': worst_promo,
        'revenue_lift': round(revenue_lift, 2)
    }

if __name__ == "__main__":
    print("=== A/B Testing Data Analysis ===\n")
    
    # Load and inspect data
    df = load_data()
    inspection = inspect_data(df)
    
    print("DATASET OVERVIEW:")
    print(f"Shape: {inspection['shape']}")
    print(f"Columns: {inspection['columns']}")
    print(f"Missing values: {inspection['missing_values']}")
    print(f"Promotion distribution: {inspection['promotion_counts']}")
    
    print("\nSUMMARY STATISTICS:")
    print(get_summary_stats(df))
    
    print("\n STATISTICAL TESTS:")
    anova_results = perform_anova(df)
    print(f"ANOVA F-statistic: {anova_results['f_statistic']}")
    print(f"P-value: {anova_results['p_value']}")
    print(f"Significant difference: {anova_results['significant']}")
    
    print("\n BUSINESS INSIGHTS:")
    insights = business_insights(df)
    print(f"Best promotion: {insights['best_promotion']}")
    print(f"Revenue lift: ${insights['revenue_lift']}k")