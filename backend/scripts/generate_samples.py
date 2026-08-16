from fastapi.testclient import TestClient
import sys
import os
import re

# Ensure backend package is importable when running the script
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root not in sys.path:
    sys.path.insert(0, root)

from app.main import app


def slugify(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:60]


def main():
    client = TestClient(app)
    instructions = [
        "Test the login functionality.",
        "Test the registration functionality.",
        "Search for a product and verify the search results.",
        "Add a product to the cart and verify that it was added successfully.",
        "Test the complete shopping workflow from product search to cart.",
        "Test the form with valid and invalid inputs.",
        "Check whether all important navigation links are working.",
        "Find broken links on the website.",
        "Check the website for accessibility issues.",
        "Check the website for UI-related issues.",
        "Check the website for performance issues.",
        "Explore the website and identify functional bugs.",
        "Explore the website up to a specified depth and identify defects.",
        "Test the website and verify whether the detected failure is an actual website bug or an automation failure.",
        "Test the website and automatically recover if a webpage element or selector has changed.",
        "Perform a complete test of the website and generate an evidence-based bug report.",
        "Verify payment and checkout integration under simulated load.",
        "Check session management and concurrency safety for user sessions.",
    ]

    out_dir = os.path.join(os.path.dirname(__file__), "..", "reports", "samples")
    os.makedirs(out_dir, exist_ok=True)

    for idx, instr in enumerate(instructions, start=1):
        resp = client.post("/api/reports/generate", json={"url": "https://example.com", "instruction": instr})
        if resp.status_code != 200:
            print(f"Failed to generate for: {instr}", resp.status_code, resp.text)
            continue
        data = resp.json()
        html = data.get("report_html", "")
        filename = f"{idx:02d}-{slugify(instr)}.html"
        path = os.path.join(out_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print("Wrote", path)


if __name__ == "__main__":
    main()
