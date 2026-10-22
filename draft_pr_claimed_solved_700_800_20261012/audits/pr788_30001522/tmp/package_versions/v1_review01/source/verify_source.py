"""Authenticate the closed PR788 source and reproduce finite checks; not a proof assistant."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,os,stat,subprocess,sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).absolute().parent
HEAD="3412d5a074c3f3a03f75735a9ccf1755e172204a"
OLD_CASE="/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr788_30001522/tmp/"
ORIGINAL="audit/intake/original/unsolved_math_prioritization/attempts/30001522"
PINS={
"math_definition":"53343305e38688a18d5b4b0f133be21ba8d7c00338e55e024b2e27a54059a093",
"math_group":"1439ea4545ca51f747abd11c4a0754e634143502b0c007e9142a1573edc939dc",
"math_definition_crosscheck":"310d9a87bb320f079b345f3a977612b697a6c07c02ebf51be3a0da821128fb3d",
"math_group_crosscheck":"767aaa58b6951a3a8320213127e5ec17e4b8c6033c814d58f1d4c784aeeeb529",
"priority_classical":"59ee3141dd73732c4494594e561feeda54ce6fa55304a5a41974945b74e7a3a2",
"priority_question":"bb312addd8615d21b2043764f194884232ed08b85a55bda688e5648dc89cc913",
"priority_classical_crosscheck":"59f34e7069f38d90cbc0a336b5069146a44f9fba06d88053701ca0f0f73f0395"}
def require(ok,message):
    if not ok:raise ValueError(message)
def digest(raw):return hashlib.sha256(raw).hexdigest()
def regular(path):
    require(stat.S_ISREG(path.lstat().st_mode),"Nonregular input")
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    with os.fdopen(fd,"rb") as f:
        require(stat.S_ISREG(os.fstat(f.fileno()).st_mode),"Nonregular descriptor")
        return f.read()
def verify(pin,pdf,replay,bodies):
    # Authenticate the builder before importing any source-supplied executable.
    raw=regular(ROOT/"MANIFEST.json")
    require(digest(raw)==pin,"Externally supplied source pin differs")
    preliminary=json.loads(raw)
    rows=[r for r in preliminary["files"] if r["path"]=="build_package.py"]
    require(len(rows)==1,"Builder binding missing/repeated")
    helper=regular(ROOT/"build_package.py")
    require(len(helper)==rows[0]["bytes"] and digest(helper)==rows[0]["sha256"],"Builder bytes differ")
    spec=importlib.util.spec_from_file_location("pr788_pinned_builder",ROOT/"build_package.py")
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    files=module.closed_source(ROOT,pin)
    identity,parse,need=module.identity,module.parse,module.need
    source=parse(files["audit/intake/ROOT_SOURCE_IDENTITY.json"])
    need(source["reviewed_head"]==HEAD and source["original_file_count"]==48,"Original target/count")
    originals=set()
    for row in source["original_files"]:
        name="audit/intake/original/"+row["path"]
        need(name not in originals,"Repeated original");originals.add(name)
        b=files[name];need(identity(b)=={k:row[k]for k in("bytes","sha256")},"Original SHA256/size")
        need(hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()==row["git_blob"],"Original Git identity")
    need({n for n in files if n.startswith("audit/intake/original/")}==originals,"Original48 closure")
    selected=parse(files["audit/intake/SELECTED_PUBLIC_RECORD.json"])
    need(digest(json.dumps([selected["problem"],selected["prior_research"]],sort_keys=True).encode())==source["review_hash"],"Full selected-record/prior binding")
    need(digest(selected["problem"]["statement"].encode())==source["statement_sha256"],"Statement binding")
    gate=parse(files["audit/root-receipts/PRIORITY_GATE.json"])
    need(gate["result"]=="PASS_FOR_CLASSICAL_ANSWER_WITH_PRIORITY_UNRESOLVED"
         and gate["known_full_predecessors"]==[] and gate["remaining_mathematical_issues"]==[]
         and gate["blocking_statement_or_credit_issues"]==[]
         and gate["priority_status"]=="PRIORITY_UNRESOLVED"
         and gate["C1_required"] is True
         and gate["historical_first_priority_certified"] is False
         and gate["current_worldwide_open_status_certified"] is False,"Scope/credit gate")
    for family,mpin in PINS.items():
        prefix="audit/"+family+"/";mraw=files[prefix+"MANIFEST.json"]
        need(digest(mraw)==mpin,"Review manifest pin: "+family)
        entries=parse(mraw)["files"]
        if isinstance(entries,list):
            manifest={r["path"]:{k:r[k]for k in("bytes","sha256")}for r in entries}
            need(len(manifest)==len(entries),"Duplicate review row")
        else:manifest=entries
        actual={n[len(prefix):]for n in files if n.startswith(prefix)}
        need(actual==set(manifest)|{"MANIFEST.json"} and all("/"not in n for n in actual),"Closed flat review: "+family)
        for n,row in manifest.items():need(identity(files[prefix+n])=={k:row[k]for k in("bytes","sha256")},"Review payload: "+family+"/"+n)
    external={};bound_authored=0
    def bind(relative,row):
        nonlocal bound_authored
        if relative.startswith(OLD_CASE):relative=relative[len(OLD_CASE):]
        need(not relative.startswith("/"),"Unexpected absolute input outside original case")
        module.safe_name(relative)
        name="audit/"+relative
        expected={k:row[k]for k in("bytes","sha256")}
        if name in files:
            need(identity(files[name])==expected,"Bound authored input differs: "+relative);bound_authored+=1
        else:
            need(relative not in external or external[relative]==expected,"Conflicting external bindings")
            external[relative]=expected
    b=parse(files["audit/math_definition/INPUT_BINDINGS.json"])
    for row in b["local_inputs"]:bind("intake/"+row["path"],row)
    b=parse(files["audit/math_group/INPUT_BINDINGS.json"])
    for n,row in b["intake_files"].items():bind("intake/"+n,row)
    for row in b["original_files"]:bind("intake/original/"+row["path"],row)
    for family in("priority_classical","priority_question"):
        rows=parse(files["audit/"+family+"/INPUT_BINDINGS.json"])["files"]
        rows=rows if isinstance(rows,list)else[dict(path=n,**r)for n,r in rows.items()]
        need(len(rows)==51,"Priority original input scope")
        for row in rows:bind("intake/"+row["path"],row)
    for family in("math_definition_crosscheck","math_group_crosscheck"):
        for row in parse(files["audit/"+family+"/INPUT_BINDINGS.json"])["inputs"]:bind(row["path"],row)
    for n,row in parse(files["audit/priority_classical_crosscheck/INPUT_BINDINGS.json"])["files"].items():bind(n,row)
    for row in parse(files["audit/math_group/SOURCE_RECEIPTS.json"])["sources"]:
        bind("math_group_scratch/"+row["scratch_basename"],row)
    for n,row in parse(files["audit/priority_classical/SOURCE_LEDGER.json"])["external_scratch_files"].items():
        bind("priority_classical_scratch/"+n,row)
    for row in parse(files["audit/priority_question/SOURCE_LEDGER.json"])["sources"]:
        for kind in("pdf","text"):
            bind("priority_question_scratch/"+row[kind+"_file"],{"bytes":row[kind+"_bytes"],"sha256":row[kind+"_sha256"]})
    row=parse(files["audit/priority_question/VISUAL_RECEIPT.json"])
    bind("priority_question_scratch/"+row["render_file"],{"bytes":row["render_bytes"],"sha256":row["render_sha256"]})
    primary_checked=0
    if bodies:
        bodyroot=bodies.absolute();need(bodyroot.is_dir()and not bodyroot.is_symlink(),"External workspace root")
        for relative,expected in sorted(external.items()):
            p=bodyroot
            for part in Path(relative).parts:p=p/part;need(not p.is_symlink(),"External path symlink")
            need(identity(regular(p))==expected,"External body/evidence differs: "+relative);primary_checked+=1
    binding=parse(files["PREPRINT_BINDINGS.json"])
    need(identity(files["paper.tex"])==binding["paper.tex"],"TeX binding")
    if pdf:need(identity(regular(pdf))==binding["paper.pdf"],"Exact released PDF binding")
    metadata=parse(files["zenodo-metadata.json"])["metadata"]
    need(metadata["title"]=="A classical Wu-manifold answer to a free-rank question"
         and metadata["publication_type"]=="preprint"and metadata["version"]=="1.0","Release identity")
    for content in(files["paper.tex"].decode(),metadata["description"],files["README.md"].decode()):
        need(all(t in content.lower()for t in("odd","cyclic","nonabelian")),"Missing C1 credit context")
    executions=[]
    if replay:
        fixed=[
          (ORIGINAL+"/verify_publication.py",["a30ff869af7e3dc5995a8c77350e5453e05fa515ec78088b4ba20d00b0b2ca16","--full"]),
          ("audit/math_definition/VERIFY.py",["--manifest-sha256",PINS["math_definition"],"--input-root",str(ROOT/"audit/intake")]),
          ("audit/math_group/CHECKS.py",[]),
          ("audit/priority_classical/custody_check.py",["--packet",str(ROOT/"audit/priority_classical"),"--input-root",str(ROOT/"audit/intake"),"--expected-manifest-sha",PINS["priority_classical"],"--expected-checker-sha","81fb18e7d6c59aa95c1d2131d9a5778e9bceb745bba0814f79be3ecbd75c1b46"]),
          ("audit/priority_question/verify_packet.py",["--packet-root",str(ROOT/"audit/priority_question"),"--intake-root",str(ROOT/"audit/intake"),"--manifest-sha256",PINS["priority_question"],"--checker-sha256","c67eb9c3e4bbd518ae0737c5f32db7ed4d974223e84b14429d46e01ddf29b487"])]
        for optimized in(False,True):
            for script,arguments in fixed:
                command=[sys.executable,"-I","-B"]+(["-O"]if optimized else[])+[str(ROOT/script)]+arguments
                result=subprocess.run(command,cwd="/",capture_output=True,text=True,timeout=300)
                need(result.returncode==0 and not result.stderr,"Replay failed: "+script+"\n"+result.stderr)
                value=parse(result.stdout);status=value.get("result",value.get("status"))
                need(status in("PASS","PASS_PUBLICATION_INVENTORY"),"Replay status")
                if script.endswith("math_group/CHECKS.py"):
                    need(value==parse(files["audit/math_group/RESULTS.json"]),"Exact independent math diagnostics")
                executions.append({"script":script,"optimized":optimized,"status":status,"stdout_sha256":digest(result.stdout.encode())})
    need(module.inventory(ROOT)==files,"Closed source changed during verification")
    return {"result":"PASS","source_manifest_sha256":pin,"source_files":len(files),"original_files":48,
       "exact_head":HEAD,"authored_input_bindings_checked":bound_authored,
       "external_evidence_bindings_recorded":len(external),"external_evidence_files_rehashed":primary_checked,
       "primary_body_custody_replayed":bool(bodies),"pdf_binding_checked":bool(pdf),
       "finite_replay_processes":executions,"classical_scope_and_C1":True,
       "scope":"Authenticates exact authored bytes and finite diagnostics; not formal topology, historical priority, or absence certification. Historical path-bound crosscheck executables are preserved; their authored inputs are remapped and bound here without pretending to run their omitted primary bodies."}
def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument("--expected-manifest-sha256",required=True);a.add_argument("--pdf",type=Path)
    a.add_argument("--replay",action="store_true");a.add_argument("--bodies-root",type=Path)
    x=a.parse_args()
    try:out=verify(x.expected_manifest_sha256,x.pdf,x.replay,x.bodies_root)
    except Exception as e:print(json.dumps({"result":"FAIL","error":str(e)}));return 1
    print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=="__main__":sys.exit(main())
