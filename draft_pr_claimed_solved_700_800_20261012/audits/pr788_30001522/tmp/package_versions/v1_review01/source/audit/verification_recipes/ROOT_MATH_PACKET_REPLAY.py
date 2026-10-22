from pathlib import Path
import sys,hashlib,json,subprocess,os,shutil,tempfile
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr788_30001522/tmp");S=T/"root_packet_replay_scratch";S.mkdir(exist_ok=True);env=dict(os.environ,TMPDIR=str(S))
families=[
("math_definition","53343305e38688a18d5b4b0f133be21ba8d7c00338e55e024b2e27a54059a093","29a450b9b3940871b33b5ec12bbd850b231915c5c99253ba6603c25faf229d26"),
("math_group","1439ea4545ca51f747abd11c4a0754e634143502b0c007e9142a1573edc939dc",None)]
records=[]
def need(c,m):
 if not c:raise RuntimeError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for family,mpin,vpin in families:
 b=T/family;vpin=vpin or sha(b/"VERIFY.py")
 def custody(root):
  need(not root.is_symlink()and root.is_dir(),"Root directory")
  need(sha(root/"MANIFEST.json")==mpin,"External manifest pin")
  need(sha(root/"VERIFY.py")==vpin,"External executable pin")
  m=json.loads((root/"MANIFEST.json").read_text());rows=m["files"]
  rows=rows if isinstance(rows,list)else[dict(path=n,**v)for n,v in rows.items()]
  need(set(p.name for p in root.iterdir())=={r["path"]for r in rows}|{"MANIFEST.json"},"Physical inventory")
  for r in rows:
   p=root/r["path"];need(p.name==r["path"]and p.is_file()and not p.is_symlink()and p.stat().st_size==r["bytes"]and sha(p)==r["sha256"],"Physical file pin")
 def command(py,opt,root):
  custody(root)
  args=["--manifest-sha256",mpin,"--input-root",str(T/"intake")]if family=="math_definition"else["--intake-root",str(T/"intake"),"--input-root",str(T/"intake/original"),"--source-root",str(T/"math_group_scratch")]
  r=subprocess.run([py,"-I","-B",*(["-O"]if opt else[]),str(root/"VERIFY.py"),*args],cwd="/",env=env,capture_output=True,text=True,timeout=120)
  need(r.returncode==0 and not r.stderr,r.stderr);got=json.loads(r.stdout);need(got["status"]=="PASS","Packet verifier status");return got
 familyrec={"family":family,"manifest_sha256":mpin,"checker_sha256":vpin,"modes":[],"physical_negative_controls":[]}
 for py in [sys.executable,"/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"]:
  for opt in [False,True]:familyrec["modes"].append({"python":py,"optimized":opt,"result":command(py,opt,b)})
 with tempfile.TemporaryDirectory(dir=S,prefix=family+"-")as td:
  d=Path(td)
  positive=d/"relocated with spaces";shutil.copytree(b,positive);familyrec["relocation_positive"]=command(sys.executable,False,positive)
  for kind in ["byte_damage","extra_file","extra_directory","missing_file","symlink","changed_manifest","rehashed_prose","tampered_verifier"]:
   p=d/kind;shutil.copytree(b,p);report="REPORT.md"if family=="math_definition"else"REVIEW.md"
   if kind=="byte_damage":(p/report).write_bytes(b"X"+(p/report).read_bytes()[1:])
   elif kind=="extra_file":(p/"EXTRA").write_bytes(b"x")
   elif kind=="extra_directory":(p/"EXTRA").mkdir()
   elif kind=="missing_file":(p/report).unlink()
   elif kind=="symlink":(p/report).unlink();(p/report).symlink_to(b/report)
   elif kind=="changed_manifest":(p/"MANIFEST.json").write_bytes((p/"MANIFEST.json").read_bytes()+b"\n")
   elif kind=="rehashed_prose":
    (p/report).write_bytes((p/report).read_bytes()+b"\nX")
    m=json.loads((p/"MANIFEST.json").read_text());r=next(x for x in m["files"]if x["path"]==report)if isinstance(m["files"],list)else m["files"][report];r.update(bytes=(p/report).stat().st_size,sha256=sha(p/report));(p/"MANIFEST.json").write_text(json.dumps(m))
   elif kind=="tampered_verifier":(p/"VERIFY.py").write_text("print('PASS')\n")
   rejected=False
   try:custody(p)
   except RuntimeError:rejected=True
   need(rejected,"Damaged packet custody accepted");familyrec["physical_negative_controls"].append({"kind":kind,"rejected_before_execution":True})
 records.append(familyrec)
out={"status":"PASS","families":records,"finite_checks_prove_topology":False}
(T/"root-receipts/ROOT_MATH_PACKET_REPLAY.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":"PASS","families":2,"checker_group_sha256":records[1]["checker_sha256"],"full_interpreter_modes_each":4,"relocation_positives_each":1,"physical_negative_controls_each":8}))
