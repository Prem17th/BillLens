import os
import sys
import io
import json
import time
import pytest

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import server

class MockHandler(server.BillLensHandler):
    """Subclass of BillLensHandler that uses in-memory IO streams for socketless testing."""
    def __init__(self, method="GET", path="/", body=None):
        self.command = method
        self.path = path
        self.headers = {}
        raw_body = b""
        if body is not None:
            if isinstance(body, dict):
                raw_body = json.dumps(body).encode("utf-8")
            elif isinstance(body, str):
                raw_body = body.encode("utf-8")
            else:
                raw_body = body
            self.headers["Content-Length"] = str(len(raw_body))
            self.headers["Content-Type"] = "application/json"

        self.rfile = io.BytesIO(raw_body)
        self.wfile = io.BytesIO()
        self.response_status = None
        self.response_headers = {}

    def send_response(self, code, message=None):
        self.response_status = code

    def send_header(self, keyword, value):
        self.response_headers[keyword] = value

    def end_headers(self):
        pass

    def get_json_response(self):
        self.wfile.seek(0)
        return json.loads(self.wfile.read().decode("utf-8"))

def test_asl_json_validity():
    """Validates that step_function_state_machine.asl.json is valid and contains expected states."""
    asl_path = os.path.join(os.path.dirname(__file__), "..", "step_function_state_machine.asl.json")
    assert os.path.exists(asl_path), "ASL state machine file must exist"
    with open(asl_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert "StartAt" in data
    assert "States" in data
    assert data["StartAt"] == "ExtractInvoiceOCR"
    assert "ArmorIQ_MintIntentGuard" in data["States"]
    assert "ParallelIntelligenceBranch" in data["States"]

def test_health_endpoint():
    """Checks the /api/health endpoint returns 200 with maintainer details."""
    handler = MockHandler("GET", "/api/health")
    handler.do_GET()
    assert handler.response_status == 200
    res = handler.get_json_response()
    assert res["status"] == "ok"
    assert res["app"] == "BillLens"
    assert res["maintainer"] == "Prem T H"

def test_armoriq_status_endpoint():
    """Checks the /api/armoriq/status endpoint for security telemetry."""
    handler = MockHandler("GET", "/api/armoriq/status")
    handler.do_GET()
    assert handler.response_status == 200
    res = handler.get_json_response()
    assert res["service"] == "ArmorIQ Agent Security SDK"
    assert "enforcement_mode" in res
    assert "tokens_issued_count" in res

def test_armoriq_verify_plan_and_audit():
    """Checks that plan verification mints a cryptographic intent token."""
    handler = MockHandler("POST", "/api/armoriq/verify-plan", {
        "goal": "Reconcile supplier prices and audit trade credit",
        "steps": [
            {"action": "detect_price_creep", "sku": "Parle-G 56g"},
            {"action": "check_mandi_arbitrage"}
        ]
    })
    handler.do_POST()
    assert handler.response_status == 200
    res = handler.get_json_response()
    assert "armoriq_token" in res
    token = res["armoriq_token"]
    assert "token_id" in token
    assert "plan_hash" in token
    assert "signature" in token

    # Check that audit log recorded this token
    audit_handler = MockHandler("GET", "/api/armoriq/audit-log")
    audit_handler.do_GET()
    assert audit_handler.response_status == 200
    audit_body = audit_handler.get_json_response()
    assert audit_body["total_tokens"] >= 1
    assert len(audit_body["tokens"]) >= 1

def test_armoriq_enforce_action():
    """Verifies runtime enforcement against signed tokens."""
    handler = MockHandler("POST", "/api/armoriq/enforce-action", {
        "token_id": "tok_live_test123",
        "action": "execute_tre_ds_factoring"
    })
    handler.do_POST()
    assert handler.response_status == 200
    res = handler.get_json_response()
    assert res["action"] == "execute_tre_ds_factoring"

def test_stepfunctions_workflow_and_execution():
    """Tests the AWS Step Functions simulated execution workflow."""
    start_handler = MockHandler("POST", "/api/step-functions/start-execution", {
        "merchant_id": "kirana.ramesh@billlens.in",
        "invoice_id": "INV-TEST-99",
        "distributor": "Bengaluru FMCG Wholesale",
        "sku": "Parle-G 56g",
        "new_unit_rate": 9.80,
        "prev_unit_rate": 9.20,
        "mrp": 12.00
    })
    start_handler.do_POST()
    assert start_handler.response_status == 200
    res = start_handler.get_json_response()
    assert "executionArn" in res
    assert res["status"] == "SUCCEEDED"
    execution_arn = res["executionArn"]

    # Verify execution status
    status_handler = MockHandler("GET", f"/api/step-functions/execution-status?executionArn={execution_arn}")
    status_handler.do_GET()
    assert status_handler.response_status == 200
    status_body = status_handler.get_json_response()
    assert status_body["executionArn"] == execution_arn
    assert status_body["status"] == "SUCCEEDED"

    # Verify list executions
    list_handler = MockHandler("GET", "/api/step-functions/list-executions")
    list_handler.do_GET()
    assert list_handler.response_status == 200
    list_body = list_handler.get_json_response()
    assert "executions" in list_body
    assert len(list_body["executions"]) >= 1

def test_static_index_html_content():
    """Verifies that index.html contains proper metadata, branding, and maintainer attribution."""
    index_path = os.path.join(os.path.dirname(__file__), "..", "index.html")
    assert os.path.exists(index_path)
    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()
    assert "BillLens" in html
    assert "Prem T H" in html
    assert "https://github.com/Prem17th/BillLens" in html
    # Ensure no raw base64 or plaintext keys were accidentally left behind
    assert "ak_live_cbecd97574151f5fb44ee6ebe07dd7507925df62ef956061e47c4e337787b5d6" not in html
    assert "56eb91707cbf415499a959f07c1e82db" not in html
    assert "sk_5acc6cb5d5ebac77ddfcb59e1081a30ef7b424510bc38f24" not in html
