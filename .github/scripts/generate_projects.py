#!/usr/bin/env python3

import json
import sys
from html import escape


def load_projects(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def create_project_card(project):
    name = escape(project.get("name", "Project"))
    repo = project.get("repo", "")
    logo = project.get("logo", "")
    description = escape(project.get("description", ""))
    tags = project.get("tags", [])

    tag_html = " ".join(
        f'<span class="tag">{escape(tag)}</span>'
        for tag in tags
    )

    # Logo is stored in the main repository.
    logo_url = (
        f"https://raw.githubusercontent.com/2004-abhi/2004-abhi/main/{logo}"
    )

    repo_url = f"https://github.com/{repo}"

    return f"""
    <a class="card" href="{repo_url}">
      <img class="logo" src="{logo_url}" alt="{name}">
      <div class="content">
        <h2>{name}</h2>
        <p>{description}</p>
        <div class="tags">{tag_html}</div>
      </div>
    </a>
    """


def create_svg(projects):
    cards = "\n".join(create_project_card(p) for p in projects)

    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>
body {{
    margin: 0;
    padding: 30px;
    background: #0a101f;
    color: #f8fafc;
    font-family: Arial, sans-serif;
}}

.container {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 18px;
}}

.card {{
    display: flex;
    align-items: center;
    gap: 18px;
    padding: 20px;
    min-height: 120px;

    background: #111827;
    border: 1px solid #263449;
    border-radius: 16px;

    text-decoration: none;
    color: #f8fafc;
}}

.logo {{
    width: 72px;
    height: 72px;
    object-fit: contain;
    border-radius: 12px;
}}

.content {{
    flex: 1;
}}

h2 {{
    margin: 0 0 8px 0;
    font-size: 20px;
}}

p {{
    margin: 0 0 12px 0;
    color: #94a3b8;
    font-size: 14px;
    line-height: 1.5;
}}

.tags {{
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
}}

.tag {{
    padding: 4px 8px;
    background: #1e293b;
    border-radius: 6px;
    color: #22d3ee;
    font-size: 11px;
}}

@media (max-width: 700px) {{
    .container {{
        grid-template-columns: 1fr;
    }}
}}
</style>
</head>

<body>

<div class="container">
{cards}
</div>

</body>
</html>
"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg"
    width="1200"
    height="{max(250, len(projects) * 180)}">

    <foreignObject x="0" y="0" width="1200"
                   height="{max(250, len(projects) * 180)}">
        <div xmlns="http://www.w3.org/1999/xhtml">
            {html}
        </div>
    </foreignObject>

</svg>
"""


def main():
    if len(sys.argv) != 3:
        print("Usage: generate_projects.py merged.json output_directory")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = sys.argv[2]

    projects = load_projects(input_file)

    import os
    os.makedirs(output_dir, exist_ok=True)

    svg = create_svg(projects)

    output_file = os.path.join(output_dir, "projects.svg")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(svg)

    print(f"Generated {output_file}")


if __name__ == "__main__":
    main()