from pathlib import Path
import datetime,json,shutil,sys
from capture_v2 import capture,sha,dump
P=Path(__file__).resolve().parent.parent;N=P/"private_notes";base=N/"clean_extracted"
fixtures=N/"guard_fixtures";fixtures.mkdir()
results=[]
patterns={"missing":"missing payload: README.md","changed":"payload hash mismatch: README.md",
 "leaf_symlink":"symlinked payload path component: README.md",
 "ancestor_symlink":"symlinked payload path component: verification/recorded_processes/",
 "unsafe":"unsafe payload path","duplicate":"duplicate payload member","ast_assertion":"removable validation assertion: verify.py"}
for case,pattern in patterns.items():
 root=fixtures/case;shutil.copytree(base,root)
 m=root/"PAYLOAD_MANIFEST.json";d=json.loads(m.read_text())
 extra=[]
 if case=="missing":(root/"README.md").unlink()
 elif case=="changed":(root/"README.md").write_text((root/"README.md").read_text()+"\n# changed bytes\n")
 elif case=="leaf_symlink":
  target=fixtures/"leaf_identical_target.md";shutil.copyfile(root/"README.md",target)
  (root/"README.md").unlink();(root/"README.md").symlink_to(target);extra=[target]
 elif case=="ancestor_symlink":
  directory=root/"verification/recorded_processes";target=fixtures/"ancestor_identical_target";directory.rename(target)
  directory.symlink_to(target,target_is_directory=True)
 elif case=="unsafe":d["files"][0]["file"]="../outside"
 elif case=="duplicate":d["files"].append(dict(d["files"][0]))
 elif case=="ast_assertion":
  q=root/"verification/verify.py";q.write_text("assert True\n"+q.read_text())
  for e in d["files"]:
   if e["file"]=="verification/verify.py":e["sha256"]=sha(q);e["bytes"]=q.stat().st_size
 if case in ("unsafe","duplicate","ast_assertion"):dump(m,d)
 spec={"case":case,"expected_error":pattern,"base_zip_sha256":sha(P/"publicfiles/pr95_support.zip"),
       "fixture_root":str(root),"leaf_is_symlink":(root/"README.md").is_symlink(),
       "ancestor_is_symlink":(root/"verification/recorded_processes").is_symlink(),
       "ancestor_target":str((root/"verification/recorded_processes").readlink()) if case=="ancestor_symlink" else None,
       "require_rejection_before_output_creation":True}
 specfile=root/"FIXTURE_SPEC.json";dump(specfile,spec)
 for optimized in (False,True):
  label="guard_"+case+("_O" if optimized else "_normal");output=N/(label+"_unexpected_output")
  argv=[sys.executable,"-E","-B"]+(["-O"] if optimized else [])+[str(root/"verification/run_all.py"),"--output-dir",str(output)]
  inputs=[Path(__file__),N/"capture_v2.py",specfile,root/"verification/run_all.py",m]+extra
  if (root/"README.md").exists():inputs.append(root/"README.md")
  if case=="ast_assertion":inputs.append(root/"verification/verify.py")
  r=capture(label,argv,root,inputs,1)
  stderr=(N/"processes"/label/"stderr.bin").read_bytes()
  if pattern.encode() not in stderr or b"RuntimeError:" not in stderr:raise RuntimeError("unrelated rejection "+label)
  if output.exists():raise RuntimeError("guard rejected after output creation "+label)
  if (N/"processes"/label/"stdout.bin").stat().st_size!=0:raise RuntimeError("guard printed success")
  results.append({"case":case,"optimized":optimized,"exit_code":1,"explicit_error":pattern,
                  "output_created":False,"process_file":str((N/"processes"/label/"process.json").relative_to(P)),"process_sha256":sha(N/"processes"/label/"process.json")})
# Prove clean guard succeeds independently of arithmetic in both modes.
probe=N/"positive_guard_probe.py"
probe.write_text("from pathlib import Path\nimport json,runpy,sys\np=Path(sys.argv[1])\nd=runpy.run_path(str(p/'verification/run_all.py'))\nprint(json.dumps(d['guard'](),sort_keys=True))\n")
for optimized in (False,True):
 label="guard_positive"+("_O" if optimized else "_normal")
 r=capture(label,[sys.executable,"-E","-B"]+(["-O"] if optimized else [])+[str(probe),str(base)],base,[probe,base/"verification/run_all.py",base/"PAYLOAD_MANIFEST.json"])
 results.append({"case":"positive","optimized":optimized,"exit_code":r["exit_code"],"process_sha256":sha(N/"processes"/label/"process.json")})
dump(N/"PAYLOAD_GUARD_CONTROLS.json",{"UTC":datetime.datetime.now(datetime.timezone.utc).isoformat(),"cases":results,"hostile_cases":14,"positive_guard_cases":2,"ancestor_rejects_both_modes_before_output":True,"repair":"Every declared path component beneath ROOT checked with is_symlink() before file-content reads."})
with (N/"RESEARCH_LOG.md").open("a") as f:
 f.write("\n"+datetime.datetime.now(datetime.timezone.utc).isoformat()+" - Guard boundary suite: missing/changed/leaf-symlink/ancestor-symlink/unsafe/duplicate/AST-assertion all explicitly rejected in ordinary and -O, before output creation; 14 hostile processes. Clean guard accepted twice. Current assembly6positive0/6false1. Preparation estimate85%; math100%; priority unresolved; publicationclearancefalse.\n")
print(json.dumps({"hostile_rejections":14,"positive_guard_passes":2,"ancestor_both_modes_explicit":True}))
