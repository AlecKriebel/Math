"""Verify the externally pinned PR786 source and optional exact PDF; read only."""
from pathlib import Path
import argparse, hashlib, importlib.util, json, os, stat, subprocess, sys
sys.dont_write_bytecode = True
ROOT = Path(__file__).absolute().parent
HEAD = "34f21454986a28ca49f24999be3a0fd1b42755f8"
ORIGINAL = "audit/intake/original/unsolved_math_prioritization/attempts/30001223"
PINS = {
 "math_schur": ("MANIFEST.json","3be42c9f1c125bc9e6243f5c6415a17114aba9a4b4719996cddad0190b329fac"),
 "math_explicit": ("MANIFEST.json","65f6604df29baa56501968ead8e8e9c990dd2b1083d56ded5a34baadb8b11f32"),
 "priority_literature": ("FROZEN_MANIFEST.json","f1e1264de4b52c0dbef57776fb07d1168f92df712263c34e73a3af7faec27904"),
 "priority_example": ("MANIFEST.json","91c1a38807de28a58f07e65fae04ebf0fc17529d232896ef6aad8163a0431689")}
def regular(path):
    if not stat.S_ISREG(path.lstat().st_mode):
        raise ValueError("Nonregular input: "+str(path))
    fd=os.open(path,os.O_RDONLY|os.O_NONBLOCK|os.O_NOFOLLOW)
    with os.fdopen(fd,"rb") as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise ValueError("Nonregular opened input")
        return stream.read()
def execute(script, arguments, optimized):
    command=[sys.executable,"-I","-B"]+(["-O"] if optimized else [])+[str(ROOT/script)]+arguments
    result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=180)
    need(result.returncode==0,"Replay failed: "+script+"\n"+result.stdout+result.stderr)
    value=parse(result.stdout)
    need(value.get("result",value.get("status"))=="PASS","Replay did not return PASS: "+script)
    return {"script":script,"optimized":optimized,"stdout_sha256":hashlib.sha256(result.stdout.encode()).hexdigest(),
            "stderr_sha256":hashlib.sha256(result.stderr.encode()).hexdigest(),"result":value}
