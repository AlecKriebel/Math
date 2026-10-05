#!/usr/bin/env python3
"""Reproduce the PR95 exact finite certificate and hostile false-target controls."""
import argparse, ast, datetime, hashlib, json, os, platform, shutil
import subprocess, sys, tempfile, time
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
SCRIPTS=("verify.py","independent_checks.py","root_lattice_check.py")
REQUIRED=("pr95_note.tex","README.md","LICENSE.txt","PR95_PRIORITY_QUALIFICATION.md",
          "verification/VERIFY_README.md","verification/SOURCE_PROVENANCE.json",
          "verification/run_all.py")+tuple("verification/"+s for s in SCRIPTS)

def require(ok,message):
    if not ok: raise RuntimeError(message)
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x): p.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n",encoding="utf-8")

def guard():
    m=ROOT/"PAYLOAD_MANIFEST.json"
    require(m.is_file(),"missing PAYLOAD_MANIFEST.json")
    d=json.loads(m.read_text(encoding="utf-8"))
    require(d.get("schema")=="pr95-support-payload/v1","wrong payload schema")
    entries=d["files"]
    names=[e["file"] for e in entries]
    require(len(set(names))==len(names),"duplicate payload member")
    require(set(REQUIRED).issubset(names),"missing required payload member")
    require("PAYLOAD_MANIFEST.json" not in names,"manifest self-reference")
    for e in entries:
        q=Path(e["file"])
        require(not q.is_absolute() and ".." not in q.parts,"unsafe payload path")
        p=ROOT/q
        require(p.is_file() and not p.is_symlink(),"missing/linked payload: "+str(q))
        require(sha(p)==e["sha256"] and p.stat().st_size==e["bytes"],
                "payload hash mismatch: "+str(q))
    for name in ("run_all.py",)+SCRIPTS:
        tree=ast.parse((ROOT/"verification"/name).read_text(encoding="utf-8"))
        require(not any(isinstance(n,ast.Assert) for n in ast.walk(tree)),
                "removable validation assertion: "+name)
    return {"manifest_sha256":sha(m),"checked_members":len(entries),
            "meaning":"Payload byte identity against this manifest; authenticate archive digest separately."}

