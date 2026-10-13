#!/usr/bin/env python3
"""Read-only reproduction and mutation tests of the frozen PR468 controls.

Intentionally invalid variants live only under this review's mutation_fixtures.
They must not be included as result-bearing verification programs.
"""
from pathlib import Path
import ast
import hashlib
import json
import os
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
FROZEN = HERE.parents[1] / "source_snapshot/unsolved_math_prioritization/attempts/30000689"

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")

def fingerprint():
    return [{"file": str(p.relative_to(FROZEN)), "bytes": p.stat().st_size,
             "sha256": digest(p.read_bytes())}
            for p in sorted(FROZEN.rglob("*")) if p.is_file()]

def execute(path, stem, optimized=False):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    command = [sys.executable] + (["-O"] if optimized else []) + [str(path)]
    started = time.monotonic()
    result = subprocess.run(command, capture_output=True, env=env, timeout=180)
    (HERE / (stem + ".stdout.json")).write_bytes(result.stdout)
    (HERE / (stem + ".stderr.txt")).write_bytes(result.stderr)
    return {"command": command, "exit_code": result.returncode,
            "seconds": round(time.monotonic()-started, 3),
            "stdout_sha256": digest(result.stdout), "stdout_bytes": len(result.stdout),
            "stderr_sha256": digest(result.stderr), "stderr_bytes": len(result.stderr)}

def main():
    before = fingerprint()
    checks = []
    for manifest, root, key, name in [
        ("release/FROZEN_AUTHOR_MANIFEST.json", "release", "files", "path"),
        ("audit/AUDIT_MANIFEST.json", "audit", "audit_files", "file"),
        ("PUBLICATION_MANIFEST.json", ".", "public_payload_files", "path")]:
        records = json.loads((FROZEN / manifest).read_text())[key]
        for record in records:
            p = FROZEN / root / record[name]
            data = p.read_bytes()
            match = len(data)==record["bytes"] and digest(data)==record["sha256"]
            checks.append({"manifest": manifest, "file": str(p.relative_to(FROZEN)),
                           "bytes": len(data), "sha256": digest(data), "match": match})
            require(match, "Frozen manifest mismatch: " + str(p))
    scripts = {"author": FROZEN/"release/check_exact.py",
               "prior_audit": FROZEN/"audit/check_independent.py"}
    outputs = {"author": FROZEN/"release/exact_results.json",
               "prior_audit": FROZEN/"audit/independent_results.json"}
    runs = []
    for label, script in scripts.items():
        code = script.read_text()
        tree = ast.parse(code)
        assert_count = sum(isinstance(n, ast.Assert) for n in ast.walk(tree))
        for optimized in [False, True]:
            stem = label + ("_optimized" if optimized else "_normal")
            record = execute(script, stem, optimized)
            data = (HERE/(stem+".stdout.json")).read_bytes()
            record.update(label=label, optimized=optimized, assert_count=assert_count,
                          byte_match=data==outputs[label].read_bytes())
            require(record["exit_code"]==0 and record["byte_match"], "Reproduction mismatch: "+stem)
            runs.append(record)
            print(json.dumps({"run": stem, "match": True, "seconds": record["seconds"]}), flush=True)
    mutations = {
        "author_retains_missing_face": ("author", "if t <= f:", "if False and t <= f:"),
        "author_zero_vandermonde": ("author", "pow(v+1,power,p)", "0"),
        "author_rank_plus_one": ("author", "return len(basis)", "return len(basis)+1"),
        "author_zero_crossings": ("author", "if tuple(union[::2])==a or tuple(union[::2])==b:", "if False:"),
        "author_all_triples_flag": ("author", "if all(x<=y or y<=x for x,y in [(a,b),(a,c),(b,c)]):", "if True:"),
        "audit_zero_fill": ("prior_audit", "return {pool[j] for j in solve(cols,target)}", "return set()"),
        "audit_wrong_complement_homology": ("prior_audit", "return [len(vs)-r1-1,len(es)-r1-r2]", "return [len(vs)-r1,len(es)-r1-r2]"),
        "audit_zero_crossings": ("prior_audit", "crossings+=tuple(u[::2]) in (s,t)", "crossings+=0"),
        "audit_wrong_paired_boundary": ("prior_audit", "paired={frozenset(t if frozenset(s)==M else s) for s,t in omega if frozenset(s)==M or frozenset(t)==M}", "paired=set()"),
    }
    fixtures = HERE/"mutation_fixtures"
    fixtures.mkdir(exist_ok=True)
    mutation_runs = []
    for name, (label, old, new) in mutations.items():
        code = scripts[label].read_text()
        require(code.count(old)==1, "Nonunique mutation: "+name)
        script = fixtures/(name+".py")
        script.write_text(code.replace(old,new))
        ast.parse(script.read_text())
        for optimized in [False, True]:
            stem = name + ("_optimized" if optimized else "_normal")
            record = execute(script, stem, optimized)
            record.update(mutation=name, optimized=optimized, rejected=record["exit_code"]!=0)
            mutation_runs.append(record)
            print(json.dumps({"mutation": name, "optimized": optimized, "rejected": record["rejected"]}), flush=True)
    after = fingerprint()
    require(before==after, "Frozen files changed")
    write_json(HERE/"reproduction_results.json", {
        "status": "Finite outputs reproduced; original scripts rely on removable assertions",
        "manifest_checks": checks, "runs": runs, "mutation_runs": mutation_runs,
        "frozen_before": before, "frozen_after": after, "frozen_unchanged": True,
        "python": sys.version, "scope": "Finite controls, no universal or novelty certification"})

if __name__=="__main__":
    main()
