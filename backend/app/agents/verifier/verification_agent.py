from __future__ import annotations

from typing import Any


class VerificationAgent:
    def classify_failure(self, expected: str, observed: str, browser_data: dict[str, Any] | None = None) -> dict[str, Any]:
        browser_data = browser_data or {}
        lower_expected = expected.lower()
        lower_observed = observed.lower()

        if "timeout" in lower_observed or "timed out" in lower_observed:
            return {"status": "FAIL", "classification": "TIMEOUT", "details": "The browser operation timed out; this is not automatically a website bug.", "confidence": 0.82, "evidence": ["timeout"]}
        if "captcha" in lower_observed or "verify you are human" in lower_observed:
            return {"status": "BLOCKED", "classification": "CAPTCHA", "details": "CAPTCHA or bot protection was detected.", "confidence": 0.98, "evidence": ["captcha"]}
        if "401" in lower_observed or "unauthorized" in lower_observed or "login" in lower_expected and "login" in lower_observed:
            return {"status": "FAIL", "classification": "AUTHENTICATION_FAILURE", "details": "Authentication or authorization state appears to be the cause.", "confidence": 0.84, "evidence": ["auth"]}
        if "network" in lower_observed or "failed to fetch" in lower_observed:
            return {"status": "FAIL", "classification": "NETWORK_FAILURE", "details": "A network or fetch issue was observed.", "confidence": 0.8, "evidence": ["network"]}
        if lower_expected not in lower_observed and "not found" not in lower_observed:
            return {"status": "FAIL", "classification": "WEBSITE_DEFECT", "details": "The expected result did not occur and the behavior appears to be a website issue.", "confidence": 0.75, "evidence": ["dom", "url", "text"]}
        return {"status": "PASS", "classification": "PASS", "details": "Expected result was observed.", "confidence": 0.92, "evidence": ["dom", "text"]}
