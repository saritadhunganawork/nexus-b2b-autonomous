"""
=============================================================================
NEXUS B2B INTELLIGENCE CORP.
EXECUTIVE HTML DOSSIER EXPORTER
Transforms raw Markdown dossiers into high-trust, printable executive web dossiers.
=============================================================================
"""

import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DOSSIERS_DIR = BASE_DIR / "data" / "dossiers"
HTML_OUT_DIR = BASE_DIR / "data" / "dossiers" / "html"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        :root {{
            --bg-primary: #0a0d14;
            --bg-card: #111622;
            --border-color: #1e293b;
            --text-main: #f1f5f9;
            --text-muted: #94a3b8;
            --accent: #38bdf8;
            --accent-glow: rgba(56, 189, 248, 0.15);
            --gold: #f59e0b;
            --success: #10b981;
        }}
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        }}
        body {{
            background-color: var(--bg-primary);
            color: var(--text-main);
            line-height: 1.6;
            padding: 40px 20px;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 48px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        }}
        .header {{
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 24px;
            margin-bottom: 32px;
        }}
        .badge {{
            display: inline-block;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            padding: 4px 10px;
            border-radius: 6px;
            background: var(--accent-glow);
            color: var(--accent);
            border: 1px solid var(--accent);
            margin-bottom: 12px;
        }}
        h1 {{
            font-size: 28px;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 8px;
        }}
        h2 {{
            font-size: 20px;
            font-weight: 600;
            color: var(--accent);
            margin-top: 32px;
            margin-bottom: 16px;
            border-left: 3px solid var(--accent);
            padding-left: 12px;
        }}
        h3 {{
            font-size: 16px;
            font-weight: 600;
            color: #ffffff;
            margin-top: 24px;
            margin-bottom: 12px;
        }}
        p, li {{
            color: var(--text-muted);
            font-size: 14.5px;
            margin-bottom: 14px;
        }}
        blockquote {{
            background: rgba(56, 189, 248, 0.05);
            border-left: 3px solid var(--accent);
            padding: 16px;
            border-radius: 6px;
            font-style: italic;
            color: #e2e8f0;
            margin: 20px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 24px 0;
            font-size: 13.5px;
        }}
        th, td {{
            padding: 12px 16px;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }}
        th {{
            background: #161e2e;
            color: #ffffff;
            font-weight: 600;
        }}
        tr:hover td {{
            background: rgba(255, 255, 255, 0.02);
        }}
        .cta-btn {{
            display: inline-block;
            background: #2563eb;
            color: #ffffff;
            font-weight: 600;
            text-decoration: none;
            padding: 14px 28px;
            border-radius: 8px;
            font-size: 15px;
            margin: 20px 0;
            transition: all 0.2s ease;
            box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3);
        }}
        .cta-btn:hover {{
            background: #1d4ed8;
            transform: translateY(-1px);
        }}
        .footer {{
            margin-top: 48px;
            padding-top: 20px;
            border-top: 1px solid var(--border-color);
            font-size: 12px;
            color: #64748b;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <span class="badge">Nexus B2B Intelligence • Confidential Report</span>
            {body}
        </div>
        <div class="footer">
            Generated autonomously by Nexus B2B Intelligence Enterprise Engine • All Rights Reserved
        </div>
    </div>
</body>
</html>
"""

def md_to_html_simple(md_text):
    # Minimalist robust markdown parser for HTML dossier rendering
    lines = md_text.split("\n")
    html_lines = []
    in_table = False
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        
        # Headers
        if stripped.startswith("# "):
            html_lines.append(f"<h1>{stripped[2:]}</h1>")
        elif stripped.startswith("## "):
            html_lines.append(f"<h2>{stripped[3:]}</h2>")
        elif stripped.startswith("### "):
            html_lines.append(f"<h3>{stripped[4:]}</h3>")
        # Blockquote
        elif stripped.startswith("> "):
            html_lines.append(f"<blockquote>{stripped[2:]}</blockquote>")
        # Tables
        elif stripped.startswith("|"):
            parts = [p.strip() for p in stripped.split("|")[1:-1]]
            if not in_table:
                html_lines.append("<table><thead><tr>")
                for p in parts:
                    html_lines.append(f"<th>{p}</th>")
                html_lines.append("</tr></thead><tbody>")
                in_table = True
            elif all(p.startswith(":") or p.startswith("-") for p in parts if p):
                continue # delimiter row
            else:
                html_lines.append("<tr>")
                for p in parts:
                    html_lines.append(f"<td>{p}</td>")
                html_lines.append("</tr>")
        else:
            if in_table:
                html_lines.append("</tbody></table>")
                in_table = False
            
            # Format buttons/links
            if "buy.stripe.com" in stripped:
                btn_match = re.search(r'\[([^\]]+)\]\((https://buy\.stripe\.com[^\)]+)\)', stripped)
                if btn_match:
                    text, url = btn_match.groups()
                    html_lines.append(f'<p><a href="{url}" class="cta-btn">{text}</a></p>')
                    continue
            
            # Normal paragraph with bold replacement
            formatted = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', stripped)
            formatted = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', formatted)
            html_lines.append(f"<p>{formatted}</p>")
            
    if in_table:
        html_lines.append("</tbody></table>")
        
    return "\n".join(html_lines)

def export_all():
    HTML_OUT_DIR.mkdir(parents=True, exist_ok=True)
    count = 0
    for md_file in DOSSIERS_DIR.glob("*.md"):
        with open(md_file, "r", encoding="utf-8") as f:
            md_content = f.read()
            
        title = md_file.stem.replace("_", " ")
        html_body = md_to_html_simple(md_content)
        full_html = HTML_TEMPLATE.format(title=title, body=html_body)
        
        out_file = HTML_OUT_DIR / f"{md_file.stem}.html"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(full_html)
        count += 1
        
    print(f"[EXPORTER] Successfully converted {count} Markdown dossiers into executive HTML reports in {HTML_OUT_DIR}")

if __name__ == "__main__":
    export_all()
