from jinja2 import Template


def generate_html_template():
    html_template = """
    <!DOCTYPE html>
    <html>
    
    <head>
        <style>
            body { font-family: Arial, sans-serif; }
            table { width: 100%; border-collapse: collapse; }
            th, td { padding: 8px 12px; border: 1px solid #dddddd; }
            th { background-color: #f2f2f2; }
            .plotly-graph { text-align: center; }
        </style>
    </head>

    <h1> Cairs Motor Guard Analysis Report </h1>
    
    </html>
    """

    template = Template(html_template)

    # html_report = template.render(plotly_chart=fig.to_html(full_html=False))

    html_report = template.render()

    return html_report


def generate_report():

    html_report = generate_html_template()

    with open("report.html", "w") as f:
        f.write(html_report)