def verify(pin,pdf,replay,with_numpy,priority_bodies):
    raw=regular(ROOT/"MANIFEST.json")
    if hashlib.sha256(raw).hexdigest()!=pin:
        raise ValueError("External source manifest pin mismatch")
    preliminary=json.loads(raw)
    rows=[r for r in preliminary["files"] if r["path"]=="build_package.py"]
    if len(rows)!=1:
        raise ValueError("Missing or repeated builder binding")
    helper=ROOT/"build_package.py"
    body=regular(helper)
    if len(body)!=rows[0]["bytes"] or hashlib.sha256(body).hexdigest()!=rows[0]["sha256"]:
        raise ValueError("Builder binding differs")
    spec=importlib.util.spec_from_file_location("pr786_authenticated_builder",helper)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    global need,parse,identity,inventory
    need,parse,identity,inventory=[getattr(module,k) for k in ("need","parse","identity","inventory")]
    files=module.closed_source(ROOT,pin)
    source=parse(files["audit/intake/ROOT_SOURCE_IDENTITY.json"])
    need(source["reviewed_head"]==HEAD and len(source["original_files"])==41,"Wrong original scope")
    expected=set()
    for row in source["original_files"]:
        name="audit/intake/original/"+row["path"]
        need(name not in expected,"Repeated original");expected.add(name)
        data=files[name]
        need(identity(data)=={k:row[k] for k in ("bytes","sha256")},"Original bytes differ")
        need(hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()==row["git_blob"],"Original Git identity differs")
    need({n for n in files if n.startswith("audit/intake/original/")}==expected,"Original41-file closure")
    selected=parse(files["audit/intake/SELECTED_PUBLIC_RECORD.json"])
    need(hashlib.sha256(json.dumps([selected["problem"],selected["prior_research"]],sort_keys=True).encode()).hexdigest()==source["review_hash"],
         "Complete selected-record binding")
    gate=parse(files["audit/root-receipts/PRIORITY_GATE.json"])
    need(gate["result"]=="PASS_FOR_HISTORICAL_REFUTATION_WITH_PRIORITY_UNRESOLVED"
         and gate["known_full_predecessors"]==[] and gate["remaining_mathematical_issues"]==[]
         and gate["blocking_statement_or_credit_issues"]==[]
         and gate["priority_status"]=="PRIORITY_UNRESOLVED"
         and gate["historical_first_priority_certified"] is False
         and gate["current_worldwide_open_status_certified"] is False,"Accepted scope/priority differs")
    for family,(manifest_name,manifest_pin) in PINS.items():
        prefix="audit/"+family+"/";mraw=files[prefix+manifest_name]
        need(hashlib.sha256(mraw).hexdigest()==manifest_pin,"Externally pinned review differs")
        m=parse(mraw);entries=m["files"]
        if isinstance(entries,list):
            rows={r["path"]:{k:r[k] for k in ("bytes","sha256")}for r in entries}
            need(len(rows)==len(entries),"Repeated review file")
        else:rows=entries
        exceptions={manifest_name}
        if family=="priority_literature":
            exceptions.add("EXTERNAL_PIN.txt")
            need(files[prefix+"EXTERNAL_PIN.txt"]==(manifest_pin+"\n").encode(),"Convenience pin differs")
        actual={n[len(prefix):]for n in files if n.startswith(prefix)}
        need(actual==set(rows)|exceptions and all("/" not in n for n in actual),"Closed flat review differs")
        for n,row in rows.items():need(identity(files[prefix+n])==row,"Review file differs: "+family+"/"+n)
    for family,name,prefix,count in [
        ("math_explicit","INPUTS.json","audit/intake/",44),
        ("priority_literature","INPUT_RECEIPTS.json","audit/",46),
        ("priority_example","INPUTS.json","audit/",47)]:
        bindings=parse(files["audit/"+family+"/"+name])["files"]
        if isinstance(bindings,list):rows={r["path"]:{k:r[k]for k in ("bytes","sha256")}for r in bindings}
        else:rows=bindings
        need(len(rows)==count,"Review input count")
        for n,row in rows.items():need(identity(files[prefix+n])==row,"Review input differs: "+n)
    custody=parse(files["audit/math_schur/SOURCE_CUSTODY.json"])
    need(custody["reviewed_head"]==HEAD and custody["immutable_files_checked"]==41,"Schur source scope")
    need(custody["selected_record_sha256"]==identity(files["audit/intake/SELECTED_PUBLIC_RECORD.json"])["sha256"],
         "Schur selected record")
    for row in custody["files"]:
        data=files["audit/intake/original/"+row["path"]]
        need(hashlib.sha256(data).hexdigest()==row["sha256"],"Schur original binding")
        need(hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()==row["git_blob"],"Schur Git binding")
    binding=parse(files["PREPRINT_BINDINGS.json"])
    need(identity(files["paper.tex"])==binding["paper.tex"],"TeX differs")
    if pdf:need(identity(regular(pdf))==binding["paper.pdf"],"PDF differs")
    checks=[]
    if replay:
        fixed=[
          (ORIGINAL+"/verify_publication.py",["--expected-manifest","aded0d2cad18642dd52b4c160c6cace7b346526a0c05405debcb0db637932922","--integrity-only"]),
          ("audit/math_schur/check_manifest.py",[]),
          ("audit/math_explicit/verify_custody.py",["--input-root",str(ROOT/"audit/intake"),"--expected-manifest-sha256",PINS["math_explicit"][1],"--expected-checker-sha256","9be88a42dea31e2073c93c8cc9a2896a765d425fa766e921b84697f1ccae71b2"]),
          ("audit/priority_literature/verify_custody.py",["--input-root",str(ROOT/"audit"),"--expected-manifest-sha256",PINS["priority_literature"][1]]),
          (ORIGINAL+"/author/verify.py",[]),
          (ORIGINAL+"/first_audit/independent_check.py",[]),
          (ORIGINAL+"/second_review/weight_graph_check.py",[]),
          ("audit/math_explicit/independent_coefficients.py",[]),
          ("audit/math_explicit/independent_polarization.py",[]),
          ("audit/priority_example/comparison_check.py",[])]
        if with_numpy:fixed.append(("audit/math_schur/schur_tensor_check.py",[]))
        if priority_bodies:
            fixed.append(("audit/priority_example/custody_check.py",["--packet",str(ROOT/"audit/priority_example"),
                "--inputs-root",str(ROOT/"audit"),"--bodies-root",str(priority_bodies.absolute()),
                "--expected-manifest-sha",PINS["priority_example"][1],"--expected-checker-sha","7a7a86f8baaeacf2b8379ed8667c6673d903aa92b118378e3aee39d5fb31b759"]))
        for optimized in (False,True):
            for script,arguments in fixed:checks.append(execute(script,arguments,optimized))
    need(inventory(ROOT)==files,"Closed source changed during verification")
    return {"result":"PASS","source_manifest_sha256":pin,"source_files":len(files),"original_files":41,
        "exact_head":HEAD,"pdf_binding_checked":bool(pdf),"replay_runs":checks,
        "numpy_tensor_replayed":bool(replay and with_numpy),
        "external_primary_bodies_rechecked":bool(replay and priority_bodies),
        "scope":"Exact custody and finite controls; not a formal proof or exhaustive priority/absence certificate."}
def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument("--expected-manifest-sha256",required=True);a.add_argument("--pdf",type=Path)
    a.add_argument("--replay",action="store_true");a.add_argument("--with-numpy",action="store_true")
    a.add_argument("--priority-bodies",type=Path);x=a.parse_args()
    try:
        if (x.with_numpy or x.priority_bodies) and not x.replay:raise ValueError("Optional computations require --replay")
        value=verify(x.expected_manifest_sha256,x.pdf,x.replay,x.with_numpy,x.priority_bodies)
    except Exception as e:
        print(json.dumps({"result":"FAIL","error":str(e)}));return 1
    print(json.dumps(value,indent=2,sort_keys=True));return 0
if __name__=="__main__":sys.exit(main())
