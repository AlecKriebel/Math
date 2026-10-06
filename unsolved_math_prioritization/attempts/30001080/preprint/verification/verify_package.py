#!/usr/bin/env python3
"""Standard-library verifier for byte custody and finite exact controls only."""
import hashlib
import json
import pathlib
import subprocess
import sys

MANIFEST = "manifest.json"
EXPECTED_CASES = (
    ("turn1", "checks/turn1_checks.py", "expected/turn1_output.json", 18814),
    ("turn2", "checks/turn2_checks.py", "expected/turn2_output.json", 75172),
    ("independent", "independent_review/independent_check.py",
     "expected/INDEPENDENT_CHECKS.json", 186869),
)


class VerificationFailure(Exception):
    def __init__(self, code, detail):
        self.code = code
        self.detail = detail
        super().__init__(detail)


def fail(code, detail):
    raise VerificationFailure(code, detail)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError) as exc:
        fail("INVALID_JSON", "{}: {}".format(path.name, exc))


def check_manifest(root):
    manifest_path = root / MANIFEST
    if manifest_path.is_symlink() or not manifest_path.is_file():
        fail("MANIFEST_MISSING", "manifest.json must be a regular non-symlink file")
    manifest = load_json(manifest_path)
    if not isinstance(manifest, dict) or manifest.get("format_version") != 1:
        fail("MANIFEST_SCHEMA", "unsupported manifest schema")
    if manifest.get("self_exception") != MANIFEST:
        fail("MANIFEST_SCHEMA", "only manifest.json may be excluded from its own hash list")
    rows = manifest.get("files")
    if not isinstance(rows, list) or not rows:
        fail("MANIFEST_SCHEMA", "nonempty files list required")
    declared = {}
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"path", "bytes", "sha256"}:
            fail("MANIFEST_SCHEMA", "file records require path, bytes, sha256")
        relative = row["path"]
        if not isinstance(relative, str):
            fail("MANIFEST_SCHEMA", "file path must be a string")
        path = pathlib.PurePosixPath(relative)
        if (not relative or path.is_absolute() or path.as_posix() != relative
                or ".." in path.parts or "\\" in relative
                or relative == MANIFEST or relative in declared):
            fail("MANIFEST_SCHEMA", "unsafe, duplicate, or self-hashed path")
        size, sha = row["bytes"], row["sha256"]
        if (type(size) is not int or size < 0 or not isinstance(sha, str)
                or len(sha) != 64 or any(c not in "0123456789abcdef" for c in sha)):
            fail("MANIFEST_SCHEMA", "invalid byte count or SHA256")
        declared[relative] = row
    actual = set()
    for path in root.rglob("*"):
        if path.is_symlink():
            fail("SYMLINK", "package contains a symbolic link")
        if path.is_file():
            actual.add(path.relative_to(root).as_posix())
        elif not path.is_dir():
            fail("NONREGULAR_FILE", "package contains a nonregular filesystem entry")
    required = set(declared) | {MANIFEST}
    if actual != required:
        fail("FILE_SET", "missing={} extra={}".format(
            sorted(required - actual), sorted(actual - required)))
    for relative, row in sorted(declared.items()):
        data = (root / relative).read_bytes()
        if len(data) != row["bytes"] or digest(data) != row["sha256"]:
            fail("HASH_MISMATCH", relative)
    controls = manifest.get("controls")
    expected = [dict(label=a, script=b, expected_stdout=c, assertions=d)
                for a, b, c, d in EXPECTED_CASES]
    if controls != expected:
        fail("MANIFEST_SCHEMA", "control set or expected assertion totals changed")
    for row in expected:
        if row["script"] not in declared or row["expected_stdout"] not in declared:
            fail("MANIFEST_SCHEMA", "control inputs must be hash-covered")
    return len(declared), expected


def run_child(root, tail):
    argv = [sys.executable, "-E", "-B"] + tail
    try:
        result = subprocess.run(argv, cwd=str(root), stdin=subprocess.DEVNULL,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                timeout=120, check=False)
    except subprocess.TimeoutExpired:
        fail("CHILD_TIMEOUT", "control or dependency probe exceeded 120 seconds")
    except OSError as exc:
        fail("CHILD_LAUNCH", str(exc))
    if result.returncode != 0:
        fail("CHILD_EXIT", "returncode={} stderr={}".format(
            result.returncode, result.stderr.decode("utf-8", errors="replace")))
    if result.stderr:
        fail("CHILD_STDERR", result.stderr.decode("utf-8", errors="replace"))
    return result.stdout


def main():
    if sys.flags.optimize != 0 or not __debug__:
        fail("OPTIMIZED_PYTHON", "assertions must be enabled; do not use -O or -OO")
    if sys.version_info < (3, 9):
        fail("PYTHON_VERSION", "Python 3.9 or newer is required")
    root = pathlib.Path(__file__).resolve().parent
    covered, cases = check_manifest(root)
    probe = "import json,sys,sympy; print(json.dumps({'sympy':sympy.__version__,'optimize':sys.flags.optimize},sort_keys=True))"
    try:
        runtime = json.loads(run_child(root, ["-c", probe]).decode("utf-8"))
    except (UnicodeError, ValueError):
        fail("DEPENDENCY_PROBE", "dependency probe did not return JSON")
    if runtime != {"sympy": "1.14.0", "optimize": 0}:
        fail("DEPENDENCY_VERSION", "requires Sympy==1.14.0 and enabled assertions")
    reports = []
    for row in cases:
        output = run_child(root, [str(root / row["script"])])
        expected = (root / row["expected_stdout"]).read_bytes()
        if output != expected:
            fail("STDOUT_MISMATCH", "{}: expected SHA256 {}, actual SHA256 {}".format(
                row["label"], digest(expected), digest(output)))
        try:
            report = json.loads(output.decode("utf-8"))
        except (UnicodeError, ValueError):
            fail("CONTROL_JSON", row["label"])
        if report.get("status") != "PASS" or report.get("assertions") != row["assertions"]:
            fail("CONTROL_STATUS", row["label"])
        reports.append(dict(label=row["label"], assertions=row["assertions"],
                            complete_stdout_sha256=digest(output)))
    print(json.dumps({
        "status": "PASS_FINITE_CONTROLS_AND_PACKAGE_HASHES",
        "manifest_covered_files": covered,
        "controls": reports,
        "child_python_flags": ["-E", "-B"],
        "sympy": "1.14.0",
        "analytical_theorem_verified_by_this_program": False,
        "formal_machine_proof": False,
        "strict_xi_erased_Cox_allocation_converse_verified": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except VerificationFailure as exc:
        print(json.dumps({"status": "FAIL", "code": exc.code,
                          "detail": exc.detail}, sort_keys=True), file=sys.stderr)
        sys.exit(2)
    except (OSError, TypeError, KeyError, AttributeError) as exc:
        print(json.dumps({"status": "FAIL", "code": "PACKAGE_ERROR",
                          "detail": str(exc)}, sort_keys=True), file=sys.stderr)
        sys.exit(2)
