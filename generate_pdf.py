import markdown2
from weasyprint import HTML, CSS
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
md_path = os.path.join(base_dir, "DVAPI_Vulnerability_Report.md")
pdf_path = os.path.join(base_dir, "DVAPI_Vulnerability_Report.pdf")

with open(md_path, "r") as f:
    md_content = f.read()

html_body = markdown2.markdown(
    md_content,
    extras=["tables", "fenced-code-blocks", "header-ids"]
)

css = """
@page {
    size: A4;
    margin: 2cm 2.2cm 2cm 2.2cm;
    @bottom-right {
        content: "Page " counter(page) " of " counter(pages);
        font-size: 9pt;
        color: #888;
    }
}

* { box-sizing: border-box; }

body {
    font-family: "DejaVu Sans", "Liberation Sans", Arial, sans-serif;
    font-size: 10.5pt;
    line-height: 1.6;
    color: #1a1a1a;
}

h1 {
    font-size: 22pt;
    color: #0d1b2a;
    border-bottom: 3px solid #c0392b;
    padding-bottom: 8px;
    margin-top: 0;
    margin-bottom: 20px;
}

h2 {
    font-size: 14pt;
    color: #0d1b2a;
    border-left: 4px solid #c0392b;
    padding-left: 10px;
    margin-top: 30px;
    page-break-after: avoid;
}

h3 {
    font-size: 12pt;
    color: #1a3a5c;
    margin-top: 24px;
    page-break-after: avoid;
}

h4 {
    font-size: 10.5pt;
    color: #333;
    margin-top: 16px;
    page-break-after: avoid;
}

p { margin: 6px 0 10px 0; }

a { color: #1a3a5c; text-decoration: none; }

/* Tables */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0;
    font-size: 9.5pt;
    page-break-inside: avoid;
}

thead tr {
    background-color: #0d1b2a;
    color: #ffffff;
}

th {
    padding: 8px 10px;
    text-align: left;
    font-weight: bold;
}

td {
    padding: 7px 10px;
    border-bottom: 1px solid #dde3ea;
    vertical-align: top;
}

tbody tr:nth-child(even) {
    background-color: #f4f6f9;
}

tbody tr:nth-child(odd) {
    background-color: #ffffff;
}

/* Code blocks */
pre {
    background-color: #1e1e1e;
    color: #d4d4d4;
    padding: 12px 14px;
    border-radius: 4px;
    font-size: 8.5pt;
    font-family: "DejaVu Sans Mono", "Courier New", monospace;
    overflow-x: auto;
    page-break-inside: avoid;
    margin: 10px 0;
    border-left: 3px solid #c0392b;
}

code {
    font-family: "DejaVu Sans Mono", "Courier New", monospace;
    font-size: 8.5pt;
    background-color: #eef0f3;
    padding: 1px 4px;
    border-radius: 3px;
    color: #c0392b;
}

pre code {
    background-color: transparent;
    color: #d4d4d4;
    padding: 0;
}

/* Images */
img {
    max-width: 100%;
    border: 1px solid #ccd2da;
    border-radius: 4px;
    margin: 10px 0;
    display: block;
    page-break-inside: avoid;
}

/* Lists */
ul, ol {
    margin: 8px 0;
    padding-left: 22px;
}

li { margin-bottom: 4px; }

/* Horizontal rule */
hr {
    border: none;
    border-top: 1px solid #dde3ea;
    margin: 24px 0;
}

/* Cover-style first heading */
h1:first-of-type {
    margin-top: 10px;
}

/* Keep finding headings with their content */
h3 { page-break-before: auto; }
"""

full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>DVAPI Vulnerability Report</title>
</head>
<body>
{html_body}
</body>
</html>"""

HTML(
    string=full_html,
    base_url=base_dir
).write_pdf(
    pdf_path,
    stylesheets=[CSS(string=css)]
)

print(f"PDF saved to: {pdf_path}")