def controlled(script,optimized,negative,out,env):
    label=script[:-3]+("_false" if negative else "_positive")+("_O" if optimized else "_normal")
    work=out/label;work.mkdir()
    source=ROOT/"verification"/script
    if negative:
        text=source.read_text(encoding="utf-8")
        old,new={
          "verify.py":("(S[0][0],{0:5,20:-10,30:10})","(S[0][0],{0:6,20:-10,30:10})"),
          "independent_checks.py":("[(1,(3475,1550))","[(1,(3476,1550))"),
          "root_lattice_check.py":("3475 if q%5 in [1,4]","3476 if q%5 in [1,4]")
        }[script]
        require(text.count(old)==1,"false-control anchor missing: "+script)
        source=work/("false_"+script);source.write_text(text.replace(old,new),encoding="utf-8")
        # The author variant identifies ../pr95_note.tex; keep that binding valid.
        if script=="verify.py":
            source=work/"verification"/script;source.parent.mkdir()
            source.write_text(text.replace(old,new),encoding="utf-8")
            shutil.copyfile(ROOT/"pr95_note.tex",work/"pr95_note.tex")
    inputs=[]
    for f in (source,ROOT/"pr95_note.tex",ROOT/"verification"/"SOURCE_PROVENANCE.json",
              ROOT/"verification"/"run_all.py",ROOT/"PAYLOAD_MANIFEST.json"):
        target=work/("input_"+str(len(inputs))+"_"+f.name)
        shutil.copyfile(f,target)
        inputs.append({"name":f.name,"snapshot":target.name,"sha256":sha(f),"bytes":f.stat().st_size})
    argv=[sys.executable,"-E","-B"]+(["-O"] if optimized else [])+[str(source)]
    process={"schema":"pr95-fresh-process/v1","label":label,"recorder_pid":os.getpid(),
             "argv":argv,"cwd":str(work),"started_utc":utc(),"inputs":inputs,
             "environment":{"python_variables_removed":sorted(k for k in os.environ if k.startswith("PYTHON")),
                            "LC_ALL":"C","python":platform.python_version(),
                            "implementation":platform.python_implementation(),
                            "numpy":__import__("numpy").__version__ if script=="verify.py" else None}}
    began=time.monotonic()
    with (work/"stdout.bin").open("wb") as o,(work/"stderr.bin").open("wb") as e:
        child=subprocess.Popen(argv,cwd=work,env=env,stdout=o,stderr=e)
        process["pid"]=child.pid;dump(work/"process.json",process)
        code=child.wait()
    process.update(exit_code=code,ended_utc=utc(),elapsed_seconds=time.monotonic()-began)
    for name in ("stdout.bin","stderr.bin"):
        f=work/name;process[name]={"bytes":f.stat().st_size,"sha256":sha(f)}
    dump(work/"process.json",process)
    if negative:
        require(code!=0,"false arithmetic target was accepted: "+label)
        require(not (work/"verification.json").exists(),"stale false-control success file")
        require((work/"stdout.bin").stat().st_size==0,"false control printed a success receipt")
        require(b"AssertionError" in (work/"stderr.bin").read_bytes()
                or b"RuntimeError" in (work/"stderr.bin").read_bytes(),"false control did not fail through explicit guard")
        summary={"status":"EXPECTED_REJECTION","false_target":"one exact expected coefficient increased by 1"}
    else:
        require(code==0,"positive child failed: "+label)
        require((work/"stderr.bin").stat().st_size==0,"unexpected positive stderr")
        parsed=json.loads((work/"stdout.bin").read_bytes())
        if script=="verify.py":
            full=json.loads((work/"verification.json").read_bytes())
            require(full["all_pass"] is True and full["weight_count"]==126
                    and full["final_polynomial_identities"]==7,"author receipt mismatch")
            require(full["artifact_sha256"]==sha(ROOT/"pr95_note.tex"),"author artifact binding mismatch")
            summary={"status":"PASS","weight_count":126,"weyl_permutation_count":120,
                     "symmetric_entries_computed":8001,"final_polynomial_identities":7,
                     "verification_json_sha256":sha(work/"verification.json")}
        elif script=="independent_checks.py":
            require(parsed["status"]=="PASS" and parsed["exact_assertions"]==2005,"historical checker receipt mismatch")
            require(parsed["normalized_squared_magnitudes"]=={"L(5,1)":[3475,1550],"L(5,2)":[4025,1800]},"historical target mismatch")
            summary={"status":"PASS","explicit_finite_checks":2005,"historical_count_key":"exact_assertions"}
        else:
            require(parsed["exact_checks"]=="all passed" and parsed["quotient_size"]==625,"fresh lattice receipt mismatch")
            require(set(parsed["results"])=={"1","2","3","4","6","7","-1","-2"},"boundary scope mismatch")
            summary={"status":"PASS","quotient_size":625,"q_controls":[1,2,3,4,6,7,-1,-2],
                     "floating_fields":"diagnostics only"}
    return dict(label=label,script=script,optimized=optimized,negative=negative,exit_code=code,
                process_sha256=sha(work/"process.json"),stdout_sha256=sha(work/"stdout.bin"),
                stderr_sha256=sha(work/"stderr.bin"),source_sha256=sha(source),summary=summary)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output-dir",type=Path)
    args=ap.parse_args()
    require(sys.version_info>=(3,9),"Python 3.9+ required")
    identity=guard()
    out=args.output_dir.resolve() if args.output_dir else Path(tempfile.mkdtemp(prefix="pr95-run-"))
    require(not out.is_relative_to(ROOT),"output must be outside supplied package")
    out.mkdir(parents=True,exist_ok=True)
    require(not any(out.iterdir()),"output directory must be absent or empty")
    started=utc()
    env={k:v for k,v in os.environ.items() if not k.startswith("PYTHON")}
    env["LC_ALL"]="C"
    runs=[]
    for negative in (False,True):
        for optimized in (False,True):
            for script in SCRIPTS:
                runs.append(controlled(script,optimized,negative,out,env))
    require(guard()==identity,"payload changed during execution")
    for script in SCRIPTS:
        pair=[r for r in runs if r["script"]==script and not r["negative"]]
        require(pair[0]["stdout_sha256"]==pair[1]["stdout_sha256"],"ordinary/-O output disagreement")
    result={"schema":"pr95-reproduction-summary/v1","status":"PASS_EXACT_SPECIALIZATION",
            "started_utc":started,"ended_utc":utc(),"runtime":{"python":platform.python_version(),
            "numpy":__import__("numpy").__version__},"payload_guard":identity,
            "note_sha256":sha(ROOT/"pr95_note.tex"),"runs":runs,
            "limits":"Imported general RT/modular-category foundations. Floating fields are diagnostics. No priority, novelty, human-review or publication clearance."}
    dump(out/"results.json",result)
    print(json.dumps({"status":result["status"],"results":str(out/"results.json"),
                      "positive_processes":6,"expected_false_rejections":6},sort_keys=True))
if __name__=="__main__": main()
