#!/usr/bin/env python3
"""Create a separate explicit-check copy and record requested repair controls."""
import ast
import difflib
import json
from pathlib import Path
from replay import HERE, SOURCE, check_manifests, run, sha, utc

def require(condition, label):
    if not condition:
        raise RuntimeError(label)

def main():
    before=check_manifests()
    source_path=SOURCE/"check_exact.py"
    original=source_path.read_text()
    assertion_lines=[]
    transformed=[]
    for n,line in enumerate(original.splitlines(),start=1):
        stripped=line.lstrip()
        if stripped.startswith("assert "):
            indent=line[:len(line)-len(stripped)]
            transformed.append(indent+"check("+stripped[len("assert "):] +
                               ", 'original assertion at line "+str(n)+"')")
            assertion_lines.append(n)
        else:
            transformed.append(line)
    repaired="\n".join(transformed)+"\n"
    old="MAX_N = 4  # A_n = {0,...,n}, distinguished point 0\n"
    require(repaired.count(old)==1,"check helper insertion ambiguous")
    new=old+"\n\ndef check(condition, description):\n    if not condition:\n        raise AssertionError(description)\n"
    repaired=repaired.replace(old,new)
    require(len(assertion_lines)==sum(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(original))),
            "not all assertions transformed")
    require(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(repaired))),
            "assertions remain in repaired program")
    folder=HERE/"hardened"
    folder.mkdir(parents=True,exist_ok=True)
    program=folder/"check_exact.py"
    program.write_text(repaired)
    patch="".join(difflib.unified_diff(original.splitlines(keepends=True),repaired.splitlines(keepends=True),
                                    fromfile="a/check_exact.py",tofile="b/check_exact.py"))
    (HERE/"hardened_check_exact.patch").write_text(patch)
    runs=[]
    for optimized in [False,True]:
        result=run("hardened"+("_optimized" if optimized else "_normal"),program,optimized)
        result_file=folder/"exact_results.json"
        result["output_sha256"]=sha(result_file)
        result["source_output_byte_equal"]=result_file.read_bytes()==(SOURCE/"exact_results.json").read_bytes()
        require(result["returncode"]==0 and result["source_output_byte_equal"],"hardened replay mismatch")
        runs.append(result)
    mutations={
        "forcing_discrete_categories":("    arrows = category(injective)",
                                         "    arrows = {n: [(n,tuple(range(n+1)))] for n in range(MAX_N+1)}"),
        "equality_forged_closure":("        relation = {(a, b): root(a) == root(b) for a in range(terms) for b in range(terms)}",
                                    "        relation = {(a, b): True for a in range(terms) for b in range(terms)}")
    }
    failure_runs=[]
    for label,(old,new) in mutations.items():
        require(repaired.count(old)==1,"mutation target ambiguous: "+label)
        directory=folder/"mutations"/label
        directory.mkdir(parents=True,exist_ok=True)
        mutant=directory/"check_exact.py"
        mutant.write_text(repaired.replace(old,new))
        for optimized in [False,True]:
            result=run("hardened_"+label+("_optimized" if optimized else "_normal"),mutant,optimized)
            stderr=(HERE/result["stderr_path"]).read_text()
            require(result["returncode"]!=0 and "AssertionError" in stderr,"hardened mutation not rejected")
            result["failed_check"]=stderr.strip().splitlines()[-1]
            result["mutation_rejected"]=True
            failure_runs.append(result)
    receipt={"finished_utc":utc(),"scope":"separate requested publication-checker repair",
             "completion_estimate_percent":100,"original_source_sha256":sha(source_path),
             "hardened_program_path":str(program.relative_to(HERE)),
             "hardened_program_sha256":sha(program),"patch_sha256":sha(HERE/"hardened_check_exact.patch"),
             "replaced_assertion_original_lines":assertion_lines,
             "all_assertions_replaced":True,"computation_order_preserved":True,
             "honest_runs":runs,"mutation_runs":failure_runs,
             "honest_outputs_byte_equal_in_both_modes":True,"four_actual_failure_controls_rejected":True,
             "source_manifest_checks_before":len(before),"source_manifest_checks_after":len(check_manifests()),
             "frozen_source_preserved":check_manifests()==before,
             "limits":["Finite sanity checks only, not an unbounded proof or priority audit."]}
    (HERE/"hardening_receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps({"finished_utc":receipt["finished_utc"],
                      "assertions_replaced":len(assertion_lines),
                      "honest_outputs_byte_equal_in_both_modes":True,
                      "actual_failure_controls_rejected":4,"frozen_source_preserved":True},indent=2))

if __name__=="__main__":main()
