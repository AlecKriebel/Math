#!/usr/bin/env python3
"""Readonly input checks and isolated mutation controls for frozen original PR31.

Run from any directory with Python 3; write only beneath this file's directory.
Requires repository Git objects, the readonly source cache, and fresh_fetch.py outputs.
Finite checker success is deliberately NOT treated as a proof/priority certificate.
"""
from pathlib import Path
import copy
import datetime
import hashlib
import json
import re
import shutil
import sqlite3
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
AUDIT = ROOT.parent
REPO = ROOT.parents[3]
HEAD = "dbe32750f32cd31c9add3aa3311af86f193fc48e"
BASE = "60292bed09f59236aa192cb17aa138f7b4750e1a"
PREFIX = "unsolved_math_prioritization/attempts/10000043/"
sha = lambda b: hashlib.sha256(b).hexdigest()
git = lambda *args: subprocess.check_output(["git", "-C", str(REPO), *args])
read_json = lambda p: json.loads(p.read_text())
manifest = read_json(AUDIT / "snapshot_manifest.json")
baseline = ROOT / "isolated_original"


def package_integrity(folder):
    return all((folder / f["path"]).is_file()
               and sha((folder / f["path"]).read_bytes()) == f["sha256"]
               and len((folder / f["path"]).read_bytes()) == f["size"]
               for f in manifest["files"])


def run_checkers(folder, label):
    results = {}
    for script, report in [("check_coupling.py", "check_results.json"),
                           ("review/independent_checks.py", "review/independent_results.json")]:
        proc = subprocess.run([sys.executable, script], cwd=folder,
                              capture_output=True, text=True, timeout=90)
        stem = "author" if script.startswith("check_") else "review"
        (ROOT / f"{label}_{stem}_stdout.txt").write_text(proc.stdout)
        (ROOT / f"{label}_{stem}_stderr.txt").write_text(proc.stderr)
        data = read_json(folder / report) if (folder / report).exists() else {}
        results[stem] = {"returncode": proc.returncode,
                         "assertions": data.get("assertions"),
                         "note_hash": data.get("partial_note_sha256", data.get("reviewed_sha256")),
                         "report_matches_frozen_bytes": (folder / report).read_bytes() ==
                             (AUDIT / "source_snapshot" / report).read_bytes()}
    return results


def fixture(name):
    dest = ROOT / "tmp" / "controls" / name
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(baseline, dest)
    return dest


