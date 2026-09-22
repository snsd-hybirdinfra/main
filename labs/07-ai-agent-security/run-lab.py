#!/usr/bin/env python3
"""Run a deterministic local tool gateway experiment; no LLM or external API."""
import json
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen

POLICY = json.loads(Path(__file__).with_name("policy.json").read_text(encoding="utf-8-sig"))


class FactsHandler(BaseHTTPRequestHandler):
    def log_message(self, *_args):
        pass

    def do_GET(self):
        if self.path != "/facts":
            self.send_error(404)
            return
        body = b'{"source":"local-fixture","fact":"synthetic"}'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


class Gate:
    def __init__(self, root, port):
        self.root = root.resolve()
        self.port = port
        self.spent = 0
        self.approved = set()
        self.audit = []

    def decide(self, tool, target):
        if tool not in POLICY["allowed_tools"]:
            return "tool_denied"
        cost = POLICY["cost_units"][tool]
        if self.spent + cost > POLICY["max_cost_units"]:
            return "budget_exceeded"
        if tool in ("read_artifact", "write_report"):
            path = Path(target).resolve()
            if not path.is_relative_to(self.root):
                return "path_denied"
            if tool == "write_report" and path != self.root / "report.txt":
                return "path_denied"
        if tool == "http_get":
            parsed = urlparse(target)
            allowed = POLICY["allowed_http"]
            if (parsed.scheme != allowed["scheme"]
                    or parsed.hostname != allowed["host"]
                    or parsed.port != self.port
                    or parsed.path != allowed["path"]
                    or parsed.query or parsed.fragment
                    or parsed.username or parsed.password):
                return "network_denied"
        if tool in POLICY["approval_required"] and tool not in self.approved:
            return "approval_required"
        return "allow"

    def execute(self, tool, target, value=None):
        decision = self.decide(tool, target)
        if decision == "allow":
            if tool == "read_artifact":
                Path(target).read_text(encoding="utf-8")
            elif tool == "http_get":
                with urlopen(target, timeout=2) as response:
                    json.load(response)
            elif tool == "write_report":
                Path(target).write_text(value, encoding="utf-8")
            self.spent += POLICY["cost_units"][tool]
        self.audit.append({"tool": tool, "decision": decision})
        return decision


def main():
    with tempfile.TemporaryDirectory(prefix="lab07-agent-") as work:
        root = Path(work)
        artifact = root / "facts.txt"
        artifact.write_text("synthetic source\n", encoding="utf-8")
        report = root / "report.txt"
        server = ThreadingHTTPServer(("127.0.0.1", 0), FactsHandler)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        try:
            port = server.server_port
            gate = Gate(root, port)
            outcomes = {
                "read": gate.execute("read_artifact", artifact),
                "unknown_tool": gate.execute("shell", "echo test"),
                "path_escape": gate.execute("read_artifact", root.parent / "outside.txt"),
                "external_http": gate.execute("http_get", "https://example.com/facts"),
                "local_http": gate.execute("http_get", f"http://127.0.0.1:{port}/facts"),
                "write_without_approval": gate.execute("write_report", report, "synthetic report"),
            }
            report_absent_before_approval = not report.exists()
            gate.approved.add("write_report")  # Synthetic approval in test harness.
            outcomes["write_after_approval"] = gate.execute(
                "write_report", report, "synthetic report"
            )
            outcomes["over_budget"] = gate.execute("read_artifact", artifact)
            expected = {
                "read": "allow", "unknown_tool": "tool_denied",
                "path_escape": "path_denied", "external_http": "network_denied",
                "local_http": "allow", "write_without_approval": "approval_required",
                "write_after_approval": "allow", "over_budget": "budget_exceeded",
            }
            if (outcomes != expected or not report_absent_before_approval
                    or report.read_text(encoding="utf-8") != "synthetic report"
                    or gate.spent != 4):
                raise AssertionError("unexpected policy enforcement result")
            print(json.dumps({
                "status": "pass",
                "results": outcomes,
                "report_absent_before_approval": report_absent_before_approval,
                "cost_units_spent": gate.spent,
                "cost_units_limit": POLICY["max_cost_units"],
                "audit": gate.audit,
                "runtime": "deterministic local harness; no LLM or external request",
            }, ensure_ascii=False, indent=2))
        finally:
            server.shutdown()
            server.server_close()
            worker.join(timeout=2)


if __name__ == "__main__":
    main()
