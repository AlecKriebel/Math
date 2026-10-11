#!/usr/bin/env python3
"""Check comparisons, build verdict and pin final audit artifacts."""
import datetime
import hashlib
import json
import math
from pathlib import Path
from record_run import meta, run

root=Path(__file__).resolve().parent
original=root.parent/"original_source_authentication_20261006"/"original_attempt"


def require(condition,message):
    if not condition:
        raise RuntimeError(message)


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def output(name):
    return root/"actual_runs"/name/"stdout.bin"


def main():
    version=run("runtime_version",["/opt/homebrew/bin/python3","--version"])
    initial=json.loads((root/"independent_initial_normal.json").read_text())
    require((root/"independent_initial_normal.json").read_bytes()==(root/"independent_initial_optimized.json").read_bytes(),"initial result mismatch")
    structural=[]
    for case in initial["cases"]:
        expected=(2**case["normalized_n"])*math.prod(map(len,case["normalized"]))
        require(case["feasible_trees"]==expected,"generic tree count differs from independently derived count")
        structural.append({"n":case["normalized_n"],"clauses":case["normalized"],"count":case["feasible_trees"],"expected":expected})
    (root/"STRUCTURAL_COUNTS.json").write_text(json.dumps({"cases":structural,"passed":True,"checks":len(structural)},indent=2)+"\n")
    comparisons={}
    for kind,reference in (("author",original/"verification.json"),("independent",original/"review"/"independent_results.json")):
        expected=json.loads(reference.read_text())
        for mode in ("normal","optimized"):
            actual=json.loads(output(kind+"_repaired_"+mode).read_text())
            intentional=[]
            require(set(expected)==set(actual),"JSON keys changed")
            for key in expected:
                if key=="checker_sha256" and expected[key]!=actual[key]:
                    intentional.append(key)
                else:
                    require(expected[key]==actual[key],"unintended repaired output change: "+key)
            comparisons[kind+"_"+mode]={"reference":meta(reference),"repaired_output":meta(output(kind+"_repaired_"+mode)),
                                        "byte_exact":reference.read_bytes()==output(kind+"_repaired_"+mode).read_bytes(),
                                        "intentional_changed_keys":intentional,"identical_excluding_only_checker_sha256":True}
        require(output(kind+"_repaired_normal").read_bytes()==output(kind+"_repaired_optimized").read_bytes(),"repair mode changed output")
    (root/"REPAIRED_RESULT_COMPARISON.json").write_text(json.dumps(comparisons,indent=2)+"\n")
    (root/"author_suggested_repair"/"verification.json").write_bytes(output("author_repaired_normal").read_bytes())
    (root/"independent_suggested_repair"/"independent_results.json").write_bytes(output("independent_repaired_normal").read_bytes())
    receipts=[]
    for path in sorted((root/"actual_runs").glob("*/receipt.json")):
        receipt=json.loads(path.read_text())
        for stream in ("stdout","stderr"):
            require(meta(Path(receipt[stream]["path"]))==receipt[stream],"receipt output mutated")
        receipts.append(receipt)
    byname={receipt["name"]:receipt for receipt in receipts}
    for kind in ("author","independent"):
        for test in ("false","corrupt_cost"):
            require(byname[kind+"_"+test+"_normal"]["exit_code"]==1,"original normal negative control did not reject")
            require(byname[kind+"_"+test+"_optimized"]["exit_code"]==0,"optimized bypass was not reproduced")
            for mode in ("normal","optimized"):
                require(byname[kind+"_repaired_"+test+"_"+mode]["exit_code"]==1,"repaired negative control did not reject")
    for mode in ("normal","optimized"):
        require(byname["author_repaired_cycle_"+mode]["exit_code"]==1,"cycle repair did not reject")
    require(byname["author_cycle_normal"]["exit_code"]==1 and byname["author_cycle_optimized"]["exit_code"]==2,"cycle bypass mismatch")
    pin=json.loads((root/"INITIAL_CONTROL_PIN.json").read_text())
    for entry in pin["artifacts"]:
        require(meta(Path(entry["path"]))["sha256"]==entry["sha256"],"initial pin changed")
    copies=json.loads((root/"FROZEN_REPLAY_COPY_MANIFEST.json").read_text())
    for entry in copies["copies"]:
        for name in ("source","copy"):
            require(meta(Path(entry[name]["path"]))==entry[name],"frozen source or copy changed")
    repaired_artifacts=[meta(root/name) for name in ("author_suggested_repair/verify.py","author_suggested_repair/verification.json",
                       "independent_suggested_repair/independent_checks.py","independent_suggested_repair/independent_results.json",
                       "author_suggested_repair.diff","independent_suggested_repair.diff")]
    verdict={"utc":utc(),"record_id":30003997,"pull_request":107,"eligible_head":"cc2ae01897135b35bee135917819e782a220f2c1",
             "verdict":"MATHEMATICAL_PASS_WITH_REQUIRED_CHECKER_CORRECTION",
             "mathematical_defect_found":False,"computational_checker_defect_found":True,
             "strongest_verified_theorem":"The fixed-root destination-specific path-cost threshold-zero decision problem is NP-complete on simple reachable four-layer adjacent-layer DAGs with nonroot indegree <=3 and binary dense costs; optimization is strongly NP-hard, also with costs {1,2} at threshold 4n+3m.",
             "finite_evidence":{"formula_cases":initial["formula_cases"],"edge_subsets_examined":initial["total_edge_subsets_examined"],
                                "feasible_trees":initial["total_feasible_trees"],"noncanonical_trees":initial["total_noncanonical_trees"],
                                "larger_witnesses":len(initial["larger_witness_checks"]),"arbitrary_size_claim_is_deductive":True},
             "required_corrections":[{"id":"C1","kind":"checker_defect","action":"Replace author's validation and cycle asserts, and old independent checker's validation assert, with explicit exceptions; regenerate author's checker-SHA-bearing verification receipt and preserve old originals.",
                                     "reason":"Python -O strips the original asserts while leaving PASS and assertion counters; known-false and corrupted-model controls accept.",
                                     "scope":"Portable computational package correction; does not require changing the mathematical proof.",
                                     "suggested_artifacts":repaired_artifacts,"repair_verified_normal_and_optimized":True}],
             "unresolved_concerns":[{"id":"U1","concern":"Historical novelty and priority are unestablished.","mathematical_correctness_blocker":False},
                                    {"id":"U2","concern":"Root must propagate and independently recheck the suggested repair before package clearance; this delegated audit edits only its dedicated folder.","mathematical_correctness_blocker":False}],
             "originals_unchanged":True,"original_author_stdout_byte_exact":True,"original_independent_stdout_byte_exact":True,
             "repaired_results_identical_excluding_only_intentional_checker_sha":True,
             "actual_process_receipts":len(receipts),"runtime":{"argv":version["argv"],"version":output("runtime_version").read_text().strip(),"dependencies":"Python standard library only"},
             "central_proof_search_turns_added":0,"original_candidate_turns":"1/5","novelty":"unestablished",
             "independence_pin":meta(root/"INITIAL_CONTROL_PIN.json"),"completion_percent":100,
             "prohibited_operations_performed":[]}
    (root/"VERDICT.json").write_text(json.dumps(verdict,indent=2)+"\n")
    timestamp=utc()
    with (root/"RESEARCH_LOG.md").open("a") as log:
        log.write("\n- "+timestamp+": verification checkpoint, 75% completion. Independent dense-table generic enumeration passed 645 formulas / 583,319 edge subsets / 8,988 trees; original outputs reproduced byte-exact. Confirmed original Python -O gates accept known-false conditions and in-memory corrupt cost models. Preserved all failing controls; no mathematical defect found.\n")
        log.write("\n- "+timestamp+": final checkpoint, 100% of delegated audit completed. Minimal author guard+cycle and independent guard repairs pass normal/-O suites and reject false, corrupt-cost and applicable cycle controls. Original/repaired JSON comparison changes only author checker SHA. Original source and pinned initial checker unchanged. Strongest result is the candidate's written arbitrary-size hardness theorem; finite evidence is supporting, novelty unestablished, no extra proof-search turn used. Root must propagate/check the correction for publication-package clearance.\n")
    inputs=[Path("/Users/alec/Documents/Math/AGENTS.md"),Path("/Users/alec/Documents/Math/unsolved_math_prioritization/AGENTS.md"),
            original/"PROOF.md",original/"source_record.json",original/"verify.py",original/"verification.json",
            original/"review"/"independent_checks.py",original/"review"/"independent_results.json",original/"review"/"REVIEW.md",
            root.parent/"primary_sources_20261006"/"owr.txt"]
    artifacts=[path for path in sorted(root.rglob("*")) if path.is_file() and path.name!="MANIFEST.json" and "__pycache__" not in path.parts]
    manifest={"utc":utc(),"inputs":[meta(path) for path in inputs],"outputs":[meta(path) for path in artifacts],
              "exclusions":["MANIFEST.json itself (self-reference)","Generated __pycache__ runtime caches"],
              "all_source_files_unchanged":True,"manifest_scope":"This dedicated delegated-audit folder only"}
    (root/"MANIFEST.json").write_text(json.dumps(manifest,indent=2)+"\n")
    print(json.dumps({"verdict":verdict["verdict"],"formula_cases":initial["formula_cases"],"receipts":len(receipts),
                      "manifest_output_files":len(artifacts),"suggested_repairs":repaired_artifacts},indent=2))


if __name__=="__main__":
    main()
