#!/usr/bin/env python3
"""Independent static/integrity audit and private replay; no search or remote writes."""
import ast
import copy
from datetime import datetime, timezone
import dis
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import types

HERE = Path(__file__).resolve().parent
CASE = HERE.parents[1]
REPO = CASE.parents[2]
SOURCE = CASE / "source_snapshot/unsolved_math_prioritization/attempts/2569"
REPRO = CASE / "reviews/reproduction_adversary"
REPAIRED = REPRO / "repaired_verification"
PRIVATE = CASE / "private_sources/repair_adversary"
HEAD = "c7805ab0804f50c6f4b0d1dda99e433dbb702ae2"
PYTHON = CASE / "private_sources/reproduction_adversary/venv/bin/python"
SCRIPTS = {
    "author": ("verify_counterexample.py", "counterexample_results.json"),
    "controls": ("verify_controls.py", "control_results.json"),
    "contributor": ("contributor_checks/check_character_data.py", "contributor_checks/character_checks.json"),
    "independent": ("independent_audit/independent_audit.py", "independent_audit/independent_results.json"),
}

def stamp():
    return datetime.now(timezone.utc).isoformat()

def sha(data):
    return hashlib.sha256(data).hexdigest()

def files(folder):
    return {str(p.relative_to(folder)): sha(p.read_bytes()) for p in sorted(folder.rglob("*")) if p.is_file()}

def write(name, data):
    (HERE / name).write_text(json.dumps(data, indent=2) + "\n")

class InverseRepair(ast.NodeTransformer):
    """Identify actual diagnostic branches, restore them to source Assert nodes."""
    def __init__(self, relative, source_tree):
        self.relative = relative
        self.original = {n.lineno: n for n in ast.walk(source_tree) if isinstance(n, ast.Assert)}
        self.rows = []

    def visit_If(self, node):
        self.generic_visit(node)
        if len(node.body) != 1 or node.orelse or not isinstance(node.body[0], ast.Raise):
            return node
        raise_node = node.body[0]
        exc = raise_node.exc
        if not isinstance(exc, ast.Call) or not isinstance(exc.func, ast.Name) or exc.func.id != "AssertionError":
            return node
        if exc.keywords or len(exc.args) != 1 or not isinstance(exc.args[0], ast.Constant):
            return node
        message = exc.args[0].value
        prefix = f"Verification failed at frozen source {self.relative}:"
        if not isinstance(message, str) or not message.startswith(prefix):
            return node
        line = int(message[len(prefix):])
        original = self.original[line]
        if not isinstance(node.test, ast.UnaryOp) or not isinstance(node.test.op, ast.Not) or raise_node.cause is not None:
            raise RuntimeError("Malformed explicit failure branch")
        equal = ast.dump(node.test.operand, include_attributes=False) == ast.dump(original.test, include_attributes=False)
        self.rows.append({"source_line": line, "repaired_line": node.lineno,
                          "test_ast_identical": equal, "test": ast.unparse(original.test),
                          "original_message": None if original.msg is None else ast.unparse(original.msg),
                          "repaired_message": message,
                          "diagnostic_only_change": original.msg is None})
        if not equal or original.msg is not None:
            raise RuntimeError("Unexpected predicate/message change")
        return ast.copy_location(ast.Assert(test=node.test.operand, msg=original.msg), node)

def code_shapes(code):
    answer = [(code.co_name, code.co_code.hex(), tuple(dis.get_instructions(code)))]
    for value in code.co_consts:
        if isinstance(value, types.CodeType):
            answer.extend(code_shapes(value))
    return answer

