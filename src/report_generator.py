from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_report(df, file_path="report.pdf"):

    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    content = []

    # Title
    content.append(Paragraph("Business Analytics Report", styles['Title']))
    content.append(Spacer(1, 10))

    # KPIs
    if 'Sales' in df.columns:
        total_sales = df['Sales'].sum()
        content.append(Paragraph(f"Total Sales: {total_sales:.2f}", styles['Normal']))

    if 'Profit' in df.columns:
        total_profit = df['Profit'].sum()
        content.append(Paragraph(f"Total Profit: {total_profit:.2f}", styles['Normal']))

    if 'Sales' in df.columns:
        avg_sales = df['Sales'].mean()
        content.append(Paragraph(f"Average Sales: {avg_sales:.2f}", styles['Normal']))

    content.append(Spacer(1, 10))

    # Insights
    if 'Region' in df.columns and 'Sales' in df.columns:
        top_region = df.groupby('Region')['Sales'].sum().idxmax()
        content.append(Paragraph(f"Top Region: {top_region}", styles['Normal']))

    doc.build(content)

    return file_path