from pathlib import Path
import json,hashlib,stat,datetime
a=Path(__file__).resolve().parents[1];c=Path(__file__).resolve().parent;s=a.parents[1]/"sources"
sha=lambda q:hashlib.sha256(q.read_bytes()).hexdigest()
old=json.loads((a/"INITIAL_MANIFEST.json").read_text())
expected={e["path"] for e in old["files"]}|{"INITIAL_MANIFEST.json","INITIAL_SEAL.json"}
actual={str(q.relative_to(a)) for q in a.rglob("*") if q.is_file() and c not in q.parents and q.name not in {"FINAL_MANIFEST.json","FINAL.json"}}
assert actual==expected and len(actual)==34
for e in old["files"]:
 q=a/e["path"];assert(q.stat().st_size,sha(q),stat.S_IMODE(q.stat().st_mode))==(e["bytes"],e["SHA256"],e["mode"])
assert sha(a/"INITIAL_SEAL.json")=="df5f4aa31839b17cee7c5fb603759531ae8a5205641eae9e157b97b9ecf6b715"
sc=json.loads((a/"SOURCE_CUSTODY.json").read_text())
assert {str(q.relative_to(s)) for q in s.rglob("*") if q.is_file()}=={e["path"] for e in sc["files"]}
assert {str(q.relative_to(s)) for q in s.rglob("*") if q.is_dir()}=={e["path"] for e in sc["directories"]}
assert stat.S_IMODE(s.stat().st_mode)==sc["source_root_mode"]
for e in sc["files"]:
 q=s/e["path"];assert(q.stat().st_size,sha(q),stat.S_IMODE(q.stat().st_mode))==(e["bytes"],e["SHA256"],e["mode"])
for e in sc["directories"]:assert stat.S_IMODE((s/e["path"]).stat().st_mode)==e["mode"]
sm=json.loads((c/"SOURCE_ONLY_MANIFEST.json").read_text())
for e in sm["files"]:
 q=c/e["path"];assert(q.stat().st_size,sha(q),stat.S_IMODE(q.stat().st_mode))==(e["bytes"],e["SHA256"],e["mode"])
assert sha(c/"SOURCE_ONLY_SEAL.json")=="c35283715f35f0e65ed9c5e8203dd7be1383d8fc1ab01fedf09489f8cc50d3a4"
now=datetime.datetime.now(datetime.timezone.utc).isoformat();exclude={"FINAL_MANIFEST.json","FINAL.json"};files=[];dirs=[]
for q in sorted(a.rglob("*")):
 r=str(q.relative_to(a));st=q.lstat()
 if stat.S_ISREG(st.st_mode):
  if r not in exclude:files.append({"path":r,"bytes":st.st_size,"SHA256":sha(q),"mode":stat.S_IMODE(st.st_mode)})
 elif stat.S_ISDIR(st.st_mode):dirs.append({"path":r,"mode":stat.S_IMODE(st.st_mode)})
 else:raise RuntimeError("Nonregular lane entry "+r)
m={"schema":"finite-final-lane-manifest-v1","UTC":now,"root":str(a),"root_mode":stat.S_IMODE(a.stat().st_mode),"files":files,"directories":dirs,"exact_terminal_exclusions":sorted(exclude),"no_future_or_subtree_exclusions":True,"extent":"entire adversarial-sol lane including immutable original INITIAL, all six page images, fresh source-only continuation and postseal primary/native evidence; empty streams included"}
mp=a/"FINAL_MANIFEST.json";mp.write_text(json.dumps(m,indent=2)+"\n")
f={"schema":"final-adversarial-lane-v1","UTC":now,"row":186,"record":"23205294","status":"FROZEN_COMPLETE","root":str(a),"manifest":"FINAL_MANIFEST.json","manifest_bytes":mp.stat().st_size,"manifest_SHA256":sha(mp),"manifested_payload_files":len(files),"manifested_child_directories":len(dirs),"total_files_including_two_terminals":len(files)+2,"exact_terminal_exclusions":sorted(exclude),"no_future_or_subtree_exclusions":True,"source_exact_files":56,"source_exact_child_directories":10,"source_FINAL_SHA256":sha(s/"SOURCE_FINAL.json"),"source_MANIFEST_SHA256":sha(s/"SOURCE_MANIFEST.json"),"preserved_original_INITIAL_files":34,"original_INITIAL_SEAL_SHA256":sha(a/"INITIAL_SEAL.json"),"fresh_source_only_SEAL_SHA256":sha(c/"SOURCE_ONLY_SEAL.json"),"informed_continuation":True,"review":"continuation-20261117/REVIEW.md","result":"continuation-20261117/RESULT.json","primary_check":"continuation-20261117/PRIMARY_PROOF_CHECK.md","ordinary_native_runs":1,"ordinary_native_exit":0,"opposite_family_read":False,"root_mathematical_findings_read":False,"follow_up":None,"open_handles":[],"completion_estimate_percent":100,"future_writes_authorized":False}
(a/"FINAL.json").write_text(json.dumps(f,indent=2)+"\n")