def static_audit():
    before = {"source": files(SOURCE), "repair": files(REPAIRED),
              "reproduction_public_manifest": sha((REPRO / "PUBLIC_FILES.json").read_bytes())}
    receipt = json.loads((CASE / "SOURCE_RECEIPT.json").read_text())
    pins = []
    for row in receipt["files"]:
        relative = row["path"].removeprefix("unsolved_math_prioritization/attempts/2569/")
        raw = (SOURCE / relative).read_bytes()
        git = subprocess.run(["git", "show", f"{HEAD}:{row['path']}"], cwd=REPO, capture_output=True, check=True).stdout
        pins.append({"path": relative, "sha256": sha(raw), "bytes": len(raw),
                     "receipt_matches": len(raw) == row["bytes"] and sha(raw) == row["sha256"],
                     "source_head_git_bytes_identical": raw == git})
    provenance = json.loads((REPAIRED / "REPAIR_PROVENANCE.json").read_text())
    static = []
    for relative, _ in SCRIPTS.values():
        original = (SOURCE / relative).read_bytes()
        repaired = (REPAIRED / relative).read_bytes()
        source_tree = ast.parse(original)
        actual_tree = ast.parse(repaired)
        inverse = InverseRepair(relative, source_tree)
        restored = inverse.visit(copy.deepcopy(actual_tree))
        rows = sorted(inverse.rows, key=lambda r: r["source_line"])
        a0 = code_shapes(compile(repaired, relative, "exec", optimize=0))
        a1 = code_shapes(compile(repaired, relative, "exec", optimize=1))
        proof = next(r for r in provenance["scripts"] if r["path"] == relative)
        static.append({"path": relative, "source_sha256": sha(original), "repaired_sha256": sha(repaired),
                       "provenance_hashes_match": proof["source_sha256"] == sha(original) and proof["repaired_sha256"] == sha(repaired),
                       "all_nonassert_ast_restored_identically": ast.dump(restored, include_attributes=False) == ast.dump(source_tree, include_attributes=False),
                       "mapped_assertions": len(rows),
                       "source_assert_count": sum(isinstance(n, ast.Assert) for n in ast.walk(source_tree)),
                       "repaired_assert_count": sum(isinstance(n, ast.Assert) for n in ast.walk(actual_tree)),
                       "debug_name_count": sum(isinstance(n, ast.Name) and n.id == "__debug__" for n in ast.walk(actual_tree)),
                       "same_recursive_bytecode_under_O": [(n, b) for n, b, _ in a0] == [(n, b) for n, b, _ in a1],
                       "explicit_assertionerror_loads_normal": sum(i.argval == "AssertionError" and i.opname.startswith("LOAD_") for _, _, seq in a0 for i in seq),
                       "explicit_assertionerror_loads_optimized": sum(i.argval == "AssertionError" and i.opname.startswith("LOAD_") for _, _, seq in a1 for i in seq),
                       "checks": rows})
    public = json.loads((REPRO / "PUBLIC_FILES.json").read_text())
    public_pins = [{"path": r["path"], "matches": sha((CASE/r["path"]).read_bytes()) == r["sha256"] and len((CASE/r["path"]).read_bytes()) == r["bytes"]} for r in public["files"]]
    result = {"checked_utc": stamp(), "source_head": HEAD, "source_head_matches_receipt": receipt["head_sha"] == HEAD,
              "source_pins": pins, "scripts": static, "reproduction_public_pins": public_pins,
              "pre_execution_hashes": before,
              "provenance_sha256": sha((REPAIRED/"REPAIR_PROVENANCE.json").read_bytes()),
              "bare_assert_messages_added": sum(len(r["checks"]) for r in static)}
    write("STATIC_AND_PROVENANCE.json", result)
    return result

def fixture(name, repaired):
    folder = PRIVATE / "fixtures" / name
    if folder.exists():
        raise RuntimeError("Never overwrite an audit fixture")
    shutil.copytree(SOURCE, folder)
    if repaired:
        for relative, _ in SCRIPTS.values():
            (folder / relative).write_bytes((REPAIRED / relative).read_bytes())
    # Fresh execution cannot pass using inherited historical output files.
    for _, output in SCRIPTS.values():
        (folder / output).unlink()
    return folder

def trace_wrapper(folder, script, mapping):
    target = str(folder / script)
    code = ("import collections,json,runpy,sys\n"
            f"target={target!r}\nline_map={mapping!r}\ncounts=collections.Counter()\n"
            "def trace(frame,event,arg):\n"
            " if frame.f_code.co_filename != target: return None\n"
            " if frame.f_code.co_name in ('<genexpr>','<listcomp>','<setcomp>','<dictcomp>'): return None\n"
            " if event == 'line' and frame.f_lineno in line_map: counts[line_map[frame.f_lineno]] += 1\n"
            " return trace\n"
            "sys.settrace(trace)\n"
            "try: runpy.run_path(target,run_name='__main__')\n"
            "finally:\n"
            " sys.settrace(None)\n"
            f" open({str(folder/'check_counts.json')!r},'w').write(json.dumps(dict(sorted(counts.items()))))\n")
    out = folder / "trace_wrapper.py"
    out.write_text(code)
    return out

