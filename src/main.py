from jinja2 import Environment, FileSystemLoader
import pandas as pd
import datetime

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
    "etude" : "Etude constances",
    "extraction": "Extraction 1",
    "year_ext_start": "2000",
    "year_ext_end": "2020",
    "domain_list": "DCIR, DC, COVID",
    "date": datetime.date.today().strftime("%d/%m/%Y"),
    "report_structure": report_structure
}


# Jinja2 render
env = Environment(loader=FileSystemLoader("./templates"), autoescape=True)
template = env.get_template("report.html")
rendered_html = template.render(context)

# Save HTML report
out_html_file = "../tmp/report.html"
with open(out_html_file, "w", encoding="utf-8") as f:
    f.write(rendered_html)

