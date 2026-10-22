"""Verify the externally pinned PR781 source and optional exact PDF; no writes."""
from pathlib import Path
import argparse, hashlib, json, subprocess, sys
sys.dont_write_bytecode = True
# The externally pinned manifest authenticates this verifier and its builder.
# It is a release-integrity check, not a signature or formal proof.
ROOT = Path(__file__).absolute().parent
ORIGINAL = "audit/original/unsolved_math_prioritization/attempts/4600024"
HEAD = "4a38c3ccc4cac918fb75fd4b97449f3ebd2e0f7f"

def run(script, arguments, optimized):
    command = [sys.executable, "-I", "-B"] + (["-O"] if optimized else []) + [str(ROOT / script)] + arguments
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=180)
    need(result.returncode == 0, "Replay failed: " + script + "\n" + result.stdout + result.stderr)
    return {"script": script, "optimized": optimized,
            "stdout_sha256": hashlib.sha256(result.stdout.encode()).hexdigest(),
            "stderr_sha256": hashlib.sha256(result.stderr.encode()).hexdigest(),
            "result": parse(result.stdout)}

def verify(pin, pdf, replay):
    # Authenticate the helper before executing its module-level code.
    manifest_raw = (ROOT / "MANIFEST.json").read_bytes()
    if hashlib.sha256(manifest_raw).hexdigest() != pin:
        raise ValueError("External source manifest pin mismatch")
    manifest = json.loads(manifest_raw)
    helper_rows = [row for row in manifest["files"] if row["path"] == "build_package.py"]
    if len(helper_rows) != 1:
        raise ValueError("Missing or repeated builder binding")
    helper = ROOT / "build_package.py"
    if helper.is_symlink() or not helper.is_file():
        raise ValueError("Nonregular builder")
    helper_bytes = helper.read_bytes()
    row = helper_rows[0]
    if len(helper_bytes) != row["bytes"] or hashlib.sha256(helper_bytes).hexdigest() != row["sha256"]:
        raise ValueError("Builder binding differs")
    import importlib.util
    spec = importlib.util.spec_from_file_location("pr781_authenticated_builder", helper)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    global closed_source, parse, identity, need, inventory
    closed_source, parse, identity, need, inventory = [getattr(module, name) for name in
        ("closed_source", "parse", "identity", "need", "inventory")]
    files = closed_source(ROOT, pin)
    source = parse(files["audit/ROOT_SOURCE_IDENTITY.json"])
    need(source["reviewed_head"] == HEAD and len(source["original_files"]) == 48, "Wrong original scope")
    expected = set()
    for row in source["original_files"]:
        name = "audit/original/" + row["path"]
        need(name not in expected, "Repeated original")
        expected.add(name)
        raw = files[name]
        need(identity(raw) == {k: row[k] for k in ("bytes", "sha256")}, "Original bytes differ")
        need(hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == row["git_blob"],
             "Original Git identity differs")
    actual = {name for name in files if name.startswith("audit/original/")}
    need(actual == expected, "Original 48-file closure differs")
    selected = parse(files["audit/SELECTED_PUBLIC_RECORD.json"])
    canonical = json.dumps([selected["problem"], selected["prior_research"]], sort_keys=True).encode()
    need(hashlib.sha256(canonical).hexdigest() == source["review_hash"], "Complete selected-record binding differs")
    gate = parse(files["audit/PRIORITY_GATE.json"])
    need(gate["result"] == "PASS_FOR_COMPLETE_EFFECTIVE_CRITERION_WITH_BOUNDED_PRIORITY"
         and gate["known_full_predecessors"] == [] and gate["remaining_mathematical_issues"] == []
         and gate["blocking_statement_or_credit_issues"] == []
         and gate["historical_first_priority_certified"] is False
         and gate["current_worldwide_open_status_certified"] is False, "Scope gate differs")
    binding = parse(files["PREPRINT_BINDINGS.json"])
    need(identity(files["paper.tex"]) == binding["paper.tex"], "TeX binding differs")
    if pdf:
        need(identity(pdf.read_bytes()) == binding["paper.pdf"], "PDF binding differs")
    checks = []
    if replay:
        fixed = [
          (ORIGINAL + "/verify_publication.py",
           ["--manifest-sha256", "456354ccba417ae9f29d0844bd66a680c43997df0a4ddfedfaad26f1cd811047", "--inventory-only"]),
          ("audit/root_reproduction/verify_math_review_custody.py", []),
          ("audit/priority_audit/verify_custody.py",
           ["--expected-manifest-sha256", "6223de076929683e0cffef1ce5a222bd7cd278c718718f686d5958bc87a56163"]),
          ("audit/priority_adversary01/verify_custody.py",
           ["--expected-manifest-sha256", "faf34ee84bcc0c22a3c0c63b42e4758bbbac565ac6b5287fff42dcc72ea3d760",
            "--expected-checker-sha256", "21956eefb9967c9d965ed108a151a689b88b1eec43bf528e6129a69fc017c4b7"]),
          (ORIGINAL + "/author/verify_math.py", []),
          (ORIGINAL + "/audit/independent_checks.py", []),
          (ORIGINAL + "/second_review/checks.py", []),
          ("audit/math_automata/independent_automata.py", []),
          ("audit/math_symbolic/independent_checks.py", [])]
        for optimized in [False, True]:
            for script, arguments in fixed:
                checks.append(run(script, arguments, optimized))
    need(inventory(ROOT) == files, "Source changed during verification")
    return {"result": "PASS", "source_manifest_sha256": pin, "source_files": len(files),
            "original_files": 48, "exact_head": HEAD,
            "pdf_binding_checked": bool(pdf), "replay_runs": checks,
            "scope": "Exact byte custody and finite controls; no formal theorem proof, practical general solver or complete priority certification."}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected-manifest-sha256", required=True)
    parser.add_argument("--pdf", type=Path)
    parser.add_argument("--replay", action="store_true")
    args = parser.parse_args()
    try:
        result = verify(args.expected_manifest_sha256, args.pdf, args.replay)
    except Exception as exc:
        print(json.dumps({"result": "FAIL", "error": str(exc)}))
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    sys.exit(main())
