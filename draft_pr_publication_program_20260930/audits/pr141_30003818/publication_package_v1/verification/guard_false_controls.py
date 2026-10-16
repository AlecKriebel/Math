"""Exercise an exact source-extracted diagnostic guard without running its suite."""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
import ast
import json
import os
import sys

root = Path(__file__).resolve().parent
specifications = json.loads((root / "DIAGNOSTIC_SPECIFICATIONS.json").read_text())
role = sys.argv[1]
spec = next(item for item in specifications["roles"] if item["role"] == role)
source = root / spec["path"]
data = source.read_bytes()
tree = ast.parse(data, filename=str(source))
guard = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == spec["guard"])
namespace = {"N": 0, "counts": {}, "checks": 0, "groups": {}, "C": Counter()}
exec(compile(ast.Module(body=[guard], type_ignores=[]), str(source), "exec"), namespace)
arguments = list(spec["false_guard_arguments"])
positive = [True if argument is False else argument for argument in arguments]
namespace[spec["guard"]](*positive)
try:
    namespace[spec["guard"]](*arguments)
except (RuntimeError, AssertionError) as error:
    if str(error) != "portable_false_control":
        raise
    exception_type = type(error).__name__
    rejected = True
else:
    raise RuntimeError("false diagnostic guard was accepted")
print(json.dumps({"verdict": "PASS_FALSE_GUARD_REJECTED", "role": role,
                  "guard": spec["guard"], "actual_process_PID": os.getpid(),
                  "UTC": datetime.now(timezone.utc).isoformat(),
                  "optimized": bool(sys.flags.optimize), "positive_accepted": True,
                  "false_rejected": rejected, "exception_type": exception_type,
                  "source_sha256": sha256(data).hexdigest(),
                  "scope": "Exact AST-extracted source guard; does not execute diagnostic suite or prove the theorem."}, indent=2))