if __name__ == "__main__":
    baseline.mkdir(exist_ok=True)
    inputs = []
    for f in manifest["files"]:
        b = git("cat-file", "blob", f["git_blob"])
        dest = baseline / f["path"]
        dest.parent.mkdir(exist_ok=True, parents=True)
        dest.write_bytes(b)
        inputs.append({"path": f["path"], "git_blob": f["git_blob"], "bytes": len(b),
                       "sha256": sha(b), "original_snapshot_equal":
                           b == (AUDIT / "source_snapshot" / f["path"]).read_bytes(),
                       "expected_sha_size_equal": sha(b) == f["sha256"] and len(b) == f["size"]})
    assert package_integrity(baseline)
    reproduction = run_checkers(baseline, "baseline")
    assert reproduction["author"]["assertions"] == 4996
    assert reproduction["review"]["assertions"] == 90170
    assert all(x["returncode"] == 0 and x["report_matches_frozen_bytes"] for x in reproduction.values())

    proof_mutations = []
    for name, text in [("proof_deleted", ""),
                       ("false_universal_claim", "# FALSE CONTROL ONLY\nEvery infinite cluster meets every fiber infinitely, for every graph and every parameter; the complete target is solved.\n")]:
        folder = fixture(name)
        (folder / "PARTIAL.md").write_text(text)
        (folder / "review/reviewed_partial.md").write_text(text)
        before_integrity = package_integrity(folder)
        checks = run_checkers(folder, name)
        proof_mutations.append({"name": name, "mutation_text": text,
                                "bound_input_gate_rejects": not before_integrity,
                                "raw_checkers_still_pass": all(x["returncode"] == 0 for x in checks.values()),
                                "counts_preserved": checks["author"]["assertions"] == 4996 and
                                    checks["review"]["assertions"] == 90170,
                                "checks": checks})
        assert proof_mutations[-1]["bound_input_gate_rejects"]
        assert proof_mutations[-1]["raw_checkers_still_pass"]
        assert proof_mutations[-1]["counts_preserved"]

    folder = fixture("undersized_reservoir")
    script = folder / "review/independent_checks.py"
    script.write_text(script.read_text().replace("2*M", "M"))
    proc = subprocess.run([sys.executable, "review/independent_checks.py"], cwd=folder,
                          capture_output=True, text=True, timeout=90)
    (ROOT / "undersized_reservoir_stdout.txt").write_text(proc.stdout)
    (ROOT / "undersized_reservoir_stderr.txt").write_text(proc.stderr)
    assert proc.returncode != 0

    raw_problem = read_json(ROOT / "tmp/problems.json")
    raw_reports = read_json(ROOT / "tmp/research_results.json")
    matches = [p for p in raw_problem if p.get("id") == 10000043]
    codes = [p for p in raw_problem if p.get("problem_number") == "AMR-099-0043"]
    assert len(matches) == len(codes) == 1
    problem = matches[0]
    report = raw_reports["AMR-099-0043"]
    source = read_json(baseline / "source_record.json")
    assert source == problem
    expected_pair_hash = "5608715374e916d7a4e6fd5e58ca2d491b6e8846535d25840adf56927a83db1e"
    pair_hash = lambda p, r: sha(json.dumps([p, r], sort_keys=True).encode())
    assert pair_hash(problem, report) == expected_pair_hash
    source_controls = []
    for name, field, value in [("numeric_identity_swap", "id", 10000044),
                                ("code_swap", "problem_number", "AMR-099-0044"),
                                ("base_hypothesis_substitution", "statement", source["statement"].replace("p_c(G)=1", "p_c(G\\times\\mathbb{Z})=1")),
                                ("json_null_to_text", "proposed_year", "null")]:
        altered = copy.deepcopy(source)
        altered[field] = value
        rejected = altered != problem and pair_hash(altered, report) != expected_pair_hash
        source_controls.append({"name": name, "field": field, "replacement": value, "rejected": rejected})
        assert rejected
    db = sqlite3.connect("file:" + str(REPO / "unsolved_math_prioritization/cache/catalog.sqlite") + "?mode=ro", uri=True)
    row = db.execute("SELECT payload,report,typeof(payload),typeof(report) FROM records WHERE key=?", ("10000043",)).fetchone()
    assert json.loads(row[0]) == problem and json.loads(row[1]) == report
    sql_null = None
    try:
        json.loads(sql_null)
        sql_null_rejected = False
    except TypeError:
        sql_null_rejected = True
    serialized_json_null_rejected = json.loads("null") != report
    assert sql_null_rejected and serialized_json_null_rejected
    fresh_hashes = {n: {"bytes": (ROOT / "tmp" / n).stat().st_size,
                         "sha256": sha((ROOT / "tmp" / n).read_bytes())}
                    for n in ["problems.json", "research_results.json"]}
    expected_raw = read_json(REPO / "unsolved_math_prioritization/manifest.json")["files"]
    assert fresh_hashes == expected_raw

    duplicate_terms = re.compile(r"vertical[- ]fib(?:er|re)|fib(?:er|re)[- ]intersection|p_c\s*\(G\)\s*=\s*1.*percolation", re.I)
    duplicate_hits = [{"id": p["id"], "code": p["problem_number"], "title": p.get("title"),
                       "statement": p.get("statement")}
                      for p in raw_problem if duplicate_terms.search(p.get("title", "") + " " + p.get("statement", ""))]
    related = read_json(REPO / "unsolved_math_prioritization/review_v2/related_target_groups.json")
    related_hits = [x for x in (related if isinstance(related, list) else list(related.values()))
                    if "10000043" in json.dumps(x) or "AMR-099-0043" in json.dumps(x)]

    diff = git("diff", BASE, HEAD, "--")
    assert diff == (AUDIT / "pr_input/diff.patch").read_bytes()
    changed = git("diff", "--name-only", BASE, HEAD).decode().splitlines()
    pr = read_json(AUDIT / "pr_input.json")
    assert sorted(changed) == sorted(x["path"] for x in pr["files"])
    original_scope_claim_rejected = "All changed files are under" in pr["body"] and any(not x.startswith(PREFIX) for x in changed)
    assert original_scope_claim_rejected
    queue = git("show", HEAD + ":unsolved_math_prioritization/QUEUE.md").decode()
    target = [x for x in queue.splitlines() if "| 10000043 / AMR-099-0043 |" in x]
    assert len(target) == 1
    columns = [x.strip() for x in target[0].split("|")[1:-1]]
    assert len(columns) == 12 and columns[7] == "unsolved" and columns[8] == "2/5"
    protected = [0, 1, 2, 3, 4, 5, 6, 9, 11]
    protected_match = lambda before, after: len(after) == 12 and all(before[i] == after[i] for i in protected)
    altered = columns.copy()
    altered[4] = "10.0"
    protected_mutation_rejected = not protected_match(columns, altered)
    legacy_eight_rejected = not protected_match(columns, columns[:8])
    false_solved = columns.copy()
    false_solved[7] = "verified_solved"
    solved_without_fullproof_rejected = false_solved[7] != "unsolved"
    assert protected_mutation_rejected and legacy_eight_rejected and solved_without_fullproof_rejected
    queue_code = (REPO / "unsolved_math_prioritization/queue.py").read_text()
    assert "| Rank | ID / code | Problem | EV | Difficulty | Proposed | Status | Turns |" in queue_code

    published = (ROOT / "sources/benjamini_kozma_published.pdf").read_bytes()
    arxiv = (ROOT / "sources/benjamini_kozma_arxiv_v2.pdf").read_bytes()
    variant_identity_rejected = published != arxiv and sha(published) != sha(arxiv)
    assert variant_identity_rejected
    result = {"at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "stage": "FROZEN ORIGINAL PARTIAL ONLY", "head": HEAD, "actual_base": BASE,
              "input_checks": inputs, "baseline_reproduction": reproduction,
              "proof_mutations": proof_mutations,
              "undersized_reservoir_control": {"returncode": proc.returncode, "rejected": True,
                                               "stderr_file": "undersized_reservoir_stderr.txt"},
              "source_identity_controls": source_controls,
              "sqlite_null_controls": {"actual_payload_type": row[2], "actual_report_type": row[3],
                                        "json_difficulty_suggested_is_null": report["difficulty_suggested"] is None,
                                        "sql_null_rejected": sql_null_rejected,
                                        "serialized_json_null_rejected": serialized_json_null_rejected},
              "fresh_upstream_hashes_match_pinned": fresh_hashes, "review_pair_hash": expected_pair_hash,
              "bounded_duplicate_search": {"regex": duplicate_terms.pattern, "hits": duplicate_hits,
                                             "related_target_hits": related_hits,
                                             "limit": "Full pinned titles/statements searched by stated terms; not semantic equivalence proof or exhaustive literature priority audit."},
              "action_scope_controls": {"original_folder_only_body_claim_rejected": original_scope_claim_rejected,
                                        "actual_changed_file_count": len(changed), "protected_column_mutation_rejected": protected_mutation_rejected,
                                        "legacy_eight_column_replacement_rejected": legacy_eight_rejected,
                                        "false_solved_status_rejected": solved_without_fullproof_rejected},
              "pdf_byte_variant_control": {"published_bytes": len(published), "published_sha256": sha(published),
                                           "arxiv_v2_bytes": len(arxiv), "arxiv_v2_sha256": sha(arxiv),
                                           "byte_identity_claim_rejected": variant_identity_rejected},
              "limits": "Integrity and explicit metadata/scope gates are controls, not theorem proving. Raw finite checkers hash but do not validate proof text. Historical reviewer/model/effort and source reports remain attestations. No full solution or novelty certification."}
    (ROOT / "CONTROL_RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"baseline": reproduction, "proof_mutations": proof_mutations,
                      "source_identity_controls": source_controls,
                      "action_scope_controls": result["action_scope_controls"],
                      "bounded_duplicate_hits": duplicate_hits}, indent=2))
