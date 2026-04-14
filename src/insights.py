def generate_insights(df):
    insights = []

    # Total Sales
    if 'Sales' in df.columns:
        total_sales = df['Sales'].sum()
        insights.append(f"💰 Total Sales is {total_sales:.2f}")

        avg_sales = df['Sales'].mean()
        insights.append(f"📊 Average Sales is {avg_sales:.2f}")

    # Top Region
    if 'Region' in df.columns and 'Sales' in df.columns:
        top_region = df.groupby('Region')['Sales'].sum().idxmax()
        insights.append(f"🏆 Top performing region is {top_region}")

    # Top Category
    if 'Category' in df.columns and 'Sales' in df.columns:
        top_category = df.groupby('Category')['Sales'].sum().idxmax()
        insights.append(f"📦 Best selling category is {top_category}")

    # Growth
    if 'Sales' in df.columns:
        growth = df['Sales'].pct_change().mean() * 100
        insights.append(f"📈 Average growth rate is {growth:.2f}%")

    return insights