"""Authenticate the exact PR789 source and reproduce diagnostics; not a formal proof checker."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,os,stat,subprocess,sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).absolute().parent
HEAD="aa44dec3baf8c1cd179cf8b55f32be95c74ee81a"
TITLE="A projective-line quotient of the Rogalski–Sierra algebra"
PINS={
"math_source_geometry":("efe8eb3f489b2c5bb8a586c374195f9aafe62d33df92931b0ea0619bf0a17a9c","d5cc1bf00c6271e7fbf14b3df3e4d3ba79629aa745a2ec500234da07f89d8b59"),
"math_quotient_algebra":("7cd556c6a87d2117f803112268e4b8eb86316c76dac40c9fee82ffe0ccf6eea0","31246b25e6040d2d676f0fd5d1b6c4c65cedc0a67440da313a3ff0a584689333"),
"priority_direct_history":("8cbc07becc1d551a0d1abd298bf1bc7112092626a3ece8324ee58d98b86c42e7","c47727f6a498b5784e31a9a31ae24a50e3c946e5c8d0752606c34dfb3c8d643b"),
"priority_structural":("8999e2b03e1d0271bc2e4e28fa053c127588c3de31d0a91bfccf4f6a1ce88f31","78aa687589626f412a58431a2fc4aa9a5f1134d303b10a4427344835e0433ed3")}
def need(ok,msg):
 if not ok:raise ValueError(msg)
def digest(raw):return hashlib.sha256(raw).hexdigest()
def regular(path):
 need(stat.S_ISREG(path.lstat().st_mode),"Nonregular input")
 fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
 with os.fdopen(fd,"rb")as f:
  need(stat.S_ISREG(os.fstat(f.fileno()).st_mode),"Nonregular opened descriptor")
  return f.read()
def verify(pin,pdf,replay,bodies):
 raw=regular(ROOT/"MANIFEST.json");need(digest(raw)==pin,"External source manifest pin differs")
 preliminary=json.loads(raw);rows=[r for r in preliminary["files"]if r["path"]=="build_package.py"]
 need(len(rows)==1,"Missing/repeated builder binding")
 helper=regular(ROOT/"build_package.py")
 need(len(helper)==rows[0]["bytes"]and digest(helper)==rows[0]["sha256"],"Builder binding differs")
 spec=importlib.util.spec_from_file_location("pr789_pinned_builder",ROOT/"build_package.py");b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
 files=b.closed_source(ROOT,pin);js=b.parse
 source=js(files["audit/intake/ROOT_SOURCE_IDENTITY.json"])
 need(source["reviewed_head"]==HEAD and len(source["original_files"])==58,"Original identity")
 originals=set()
 for row in source["original_files"]:
  name="audit/intake/original/"+row["path"];need(name not in originals,"Duplicate original");originals.add(name);data=files[name]
  need(b.identity(data)=={k:row[k]for k in("bytes","sha256")},"Original bytes")
  need(hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()==row["git_blob"],"Original Git blob")
 need({n for n in files if n.startswith("audit/intake/original/")}==originals,"Original58closure")
 selected=js(files["audit/intake/SELECTED_PUBLIC_RECORD.json"])
 need(digest(selected["problem"]["statement"].encode())==source["statement_sha256"]=="628ed4ce70b7b62857ead560403291f24b890137a8073ce34a17c50d857aa3a6","Statement")
 need(digest(json.dumps([selected["problem"],selected["prior_research"]],sort_keys=True).encode())==source["review_hash"]=="cf0071b62b0e096c74205deac1c8f7cad50cbbf50b4f37d8400170a2d742848f","Complete selected record/prior pair")
 for family,(mf,cp)in PINS.items():
  prefix="audit/"+family+"/";m=files[prefix+"MANIFEST.json"];need(digest(m)==mf,"Independent manifest")
  entries=js(m)["files"];names=set()
  for row in entries:
   n=b.safe_name(row["path"]);need(n not in names,"Repeated independent file");names.add(n)
   need(b.identity(files[prefix+n])=={k:row[k]for k in("bytes","sha256")},"Independent bytes")
  need({n[len(prefix):]for n in files if n.startswith(prefix)}==names|{"MANIFEST.json"},"Closed independent packet")
  checker="verify_packet.py"if family.startswith("math_")else"verify_priority.py"
  need(digest(files[prefix+checker])==cp,"Independent checker")
 g=js(files["audit/root-receipts/PRIORITY_GATE.json"])
 need(g["result"]=="PASS_WITH_PRIORITY_UNRESOLVED"and g["priority_status"]=="PRIORITY_UNRESOLVED"and g["known_full_predecessors"]==[]and g["remaining_mathematical_issues"]==[]and g["blocking_statement_or_credit_issues"]==[],"Priority gate")
 need(all(g["mandatory_context"].values())and not g["historical_first_priority_certified"]and not g["novelty_certified"]and not g["current_worldwide_open_status_certified"],"Bounded scope")
 bind=js(files["PREPRINT_BINDINGS.json"]);need(b.identity(files["main.tex"])==bind["main.tex"],"TeX binding")
 if pdf:need(b.identity(regular(pdf))==bind["paper.pdf"],"PDF binding")
 md=js(files["zenodo-metadata.json"])["metadata"];need(md["title"]==TITLE and md["version"]=="1.0"and md["publication_type"]=="preprint","Release metadata")
 for name,text in[("paper",files["main.tex"].decode()),("description",md["description"]),("README",files["README.md"].decode())]:
  need(all(s in text.lower()for s in("nevins","sierra","characteristic","unresolved","unrefereed")),"Required scope context: "+name)
 executions=[];primary_count=0
 if bodies:need(bodies.is_dir()and not bodies.is_symlink(),"External evidence root")
 if replay or bodies:
  intake=str(ROOT/"audit/intake")
  geo=ROOT/"audit/math_source_geometry";alg=ROOT/"audit/math_quotient_algebra";di=ROOT/"audit/priority_direct_history";st=ROOT/"audit/priority_structural"
  def args(family):
   mf,cp=PINS[family]
   if family=="math_source_geometry":return["--packet-root",str(geo),"--input-root",intake,"--expected-manifest-sha256",mf,"--expected-checker-sha256",cp]+(["--replay"]if replay else[])+(["--source-root",str(bodies/"math_source_geometry/scratch")]if bodies else[])
   if family=="math_quotient_algebra":return["--packet",str(alg),"--intake-root",intake,"--expected-manifest-sha256",mf,"--expected-checker-sha256",cp]+(["--replay"]if replay else[])+(["--primary-root",str(bodies/"math_quotient_algebra_scratch")]if bodies else[])
   if family=="priority_direct_history":return["--packet-root",str(di),"--intake-root",intake,"--expected-manifest-sha256",mf,"--expected-checker-sha256",cp]+(["--primary-root",str(bodies/"scratch_priority_direct_history")]if bodies else[])
   return["--packet-root",str(st),"--input-root",intake,"--manifest-sha256",mf,"--checker-sha256",cp]+(["--primary-root",str(bodies/"scratch_priority_structural")]if bodies else[])
  jobs=[]
  if replay:jobs.append(("audit/intake/original/unsolved_math_prioritization/attempts/30001478/verify_publication.py",["--expected-manifest","f1aab7f750c4c2aba55ba52addbfdd211de3b47edb6fa898387b2720b713e58d"]))
  for family in PINS:jobs.append(("audit/"+family+("/verify_packet.py"if family.startswith("math_")else"/verify_priority.py"),args(family)))
  for opt in([False,True]if replay else[False]):
   for script,arguments in jobs:
    cmd=[sys.executable,"-I","-B"]+(["-O"]if opt else[])+[str(ROOT/script)]+arguments
    p=subprocess.run(cmd,cwd="/",capture_output=True,text=True,timeout=300);need(p.returncode==0 and not p.stderr,"Replay rejected: "+script+"\n"+p.stdout+p.stderr)
    got=js(p.stdout);need(got.get("result",got.get("status"))=="PASS","Replay status")
    count=got.get("primary_files_checked",got.get("primary_files_rehashed",got.get("external_inputs_rehashed",got.get("primary_files_verified",0))))
    if not opt:primary_count+=count
    executions.append({"script":script,"optimized":opt,"status":"PASS","stdout_sha256":digest(p.stdout.encode()),"external_evidence_files_rehashed":count})
 need(b.inventory(ROOT)==files,"Source changed")
 return{"result":"PASS","source_manifest_sha256":pin,"source_files":len(files),"original_files":58,"exact_head":HEAD,"pdf_binding_checked":bool(pdf),"external_evidence_files_rehashed":primary_count,"finite_replay_processes":executions,"priority":"UNRESOLVED","scope":"Byte custody, complete original inventory and finite diagnostics; no proof assistant, exhaustive literature or firstness certification. Current selected record verified; historical full-dataset receipts remain historical. Optional body counts are distinct from reading scope."}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("--expected-manifest-sha256",required=True);p.add_argument("--pdf",type=Path);p.add_argument("--replay",action="store_true");p.add_argument("--bodies-root",type=Path);a=p.parse_args()
 try:r=verify(a.expected_manifest_sha256,a.pdf,a.replay,a.bodies_root)
 except Exception as e:print(json.dumps({"result":"FAIL","error":str(e)}));return 1
 print(json.dumps(r,indent=2,sort_keys=True));return 0
if __name__=="__main__":sys.exit(main())
