from jinja2 import Environment, FileSystemLoader
import pandas as pd
from weasyprint import HTML
import datetime
import os

# Create a basic Pandas table for demo
df = pd.DataFrame({
    "Nom": ["Alice", "Bob", "Charlie"],
    "Score": [85, 92, 78]
})
table_html = df.to_html(index=False, classes="dataframe", border=0)

# Sample report structure
report_structure = [
    {
        "title": "NOMBRE DE LIGNES PAR TABLE",
        "description": "Résumé du nombre de lignes pour chaque table.",
        "table_html": table_html,
        "image_path": None,
        "children": []
    },
    {
        "title": "LES DATES",
        "description": "Analyse des dates dans les données.",
        "table_html": None,
        "image_path": None,
        "children": [
            {
                "title": "TABLE A",
                "description": None,
                "table_html": None,
                "image_path": None,
                "children": [
                    {
                        "title": "VARIABLE DATE N°1",
                        "description": None,
                        "table_html": None,
                        "image_path": None,
                        "children": [
                            {
                                "title": "RÉPARTITION DE L’ANNÉE",
                                "description": "Répartition annuelle.",
                                "table_html": table_html,
                                "image_path": "plot1.png",  # placeholder
                                "children": []
                            }
                        ]
                    }
                ]
            }
        ]
    }
]

# Metadata
context = {
    "title": "Rapport de Validation",
    "author": "Équipe Qualité",
    "date": datetime.date.today().strftime("%d/%m/%Y"),
    "report_structure": report_structure
}

# Template string from user
template_html = """<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>{{ title }}</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 2em; counter-reset: page; }
    h1, h2, h3, h4, h5, h6 { color: #2c3e50; margin-top: 1.5em; }
    table { border-collapse: collapse; width: 100%; margin: 1em 0; }
    th, td { border: 1px solid #ccc; padding: 6px; text-align: left; }
    th { background-color: #f5f5f5; }
    img { max-width: 100%; margin: 1em 0; }
    .section { margin-bottom: 2em; }
    .toc ul { list-style: none; padding-left: 1em; }
    .toc a { text-decoration: none; color: #2980b9; }
    .toc a:hover { text-decoration: underline; }

    @page {
      @bottom-right {
        content: "Page " counter(page);
      }
    }

    .page-number::after {
      content: leader('.') target-counter(attr(href), page);
      float: right;
    }
  </style>
</head>
<body>

<h1>{{ title }}</h1>
<p><strong>Auteur :</strong> {{ author }}<br><strong>Date :</strong> {{ date }}</p>

<hr>

<div class="toc">
  <h2>Table des matières</h2>
  {% macro render_toc_auto(section_list, prefix="") %}
    <ul>
    {% for section in section_list %}
      {% set number = prefix ~ (loop.index) %}
      <li>
        <a class="page-number" href="#s{{ number }}">{{ number }} {{ section.title }}</a>
        {% if section.children %}
          {{ render_toc_auto(section.children, number ~ ".") }}
        {% endif %}
      </li>
    {% endfor %}
    </ul>
  {% endmacro %}
  {{ render_toc_auto(report_structure) }}
</div>

<hr>

{% macro render_section_auto(section_list, level=2, prefix="") %}
  {% for section in section_list %}
    {% set number = prefix ~ (loop.index) %}
    <div class="section">
      <h{{ level }} id="s{{ number }}">{{ number }} {{ section.title }}</h{{ level }}>
      {% if section.description %}
        <p>{{ section.description }}</p>
      {% endif %}
      {% if section.table_html %}
        {{ section.table_html | safe }}
      {% endif %}
      {% if section.image_path %}
        <img src="{{ section.image_path }}" alt="Plot for {{ section.title }}">
      {% endif %}
      {% if section.children %}
        {{ render_section_auto(section.children, level+1, number ~ ".") }}
      {% endif %}
    </div>
  {% endfor %}
{% endmacro %}

{{ render_section_auto(report_structure) }}

</body>
</html>"""

# Write template to file (optional)
template_path = "template.html"
with open(template_path, "w", encoding="utf-8") as f:
    f.write(template_html)

# Jinja2 render
env = Environment(loader=FileSystemLoader("."), autoescape=True)
template = env.get_template("template.html")
rendered_html = template.render(context)

# Save HTML report
html_file = "report.html"
with open(html_file, "w", encoding="utf-8") as f:
    f.write(rendered_html)

# Generate PDF
pdf_file = "report.pdf"
HTML(html_file).write_pdf(pdf_file)

print(f"Report saved: {html_file} and {pdf_file}")
