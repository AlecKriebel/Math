#!/usr/bin/env python3
"""Supplement line tracing with exact test-entry opcode counts and norm fault."""
import ast
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("own_replay", HERE / "audit_repair.py")
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

def wrapper(folder, script, mapping):
    target = str(folder / script)
    out = folder / "opcode_wrapper.py"
    out.write_text(
        "import collections,dis,json,runpy,sys\n"
        f"target={target!r}\nline_map={mapping!r}\ncounts=collections.Counter()\ncache={{}}\n"
        "def trace(frame,event,arg):\n"
        " if frame.f_code.co_filename != target: return None\n"
        " if frame.f_code.co_name in ('<genexpr>','<listcomp>','<setcomp>','<dictcomp>'): return None\n"
        " if frame.f_code not in cache:\n"
        "  offsets={}\n"
        "  seen=set()\n"
        "  for ins in dis.get_instructions(frame.f_code):\n"
        "   if ins.starts_line in line_map and ins.starts_line not in seen:\n"
        "    offsets[ins.offset]=line_map[ins.starts_line]\n"
        "    seen.add(ins.starts_line)\n"
        "  cache[frame.f_code]=offsets\n"
        " if not cache[frame.f_code]: return None\n"
        " frame.f_trace_opcodes=True\n"
        " frame.f_trace_lines=False\n"
        " if event=='opcode' and frame.f_lasti in cache[frame.f_code]: counts[cache[frame.f_code][frame.f_lasti]]+=1\n"
        " return trace\n"
        "sys.settrace(trace)\n"
        "try: runpy.run_path(target,run_name='__main__')\n"
        "finally:\n"
        " sys.settrace(None)\n"
        f" open({str(folder/'check_counts.json')!r},'w').write(json.dumps(dict(sorted(counts.items()))))\n")
    return out

def main():
    static=json.loads((HERE/"STATIC_AND_PROVENANCE.json").read_text())
    rows=[]; controls=[]
    for family,(script,output) in audit.SCRIPTS.items():
        checked=next(r for r in static["scripts"] if r["path"]==script)
        for repaired,optimized in ((False,False),(True,False),(True,True)):
            name=f"opcode_{family}_{'repaired' if repaired else 'source'}_{'optimized' if optimized else 'normal'}"
            folder=audit.fixture(name,repaired)
            if repaired:
                mapping={r["repaired_line"]:r["source_line"] for r in checked["checks"]}
            else:
                old=ast.parse((folder/script).read_bytes())
                normalized=ast.unparse(old)+"\n"
                tree=ast.parse(normalized)
                if ast.dump(tree,include_attributes=False)!=ast.dump(old,include_attributes=False):
                    raise RuntimeError("Normalization changed mathematical code")
                (folder/script).write_text(normalized)
                assertions=sorted((n for n in ast.walk(tree) if isinstance(n,ast.Assert)),key=lambda n:n.lineno)
                mapping={n.lineno:r["source_line"] for n,r in zip(assertions,checked["checks"])}
            entry=wrapper(folder,script,mapping)
            rows.append(audit.execute(name,folder,entry,optimized,output))
    coverage=[]
    for family,(script,_) in audit.SCRIPTS.items():
        group=[r for r in rows if r["name"].startswith(f"opcode_{family}_")]
        counts=[r["check_visit_counts"] for r in group]
        coverage.append({"path":script,"exact_condition_evaluations":sum(counts[0].values()),
                         "same_source_normal_and_repaired_normal_O_counts":all(c==counts[0] for c in counts),
                         "all_assert_sites_visited":len(counts[0])==next(r["source_assert_count"] for r in static["scripts"] if r["path"]==script),
                         "counts_by_source_line":counts[0]})
    for repaired in (False,True):
        for optimized in (False,True):
            name=f"character_scale_fault_{'repaired' if repaired else 'source'}_{'optimized' if optimized else 'normal'}"
            folder=audit.fixture(name,repaired)
            script=folder/"verify_counterexample.py"
            tree=ast.parse(script.read_bytes())
            assignments=[n for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='values' for t in n.targets)]
            if len(assignments)!=1 or not isinstance(assignments[0].value,ast.DictComp):
                raise RuntimeError("Cannot uniquely identify computed character")
            comp=assignments[0].value
            comp.value=ast.BinOp(left=ast.Constant(2),op=ast.Mult(),right=comp.value)
            ast.fix_missing_locations(tree)
            script.write_text(ast.unparse(tree)+"\n")
            row=audit.execute(name,folder,script,optimized)
            row.update(mutation="values[q] becomes 2*chi(q); exact integer character remains integer but norm is multiplied by four",
                       mutated_script_sha256=audit.sha(script.read_bytes()))
            raw=audit.CASE/row["raw_record"]
            last=(raw/"stderr.txt").read_text().splitlines()
            row["exact_failure"]=last[-1] if last else ""
            row["repaired_norm_check_rejected"]=row["exit_code"]!=0 and row["exact_failure"]=="AssertionError: Verification failed at frozen source verify_counterexample.py:62"
            if row["exit_code"]==0:
                value=json.loads((folder/"counterexample_results.json").read_text())
                row["false_success"]={"all_assertions_passed":value["all_assertions_passed"],
                                      "wrong_character_norm":value["icosian_character_construction"]["symmetric_cube_norm"]}
            controls.append(row)
    after={"source":audit.files(audit.SOURCE),"repair":audit.files(audit.REPAIRED),
           "reproduction_public_manifest":audit.sha((audit.REPRO/"PUBLIC_FILES.json").read_bytes())}
    result={"finished_utc":audit.stamp(),"opcode_traced_runs":rows,"coverage":coverage,
            "mathematical_norm_controls":controls,
            "sealed_source_and_public_repair_unchanged":after==static["pre_execution_hashes"],
            "line_trace_correction":"The earlier source-line counts include inline comprehension line events. These test-entry opcode counts supersede those counts; baseline and negative-control results are unchanged.",
            "proof_search_turns_added":0}
    audit.write("OPCODE_COVERAGE_AND_NORM_CONTROL.json",result)
    print(json.dumps({"finished":True,"coverage":coverage,"norm_controls":len(controls)}),flush=True)

if __name__=="__main__":
    main()
