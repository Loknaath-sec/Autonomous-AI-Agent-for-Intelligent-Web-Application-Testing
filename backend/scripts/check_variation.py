from fastapi.testclient import TestClient
import sys
import os

# make sure app package is importable
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root not in sys.path:
    sys.path.insert(0, root)

from app.main import app

client = TestClient(app)

instructions = [
    "Test the login functionality.",
    "Check the website for accessibility issues.",
    "Check the website for performance issues.",
    "Find broken links on the website.",
]

for instr in instructions:
    resp = client.post("/api/reports/generate", json={"url": "https://example.com", "instruction": instr})
    print('\n--- Instruction:', instr)
    if resp.status_code != 200:
        print('ERROR', resp.status_code, resp.text)
        continue
    data = resp.json()
    html = data.get('report_html', '')
    # crude extraction of the Findings and Recommendations lists from the HTML
    import re
    def extract_section(html, heading):
        m = re.search(fr"<h2>{heading}</h2>\s*<ul>(.*?)</ul>", html, re.S | re.I)
        if not m:
            return []
        items = re.findall(r"<li>(.*?)</li>", m.group(1), re.S | re.I)
        return [re.sub(r"<.*?>", "", it).strip() for it in items]

    findings = extract_section(html, 'Findings')
    recommendations = extract_section(html, 'Recommendations')
    print('Findings:')
    for f in findings:
        print(' -', f)
    print('Recommendations:')
    for rec in recommendations:
        print(' -', rec)
