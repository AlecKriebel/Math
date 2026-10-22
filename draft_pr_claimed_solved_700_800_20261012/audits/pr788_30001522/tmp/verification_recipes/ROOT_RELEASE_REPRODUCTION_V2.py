from pathlib import Path
import datetime,hashlib,importlib.util,json,os,shutil,subprocess,sys,tempfile
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr788_30001522/tmp");P=T/"preprint";S=P/"source";M=T/"root-receipts";W=T/"root_release_reproduction_v2";W.mkdir(exist_ok=True)
env=dict(os.environ,TMPDIR=str(W));pin=hashlib.sha256((S/"MANIFEST.json").read_bytes()).hexdigest();release=json.loads((P/"PACKAGE_INVENTORY.json").read_text());rows=[];py312="/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"
for py in [sys.executable,py312]:
 for optimized in [False,True]:
  key=("314"if py==sys.executable else"312")+("_O"if optimized else"_normal")
  flags=[py,"-I","-B"]+(["-O"]if optimized else[])
  replay=py==py312 and not optimized
  args=["--expected-manifest-sha256",pin,"--pdf",str(P/"output/pdf/paper.pdf")]
  if replay:args+=["--replay"]
  r=subprocess.run(flags+[str(S/"verify_source.py")]+args,cwd="/",env=env,capture_output=True,text=True,timeout=300)
  if r.returncode or r.stderr:raise RuntimeError(r.stdout+r.stderr)
  got=json.loads(r.stdout);assert got["result"]=="PASS"and got["external_evidence_files_rehashed"]==0
  (M/("ROOT_PORTABLE_V2_"+key+".json")).write_text(r.stdout)
  out=W/key
  r=subprocess.run(flags+[str(S/"build_package.py"),"--expected-manifest-sha256",pin,"--pdf",str(P/"output/pdf/paper.pdf"),"--output-dir",str(out)],cwd="/",env=env,capture_output=True,text=True,timeout=120)
  if r.returncode or r.stderr:raise RuntimeError(r.stdout+r.stderr)
  new=json.loads(r.stdout)
  assert new==release
  for entry in release["files"]:
   raw=(out/entry["path"]).read_bytes();assert raw==(P/entry["path"]).read_bytes()
  rows.append({"key":key,"source_core":"PASS","finite_replay_processes":len(got["finite_replay_processes"]),"external_bodies_rehashed":0,"six_outputs_byte_identical":True})
spec=importlib.util.spec_from_file_location("pinned788verifier",S/"verify_source.py");v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
spec=importlib.util.spec_from_file_location("pinned788builder",S/"build_package.py");b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
controls=[]
def reject(label,call):
 try:call()
 except Exception as e:controls.append({"case":label,"rejected":True,"error":str(e)[:180]});return
 raise RuntimeError("Adversarial control accepted: "+label)
reject("wrong_external_pin",lambda:v.verify("0"*64,P/"output/pdf/paper.pdf",False,None))
with tempfile.TemporaryDirectory(dir=W,prefix="own-controls-")as td:
 d=Path(td);badpdf=d/"bad.pdf";badpdf.write_bytes((P/"output/pdf/paper.pdf").read_bytes()+b"X")
 reject("released_PDF_byte_damage",lambda:v.verify(pin,badpdf,False,None))
 for kind in ["changed_prose","extra_file","extra_empty_directory","missing_original","source_symlink","source_FIFO","changed_builder","changed_manifest"]:
  c=d/"case";shutil.copytree(S,c);oldroot=v.ROOT;v.ROOT=c
  try:
   target=c/"README.md"
   if kind=="changed_prose":target.write_bytes(target.read_bytes()+b"X")
   elif kind=="extra_file":(c/"UNEXPECTED").write_bytes(b"X")
   elif kind=="extra_empty_directory":(c/"UNEXPECTED").mkdir()
   elif kind=="missing_original":next((c/"audit/intake/original").rglob("PROOF.md")).unlink()
   elif kind=="source_symlink":target.unlink();target.symlink_to(S/"README.md")
   elif kind=="source_FIFO":target.unlink();os.mkfifo(target)
   elif kind=="changed_builder":(c/"build_package.py").write_text("raise RuntimeError('must not execute')\n")
   elif kind=="changed_manifest":(c/"MANIFEST.json").write_bytes((c/"MANIFEST.json").read_bytes()+b"\n")
   reject(kind,lambda:v.verify(pin,P/"output/pdf/paper.pdf",False,None))
  finally:v.ROOT=oldroot;shutil.rmtree(c)
 reject("builder_output_inside_closed_source",lambda:b.build(S,pin,P/"output/pdf/paper.pdf",S/"forbidden-output"))
 target=d/"output";target.mkdir();(target/"paper.tex").symlink_to(S/"paper.tex")
 reject("builder_output_symlink_alias",lambda:b.build(S,pin,P/"output/pdf/paper.pdf",target))
 (target/"paper.tex").unlink();os.link(S/"paper.tex",target/"paper.tex")
 reject("builder_output_hardlink_alias",lambda:b.build(S,pin,P/"output/pdf/paper.pdf",target))
 (target/"paper.tex").unlink()
 needled=d/"parent";needled.symlink_to(target,target_is_directory=True)
 reject("builder_output_ancestor_symlink",lambda:b.build(S,pin,P/"output/pdf/paper.pdf",needled/"nested"))
 reject("duplicate_JSON_keys",lambda:b.parse(b'{"a":1,"a":2}'))
 reject("nonfinite_JSON",lambda:b.parse(b'{"a":NaN}'))
 reject("unsafe_archive_path",lambda:b.archive({"../escape":b"x"}))
assert len(controls)==17
for entry in release["files"]:assert b.identity((P/entry["path"]).read_bytes())=={k:entry[k]for k in["bytes","sha256"]}
out={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PASS","source_manifest_sha256":pin,"cross_interpreter_modes":rows,"negative_controls":controls,"historical_full_optional_custody_files":76,"new_optional_external_custody_files":0,"historical_full_optional_custody_receipt":"FIRST_PORTABLE_VERIFICATION.stdout (dated prior to reset; not replayed now)","source_and_six_unchanged":True,"formal_topology_or_priority_certified":False}
(M/"ROOT_RELEASE_REPRODUCTION_V2.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"result":"PASS","interpreter_modes":4,"six_byte_identical_rebuilds":4,"negative_controls":len(controls),"free_bytes":os.statvfs(T).f_bavail*os.statvfs(T).f_frsize}))