def execute(name, folder, entry, optimized, output=None):
    command = [str(PYTHON), "-B", *(["-O"] if optimized else []), str(entry)]
    env = os.environ.copy()
    env.pop("PYTHONOPTIMIZE", None)
    env.pop("PYTHONPATH", None)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    before = files(folder)
    start = stamp(); start_perf = time.perf_counter()
    proc = subprocess.run(command, cwd=folder, env=env, capture_output=True, timeout=180)
    duration = time.perf_counter() - start_perf
    raw = PRIVATE / "raw" / name
    raw.mkdir(parents=True, exist_ok=False)
    (raw / "stdout.txt").write_bytes(proc.stdout)
    (raw / "stderr.txt").write_bytes(proc.stderr)
    after = files(folder)
    row = {"name": name, "command": command, "cwd": str(folder), "started_utc": start,
           "finished_utc": stamp(), "duration_seconds": duration, "exit_code": proc.returncode,
           "stdout_sha256": sha(proc.stdout), "stderr_sha256": sha(proc.stderr),
           "stdout_bytes": len(proc.stdout), "stderr_bytes": len(proc.stderr),
           "optimized": optimized, "raw_record": str(raw.relative_to(CASE)),
           "modified_existing_inputs": [p for p,h in before.items() if after.get(p) != h],
           "new_files": [p for p in after if p not in before]}
    if output:
        created = (folder/output).is_file()
        row["fresh_expected_output_created"] = created
        if created:
            generated = (folder/output).read_bytes()
            (raw/"generated.json").write_bytes(generated)
            historical = (SOURCE/output).read_bytes()
            row.update(output_sha256=sha(generated), output_byte_equals_historical=generated == historical,
                       output_fields_equal_historical=json.loads(generated)==json.loads(historical),
                       stdout_equals_fresh_output=proc.stdout == generated)
    if (folder/"check_counts.json").is_file():
        row["check_visit_counts"] = json.loads((folder/"check_counts.json").read_text())
    (raw/"execution.json").write_text(json.dumps(row,indent=2)+"\n")
    print(json.dumps({k: row[k] for k in ("name","exit_code","duration_seconds")}),flush=True)
    return row

def mutate_symcube(folder):
    script = folder / "verify_counterexample.py"
    tree = ast.parse(script.read_bytes())
    changes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "S" and len(node.args) == 2:
            if isinstance(node.args[0], ast.Name) and node.args[0].id == "x" and isinstance(node.args[1], ast.Constant) and node.args[1].value == 2:
                node.args[1].value = 3
                changes.append(node.lineno)
    if len(changes) != 1:
        raise RuntimeError("Mathematical mutation is not unique")
    script.write_text(ast.unparse(tree)+"\n")
    return {"mutation": "symcube polynomial x^3-2x becomes x^3-3x",
            "changed_call_count": len(changes), "mutated_script_sha256": sha(script.read_bytes())}

