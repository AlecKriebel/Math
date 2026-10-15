#!/usr/bin/env python3
"""Replace removable assertions by explicit runtime conditions in separate copies."""
import ast
import difflib
import json
from pathlib import Path
import run_reproduction as rr

HERE = Path(__file__).resolve().parent

def harden(source):
    code = source.read_text()
    lines = code.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1]+len(line))
    replacements = []
    for node in ast.walk(ast.parse(code)):
        if isinstance(node, ast.Assert):
            condition = ast.get_source_segment(code, node.test)
            message = ast.get_source_segment(code, node.msg) if node.msg else repr("original line %d: %s" % (node.lineno, condition))
            replacement = "require((%s), %s)" % (condition, message)
            replacements.append((offsets[node.lineno-1]+node.col_offset,
                                 offsets[node.end_lineno-1]+node.end_col_offset, replacement))
    for begin, end, replacement in sorted(replacements, reverse=True):
        code = code[:begin] + replacement + code[end:]
    first_def = code.index("\ndef ")
    helper = '\ndef require(condition, message):\n    if not condition:\n        raise RuntimeError("Finite control failed: " + str(message))\n\n'
    code = code[:first_def] + helper + code[first_def:]
    rr.require(not any(isinstance(n, ast.Assert) for n in ast.walk(ast.parse(code))), "Residual assert")
    return code, len(replacements)

def main():
    before = rr.fingerprint()
    folder = HERE / "hardened"
    folder.mkdir(exist_ok=True)
    scripts = {"author": rr.FROZEN/"release/check_exact.py", "prior_audit": rr.FROZEN/"audit/check_independent.py"}
    outputs = {"author": rr.FROZEN/"release/exact_results.json", "prior_audit": rr.FROZEN/"audit/independent_results.json"}
    records = []
    copies = {}
    for name, source in scripts.items():
        code, count = harden(source)
        target = folder / source.name
        target.write_text(code)
        copies[name] = target
        patch = "".join(difflib.unified_diff(source.read_text().splitlines(keepends=True), code.splitlines(keepends=True), fromfile="frozen/"+source.name, tofile="hardened/"+source.name))
        (folder/(source.stem+".patch")).write_text(patch)
        record = {"label": name, "replaced_assert_count": count, "file": str(target.relative_to(HERE)), "sha256": rr.digest(target.read_bytes()), "runs": []}
        for optimized in [False, True]:
            stem = "hardened_"+name+("_optimized" if optimized else "_normal")
            run = rr.execute(target, stem, optimized)
            run["byte_match"] = (HERE/(stem+".stdout.json")).read_bytes()==outputs[name].read_bytes()
            rr.require(run["exit_code"]==0 and run["byte_match"], "Hardened mismatch")
            record["runs"].append(run)
        records.append(record)
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
    tests = []
    for name, (label, old, new) in mutations.items():
        code = copies[label].read_text()
        rr.require(code.count(old)==1, "Nonunique mutation")
        script = fixtures/("hardened_"+name+".py")
        script.write_text(code.replace(old,new))
        for optimized in [False, True]:
            stem = "hardened_"+name+("_optimized" if optimized else "_normal")
            test = rr.execute(script, stem, optimized)
            test.update(mutation=name, optimized=optimized, rejected=test["exit_code"]!=0)
            rr.require(test["rejected"], "Hardened control failed to reject "+stem)
            tests.append(test)
    rr.require(before==rr.fingerprint(), "Frozen files changed")
    rr.write_json(HERE/"hardening_results.json", {"copies": records, "mutation_runs": tests, "all_18_mutation_executions_rejected": True, "frozen_unchanged": True, "scope": "Condition durability only; no added theorem claims"})
    print(json.dumps({"hardened": len(copies), "asserts_replaced": sum(x["replaced_assert_count"] for x in records), "mutation_executions_rejected": len(tests)}))

if __name__=="__main__":
    main()
