#!/usr/bin/env python3
"""Replay the current diagnostic in disposable lane-local copies.

The accepted OPERATOR_CHECK.json is read and hash-checked, never rewritten.
Both ordinary and optimized Python must pass the original result byte-for-byte
and reject a deliberately corrupted expected scalar before writing acceptance.
"""

import ast
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


class NormalizeChecks(ast.NodeTransformer):
    """Normalize guard syntax only, preserving every mathematical expression."""

    def visit_FunctionDef(self, node):
        if node.name == "need":
            return None
        return self.generic_visit(node)

    def visit_Assert(self, node):
        node.msg = None
        return self.generic_visit(node)

    def visit_Expr(self, node):
        call = node.value
        if isinstance(call, ast.Call) and isinstance(call.func, ast.Name):
            if call.func.id == "need":
                need(len(call.args) == 2 and not call.keywords,
                     "Unexpected explicit guard signature")
                return ast.Assert(test=self.visit(call.args[0]), msg=None)
        return self.generic_visit(node)


def normalized_tree(source):
    return ast.dump(NormalizeChecks().visit(ast.parse(source)),
                    include_attributes=False)


def run_copy(lane, source, flags):
    with tempfile.TemporaryDirectory(prefix=".operator_replay_", dir=lane) as temp:
        folder = Path(temp)
        script = folder / "check_operator_blocks.py"
        script.write_text(source)
        proc = subprocess.run([sys.executable, *flags, str(script)],
                              capture_output=True, check=False)
        output = folder / "OPERATOR_CHECK.json"
        return {"returncode": proc.returncode, "stdout": proc.stdout,
                "stderr": proc.stderr, "output_exists": output.exists(),
                "output": output.read_bytes() if output.exists() else None}


def main():
    lane = Path(__file__).resolve().parent
    source_bytes = (lane / "check_operator_blocks.py").read_bytes()
    source = source_bytes.decode()
    historical = lane / "historical_v1"
    historical_source = (historical / "check_operator_blocks.py").read_text()
    accepted_path = lane / "OPERATOR_CHECK.json"
    accepted = accepted_path.read_bytes()
    need(accepted == (historical / "OPERATOR_CHECK.json").read_bytes(),
         "Accepted output differs from the preserved first accepted bytes")
    need(not any(isinstance(node, ast.Assert)
                 for node in ast.walk(ast.parse(source))),
         "Current acceptance diagnostic still contains removable assertions")
    need(normalized_tree(source) == normalized_tree(historical_source),
         "The repair changed more than guard syntax and its helper function")

    runs = {}
    for name, flags in (("normal", []), ("optimized", ["-O"])):
        result = run_copy(lane, source, flags)
        need(result["returncode"] == 0, name + " replay failed")
        need(result["stderr"] == b"", name + " replay emitted an error")
        need(result["output_exists"], name + " replay did not write acceptance")
        need(result["output"] == accepted,
             name + " accepted output differs byte-for-byte from original")
        need(json.loads(result["output"]) == json.loads(accepted),
             name + " accepted output differs semantically from original")
        runs[name] = result
    need(runs["normal"]["stdout"] == runs["optimized"]["stdout"],
         "Normal and optimized standard output differ")
    need(runs["normal"]["output"] == runs["optimized"]["output"],
         "Normal and optimized acceptance bytes differ")

    original_check = "need(euler_scalar == d,"
    corrupted_check = "need(euler_scalar == d + 1,"
    need(source.count(original_check) == 1,
         "Expected scalar corruption point is not unique")
    corrupted = source.replace(original_check, corrupted_check, 1)
    rejected = {}
    for name, flags in (("normal", []), ("optimized", ["-O"])):
        result = run_copy(lane, corrupted, flags)
        need(result["returncode"] != 0,
             name + " accepted a deliberately corrupted expected Euler scalar")
        need(not result["output_exists"],
             name + " wrote acceptance before rejecting the corrupt scalar")
        need(result["stdout"] == b"",
             name + " printed an acceptance summary before rejection")
        failure = "RuntimeError: Euler scalar differs from orbit cardinality"
        need(result["stderr"].decode().splitlines()[-1] == failure,
             name + " rejected for an unexpected reason")
        rejected[name] = {"returncode": result["returncode"],
                          "acceptance_file_written": result["output_exists"],
                          "stdout_empty": result["stdout"] == b"",
                          "final_error": failure}

    need(accepted_path.read_bytes() == accepted,
         "Replay modified the accepted output")
    need((lane / "check_operator_blocks.py").read_bytes() == source_bytes,
         "Replay modified the current diagnostic source")
    receipt = {
        "status": "passed",
        "replayed_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "python_version": sys.version,
        "disposable_copies": "Temporary directories inside this lane; removed after each run",
        "historical_v1_preserved": True,
        "current_script_sha256": sha256(source_bytes),
        "historical_script_sha256": sha256(historical_source.encode()),
        "accepted_output_sha256": sha256(accepted),
        "normalized_mathematical_AST_identical": True,
        "current_script_contains_assert_nodes": False,
        "success_modes": {
            name: {"python_flags": [] if name == "normal" else ["-O"],
                   "returncode": result["returncode"],
                   "stderr_empty": result["stderr"] == b"",
                   "acceptance_bytes_identical_to_original": result["output"] == accepted,
                   "acceptance_semantics_identical_to_original":
                       json.loads(result["output"]) == json.loads(accepted),
                   "output_sha256": sha256(result["output"]),
                   "stdout_sha256": sha256(result["stdout"]),
                   "stdout": result["stdout"].decode()}
            for name, result in runs.items()
        },
        "normal_optimized_stdout_byte_equal": True,
        "normal_optimized_acceptance_byte_equal": True,
        "negative_control": {
            "mutation": original_check + " -> " + corrupted_check,
            "purpose": "Deliberately incorrect expected scalar, isolated to disposable copies",
            "corrupted_source_sha256": sha256(corrupted.encode()),
            "modes": rejected
        },
        "accepted_output_unchanged": True,
        "unlimited_mathematical_proof_scope_unchanged": True
    }
    (lane / "REPLAY_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"status": receipt["status"],
                      "normal_optimized_output_byte_equal": True,
                      "both_corrupted_expected_scalar_runs_rejected": True,
                      "accepted_output_unchanged": True}, indent=2))


if __name__ == "__main__":
    main()