def main():
    static = static_audit()
    if not static["source_head_matches_receipt"] or not all(r["receipt_matches"] and r["source_head_git_bytes_identical"] for r in static["source_pins"]):
        raise RuntimeError("Source pin validation failed before execution")
    if not all(r["matches"] for r in static["reproduction_public_pins"]):
        raise RuntimeError("Public repair seal does not match")
    if not all(r["provenance_hashes_match"] and r["all_nonassert_ast_restored_identically"] and r["mapped_assertions"]==r["source_assert_count"] and r["repaired_assert_count"]==0 and r["same_recursive_bytecode_under_O"] for r in static["scripts"]):
        raise RuntimeError("Static check equivalence failed before execution")
    env = subprocess.run([str(PYTHON),"-B","-c","import sys,sympy,json; print(json.dumps({'executable':sys.executable,'version':sys.version,'sympy':sympy.__version__}))"],capture_output=True,check=True)
    environment=json.loads(env.stdout)
    baseline=[]; traced=[]; controls=[]
    for family,(script,output) in SCRIPTS.items():
        checked=next(r for r in static["scripts"] if r["path"]==script)
        for repaired in (False,True):
            for optimized in (False,True):
                name=f"{family}_{'repaired' if repaired else 'source'}_{'optimized' if optimized else 'normal'}"
                folder=fixture(name,repaired)
                baseline.append(execute(name,folder,folder/script,optimized,output))
        for repaired,optimized in ((False,False),(True,False),(True,True)):
            name=f"trace_{family}_{'repaired' if repaired else 'source'}_{'optimized' if optimized else 'normal'}"
            folder=fixture(name,repaired)
            if repaired:
                mapping={r["repaired_line"]:r["source_line"] for r in checked["checks"]}
            else:
                # Canonical formatting separates asserts originally sharing a line
                # with a loop/conditional; do not count a loop header as a test.
                old_tree=ast.parse((folder/script).read_bytes())
                normalized=ast.unparse(old_tree)+"\n"
                new_tree=ast.parse(normalized)
                if ast.dump(old_tree,include_attributes=False)!=ast.dump(new_tree,include_attributes=False):
                    raise RuntimeError("Source trace normalization changed semantics")
                (folder/script).write_text(normalized)
                new_asserts=sorted((n for n in ast.walk(new_tree) if isinstance(n,ast.Assert)),key=lambda n:n.lineno)
                mapping={n.lineno:r["source_line"] for n,r in zip(new_asserts,checked["checks"])}
            entry=trace_wrapper(folder,script,mapping)
            traced.append(execute(name,folder,entry,optimized,output))
    for repaired in (False,True):
        for optimized in (False,True):
            name=f"symcube_polynomial_fault_{'repaired' if repaired else 'source'}_{'optimized' if optimized else 'normal'}"
            folder=fixture(name,repaired)
            mutation=mutate_symcube(folder)
            row=execute(name,folder,folder/"verify_counterexample.py",optimized)
            row.update(mutation)
            row["expected_invariant_failure"] = row["exit_code"] != 0 and b"AssertionError" in (PRIVATE/row["raw_record"].removeprefix("private_sources/repair_adversary/")/"stderr.txt").read_bytes()
            if row["exit_code"]==0:
                value=json.loads((folder/"counterexample_results.json").read_text())
                row["false_success"]={"all_assertions_passed":value["all_assertions_passed"],
                                      "wrong_character_norm":value["icosian_character_construction"]["symmetric_cube_norm"],
                                      "wrong_FS_indicator":value["icosian_character_construction"]["symmetric_cube_frobenius_schur_indicator"]}
            controls.append(row)
    coverage=[]
    for family,(script,_) in SCRIPTS.items():
        selected=[r for r in traced if r["name"].startswith(f"trace_{family}_")]
        counts=[r["check_visit_counts"] for r in selected]
        coverage.append({"path":script,"same_source_normal_and_repaired_normal_O_counts":all(c==counts[0] for c in counts),
                         "all_assert_sites_visited": len(counts[0])==next(r["source_assert_count"] for r in static["scripts"] if r["path"]==script),
                         "total_check_visits":sum(counts[0].values()),"counts_by_source_line":counts[0]})
    after={"source":files(SOURCE),"repair":files(REPAIRED),"reproduction_public_manifest":sha((REPRO/"PUBLIC_FILES.json").read_bytes())}
    result={"finished_utc":stamp(),"source_head":HEAD,"environment":environment,
            "baseline_runs":baseline,"traced_runs":traced,"coverage":coverage,"mathematical_negative_controls":controls,
            "sealed_source_and_public_repair_unchanged":after==static["pre_execution_hashes"],
            "post_execution_hashes":after,"proof_search_turns_added":0}
    write("EXECUTION_RESULTS.json",result)
    print(json.dumps({"finished":True,"baselines":len(baseline),"traced":len(traced),"controls":len(controls),"sealed_inputs_unchanged":result["sealed_source_and_public_repair_unchanged"]}),flush=True)

if __name__=="__main__":
    main()
