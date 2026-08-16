from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_reports_vary_per_instruction():
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

    outputs = []
    for instr in instructions:
        resp = client.post("/api/reports/generate", json={"url": "https://example.com", "instruction": instr})
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert "report_html" in data
        outputs.append(data["report_html"]) 

    # Ensure outputs are not all identical; expect uniqueness across instructions
    unique_count = len(set(outputs))
    assert unique_count == len(outputs), f"Expected all reports to be unique, got {unique_count}/{len(outputs)} unique"
