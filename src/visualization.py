import plotly.express as px

def sales_by_region(df):
    if 'Region' in df.columns and 'Sales' in df.columns:
        fig = px.bar(df, x='Region', y='Sales', title="Sales by Region")
        return fig
    return None


def monthly_sales(df):
    if 'Month' in df.columns and 'Sales' in df.columns:
        monthly = df.groupby('Month')['Sales'].sum().reset_index()
        fig = px.line(monthly, x='Month', y='Sales', title="Monthly Sales Trend")
        return fig
    return None


def category_sales(df):
    if 'Category' in df.columns and 'Sales' in df.columns:
        fig = px.pie(df, names='Category', values='Sales', title="Sales by Category")
        return fig
    return None